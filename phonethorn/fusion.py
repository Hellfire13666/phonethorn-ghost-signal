"""PHONETHORN v0.6.3: provenance-first phone and public business intelligence."""
import base64
import datetime as dt
import html
import ipaddress
import json
import os
import re
import socket
from urllib.parse import quote, quote_plus, urlparse
from urllib.request import Request, urlopen

USER_AGENT = 'PHONETHORN/0.6.2 (single-page public business verification)'

def number_variants(number, region='US'):
    """Canonical and presentation variants; no bulk candidate enumeration."""
    digits = re.sub(r'\D', '', number)
    if not (7 <= len(digits) <= 15):
        raise ValueError('Expected one phone number, 7–15 digits')
    variants = [number.strip(), '+' + digits, digits]
    try:
        import phonenumbers
        n = phonenumbers.parse(number, region)
        variants += [phonenumbers.format_number(n, f) for f in
                     (phonenumbers.PhoneNumberFormat.E164,
                      phonenumbers.PhoneNumberFormat.INTERNATIONAL,
                      phonenumbers.PhoneNumberFormat.NATIONAL)]
    except Exception:
        pass
    return list(dict.fromkeys(v.strip() for v in variants if v.strip()))[:7]

def web_echo(number, region='US'):
    """Diverse research links, not scraped results or confirmed number ownership."""
    variants = number_variants(number, region)
    digits = re.sub(r'\D', '', number)
    local = digits[-10:]
    presentations = [*variants]
    if len(local) == 10:
        presentations += [f'{local[:3]}-{local[3:6]}-{local[6:]}',
                          f'({local[:3]}) {local[3:6]}-{local[6:]}',
                          f'{local[:3]}.{local[3:6]}.{local[6:]}']
    presentations = list(dict.fromkeys(presentations))
    searches = []
    services = {
        'Google': 'https://www.google.com/search?q=',
        'Bing': 'https://www.bing.com/search?q=',
        'Brave': 'https://search.brave.com/search?q=',
        'DuckDuckGo': 'https://duckduckgo.com/?q=',
    }
    from urllib.parse import quote_plus
    for display in presentations:
        query = '"' + display + '"'
        searches.append({'format': display, 'query': query,
                         'engines': {label: prefix + quote_plus(query) for label,prefix in services.items()}})
    return {'variants': presentations, 'public_business_searches': [{'query': row['query'], 'google': row['engines']['Google'], 'bing': row['engines']['Bing']} for row in searches], 'public_search_references': searches,
            'reference_count': len(presentations)*len(services),
            'mode': 'manual public search references (no result scraping)',
            'note': 'A public mention is not verified ownership, carrier or location.'}

def _public_https_host(url):
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.port not in (None,443):
        raise ValueError('Only public HTTPS websites on the standard port are supported')
    host = parsed.hostname
    if host.lower() == 'localhost' or host.endswith('.local') or '.' not in host:
        raise ValueError('Internal host is not permitted')
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    for addr in addresses:
        ip = ipaddress.ip_address(addr[4][0])
        if not ip.is_global:
            raise ValueError('Private or non-public network destinations are blocked')
    return parsed

def inspect_public_business_page(url, number):
    """Opt-in single URL contact matching. No link following, redirects or crawl."""
    _public_https_host(url)
    # Disable redirects to prevent implicit jumps to private hosts.
    from urllib.request import build_opener, HTTPRedirectHandler
    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, request, fp, code, msg, headers, newurl):
            return None
    req = Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html'})
    try:
        with build_opener(NoRedirect).open(req, timeout=7) as resp:
            if 'text/html' not in resp.headers.get('Content-Type', ''):
                return {'url': url, 'error': 'URL did not return HTML'}
            raw = resp.read(512_001)
            if len(raw) > 512_000:
                return {'url': url, 'error': 'Page larger than 500 KiB limit'}
            body = html.unescape(raw.decode('utf-8', errors='replace'))
    except Exception as e:
        return {'url': url, 'error': 'Page unavailable: ' + type(e).__name__}
    # compare digit sequences in page without returning unrelated personal contacts
    target = re.sub(r'\D', '', number)
    words = re.findall(r'(?:\+?\d[\d ().\-]{5,}\d)', body)
    matches = sorted(set(w.strip()[:48] for w in words if re.sub(r'\D', '', w).endswith(target[-10:])))
    return {'url': url, 'matching_phone_mentions': matches[:5], 'match_found': bool(matches),
            'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
            'note': 'Unverified public text mention, not proof of phone ownership; only the supplied page was inspected.'}

def twilio_line_type(number):
    key, secret = os.getenv('TWILIO_API_KEY'), os.getenv('TWILIO_API_SECRET')
    if not (key and secret):
        return {'status': 'not_configured', 'notice': 'Paid Twilio lookup NOT requested. Set TWILIO_API_KEY and TWILIO_API_SECRET in your own shell before using --carrier.'}
    if not re.fullmatch(r'\+[1-9]\d{7,14}', number):
        raise ValueError('Twilio requires a valid E.164 number')
    url = 'https://lookups.twilio.com/v2/PhoneNumbers/' + quote(number, safe='') + '?Fields=line_type_intelligence'
    token = base64.b64encode(f'{key}:{secret}'.encode()).decode()
    req = Request(url, headers={'Authorization': 'Basic ' + token, 'User-Agent': USER_AGENT})
    try:
        with urlopen(req, timeout=10) as resp:
            data = json.load(resp)
        line = data.get('line_type_intelligence')
        return {'source': 'Twilio Lookup v2', 'billable_request': True, 'country_code': data.get('country_code'),
                'valid': data.get('valid'), 'line_type_intelligence': line,
                'notice': 'Provider-supplied network intelligence; does not establish subscriber identity or GPS.'}
    except Exception as e:
        return {'source': 'Twilio Lookup v2', 'billable_request': True, 'error': 'Request failed: ' + type(e).__name__,
                'notice': 'A failed provider request might still be billable. See your provider dashboard.'}

def fusion_evidence(report):
    rows = []
    if 'number_intelligence' in report:
        rows.append({'module': 'offline number metadata', 'evidence': 'number allocation reference data',
                     'confidence': 'metadata only', 'status': 'available'})
    if 'web_echo' in report:
        rows.append({'module': 'web echo', 'evidence': 'outbound manual links, not reviewed results',
                     'confidence': 'not verified', 'status': 'links ready'})
    if 'business_page_match' in report:
        page = report['business_page_match']
        rows.append({'module': 'single public business page', 'source': page['url'],
                     'confidence': 'unverified textual mention', 'status': 'match' if page.get('match_found') else 'no match/error'})
    if 'twilio_line_intelligence' in report:
        rows.append({'module': 'Twilio line type', 'evidence': 'authenticated provider response if configured',
                     'confidence': 'provider reported', 'status': 'provider attempted'})
    return {'evidence': rows, 'live_gps_from_number': False,
            'notes': ['No subscriber identity or private account access.', 'No assumption that matching text proves ownership.',
                      'Research one authorized number at a time.']}
