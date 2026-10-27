"""PHONETHORN: offline-first, ownership-respecting phone recovery toolkit."""
import argparse
import datetime as dt
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import webbrowser
from urllib.parse import quote_plus, quote, urlparse
from urllib.request import Request, urlopen
import ipaddress
from .fusion import number_variants, web_echo, inspect_public_business_page, twilio_line_type, fusion_evidence
from .terminal_art import banner as print_banner

VERSION = '0.5.0'
OFFICIAL = {
    'android': 'https://android.com/find',
    'iphone': 'https://www.icloud.com/find',
    'google-account': 'https://myaccount.google.com/device-activity',
    'apple-account': 'https://account.apple.com/',
    'fcc-lost-phone': 'https://www.fcc.gov/consumers/guides/protect-your-mobile-device',
}
COLORS = {'pink':'\033[95m','cyan':'\033[96m','green':'\033[92m','yellow':'\033[93m','violet':'\033[35m','reset':'\033[0m'}

def paint(s, color, enabled):
    return (COLORS[color] + str(s) + COLORS['reset']) if enabled else str(s)

def safe_run(argv, timeout=8):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
        return {'available': True, 'exit_code': p.returncode, 'stdout': p.stdout[:2500], 'stderr': p.stderr[:500]}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {'available': False, 'error': type(e).__name__}

def device_diagnostics():
    result = {'usb_listing': None, 'adb_devices': None, 'notice': 'Use only with a device you own or have permission to inspect. USB/ADB never tracks a phone remotely.'}
    if shutil.which('lsusb'):
        result['usb_listing'] = safe_run(['lsusb'])
    if shutil.which('adb'):
        result['adb_devices'] = safe_run(['adb', 'devices', '-l'])
    return result

def lookup(number, region):
    try:
        import phonenumbers
        from phonenumbers import carrier, geocoder, timezone
    except ImportError:
        raise RuntimeError('Missing phonenumbers. Run ./INSTALL.sh or pip install phonenumbers.')
    try:
        n = phonenumbers.parse(number, region)
    except phonenumbers.NumberParseException as e:
        return {'input': number, 'error': str(e), 'valid': False}
    region_code = phonenumbers.region_code_for_number(n)
    type_code = phonenumbers.number_type(n)
    type_names = {
        phonenumbers.PhoneNumberType.MOBILE:'MOBILE',
        phonenumbers.PhoneNumberType.FIXED_LINE:'FIXED_LINE',
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE:'FIXED_LINE_OR_MOBILE',
        phonenumbers.PhoneNumberType.TOLL_FREE:'TOLL_FREE',
        phonenumbers.PhoneNumberType.PREMIUM_RATE:'PREMIUM_RATE',
        phonenumbers.PhoneNumberType.VOIP:'VOIP',
        phonenumbers.PhoneNumberType.UNKNOWN:'UNKNOWN',
    }
    return {
        'input': number,
        'e164': phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164),
        'international': phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        'national': phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.NATIONAL),
        'possible': phonenumbers.is_possible_number(n),
        'valid': phonenumbers.is_valid_number(n),
        'number_type': type_names.get(type_code, str(type_code)),
        'numbering_region': region_code,
        'region_description': geocoder.description_for_number(n, 'en'),
        'time_zone_hints': list(timezone.time_zones_for_number(n)),
        'original_carrier_hint': carrier.name_for_number(n, 'en') or None,
        'carrier_warning': 'Original allocation only. NOT a verified current provider; number portability can change carriers.',
        'geo_warning': 'Region description is NOT live GPS location or a device position.',
    }

def public_links(num):
    q = quote_plus('"' + num + '"')
    return {
        'web_search': 'https://www.google.com/search?q=' + q,
        'bing_search': 'https://www.bing.com/search?q=' + q,
    }

def rescue_steps(platform):
    return [
        'Sign in personally at the official device-find service. Never share passwords or one-time codes.',
        'Check your account\'s registered devices; ring, locate, secure/mark lost where supported.',
        'If you suspect theft, avoid confronting anyone at a map pin. Contact local authorities.',
        'Call your carrier via its verified official support page; request SIM suspension and ask about port-out protection.',
        'Find your IMEI from original purchase records/account documentation; do not publish it.',
        'Update important passwords and remove exposed sessions where appropriate.',
        'Beware paid number-to-GPS sites and fake recovery texts; number-only live tracking is not reliable.',
    ]


def ip_geo(address, live=False):
    """Check an IP locally; optional user-requested approximate public IP geolocation."""
    ip = ipaddress.ip_address(address)
    result = {'ip': str(ip), 'version': ip.version, 'is_global': ip.is_global,
              'disclaimer': 'IP geolocation is approximate, not a phone or person GPS fix.'}
    if live:
        if not ip.is_global:
            result['notice'] = 'Non-public IP: cannot query an external geolocation service.'
        else:
            try:
                req = Request('https://ipwho.is/' + quote(str(ip)), headers={'User-Agent':'PHONETHORN/0.3 (personal recovery)'})
                with urlopen(req, timeout=8) as response:
                    obj = json.load(response)
                if obj.get('success'):
                    result['approximate_geography'] = {k:obj.get(k) for k in ('continent','country','region','city','latitude','longitude')}
                    result['network'] = {k:obj.get('connection', {}).get(k) for k in ('asn','org','isp')}
                    result['provider'] = 'ipwho.is'
                else:
                    result['error'] = str(obj.get('message', 'Provider did not return a location'))
            except Exception as e:
                result['error'] = 'Network/provider failure: ' + type(e).__name__
    return result

def coordinate_geo(lat, lon):
    lat, lon = float(lat), float(lon)
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError('Coordinate ranges must be latitude -90..90, longitude -180..180')
    return {'latitude':lat, 'longitude':lon,
            'map_url':'https://www.openstreetmap.org/?mlat='+str(lat)+'&mlon='+str(lon)+'#map=14/'+str(lat)+'/'+str(lon),
            'notice':'Coordinates supplied by you, not derived from a phone number.'}

def photo_geo(filename):
    """Read GPS EXIF only from a local photo. No uploads."""
    try:
        from PIL import Image, ExifTags
    except ImportError:
        raise RuntimeError('Photo GPS needs Pillow. Install with .venv/bin/pip install Pillow')
    path = Path(filename).expanduser().resolve()
    if not path.is_file():
        raise ValueError('Photo not found')
    with Image.open(path) as img:
        exif = img.getexif()
        gps = exif.get_ifd(34853) if exif else {}
    if not gps:
        return {'photo':path.name, 'gps_found':False, 'notice':'No embedded GPS coordinates. Many apps remove EXIF metadata.'}
    def decimal(values, ref):
        a,b,c = [float(x) for x in values]
        return (a+b/60+c/3600) * (-1 if ref in ('S','W',b'S',b'W') else 1)
    try:
        lat = decimal(gps[2], gps[1]); lon = decimal(gps[4], gps[3])
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return {'photo':path.name, 'gps_found':False, 'notice':'Incomplete or invalid GPS tags.'}
    return {'photo':path.name, 'gps_found':True, **coordinate_geo(lat,lon),
            'accuracy_notice':'Embedded metadata can be old, edited, or forged. Not live device tracking.'}

def make_report(number=None, region='US', rescue=None, devices=False, public=False):
    report = {
        'tool': 'PHONETHORN // GHOST SIGNAL', 'version': VERSION,
        'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'offline_lookup': True, 'contact_or_live_location': False,
        'official_recovery_links': OFFICIAL,
        'limitations': ['No subscriber identity or private records.', 'No current carrier verification.', 'No live device GPS from a phone number.', 'No automatic remote access.'],
    }
    if number:
        report['number_intelligence'] = lookup(number, region)
        if public:
            report['manual_public_search_links'] = public_links(number)
            report['public_search_notice'] = 'Links only; no scraping or claims about people. Verify independently.'
    if rescue:
        report['rescue_platform'] = rescue
        report['rescue_checklist'] = rescue_steps(rescue)
        report['find_device_url'] = OFFICIAL[rescue]
    if devices:
        report['local_device_diagnostics'] = device_diagnostics()
    return report

def render_html(data):
    payload = html.escape(json.dumps(data, indent=2, ensure_ascii=False))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PHONETHORN • Cosmic Kitty Report</title><style>
:root{{--pink:#ff1493;--cyan:#55eaff;--violet:#a77bff;--dark:#080808}}*{{box-sizing:border-box}}body{{background:radial-gradient(ellipse at top right,#271146 0%,#090915 42%,#080808 90%);color:#f5efff;font:16px system-ui,sans-serif;max-width:1040px;margin:0 auto;padding:36px 22px}}.hero{{border:1px solid #b84a9b;border-radius:24px;padding:36px 26px;background:linear-gradient(135deg,#280c38cc,#09111acc);box-shadow:0 0 36px #ff149325}}.eyebrow{{letter-spacing:4px;color:var(--cyan);font-size:12px}}h1{{font-size:clamp(30px,5vw,58px);color:var(--pink);margin:12px 0;text-shadow:0 0 22px #ff149344}}h2{{color:var(--cyan)}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#12101f;padding:22px;border:1px solid #77509e;border-radius:16px;line-height:1.5}}small{{color:#c3b8ce}}.stars{{letter-spacing:16px;color:var(--violet)}}.cat{{font-size:34px;line-height:1.25;white-space:pre;color:var(--cyan)}}.warn{{color:#ffd09d;margin-top:16px}}</style></head><body><div class="hero"><div class="eyebrow">GLITCHBYTE PHANTOM LABS • ANONYMISSGLITCH DIVISION</div><div class="cat"> /\\_/\\  ✦<br>( o.o )  ☄<br> &gt; ^ &lt;</div><h1>PHONETHORN</h1><h2>GHOST SIGNAL // COSMIC KITTIES</h2><p>Evidence before assumptions. Coordinates are not conjured from numbers.</p><div class="stars">✦ ⋆ ✧ ⋆ ✦</div></div><p class="warn">PRIVATE LOCAL REPORT: Share carefully. A phone-number region, photo EXIF and IP geolocation are distinct clues, never verified live phone GPS.</p><pre>{payload}</pre><small>v{VERSION} • Offline report viewer. No embedded remote scripts.</small></body></html>'''

def save_report(report, out, fmt):
    dest = Path(out).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
    output = []
    body = json.dumps(report, indent=2, ensure_ascii=False)
    for kind in (['html','json','txt'] if fmt == 'all' else [fmt]):
        target = dest / f'PHONETHORN-{ts}.{kind}'
        target.write_text(render_html(report) if kind == 'html' else body + '\n', encoding='utf-8')
        try:
            os.chmod(target, 0o600)
        except OSError:
            pass
        output.append(str(target))
    return output

EXAMPLES = """
  PHONETHORN QUICK RECIPES  •  COPY + PASTE
  phonethorn --demo --out ~/PhoneThornReports
  phonethorn --phone '+14155552671' --region US
  phonethorn --rescue android --open-find android
  phonethorn --rescue iphone --open-find iphone
  phonethorn --devices
  phonethorn --geo-ip 8.8.8.8
  phonethorn --geo-ip 8.8.8.8 --live-geo
  phonethorn --coords 40.7128 -74.0060
  phonethorn --photo-gps ~/Pictures/my-own-photo.jpg
  phonethorn --phone '+14155552671' --public-links --out ~/PhoneThornReports
  phonethorn --phone '+14155552671' --web-intel
  phonethorn --phone '+14155552671' --web-url https://example.org/contact
  phonethorn --phone '+14155552671' --carrier  # requires Twilio API keys, billed
  phonethorn --phone '+14155552671' --fusion --out ~/PhoneThornReports
  No live phone GPS from a telephone number.
"""


def print_switch_menu():
    """Human-readable switchboard; display only, never perform a lookup."""
    print("""
  ╔══════════════════════ PHONETHORN SWITCHBOARD ══════════════════════╗
  ║  PHONE SIGNALS                                                     ║
  ║    --phone NUMBER --region US         Number metadata              ║
  ║    --phone NUMBER --web-intel         Public search links          ║
  ║    --phone NUMBER --fusion            Evidence fusion              ║
  ║    --phone NUMBER --web-url URL       Public business contact     ║
  ║    --phone NUMBER --carrier           Optional paid provider      ║
  ║  FIELD TOOLS                                                       ║
  ║    --geo-ip IP [--live-geo]           Approximate IP location     ║
  ║    --coords LAT LON                   Known coordinates map       ║
  ║    --photo-gps PHOTO                  Own photo EXIF              ║
  ║    --devices                          Local device inventory      ║
  ║  RECOVERY & REPORTS                                                ║
  ║    --rescue android|iphone            Official recovery steps     ║
  ║    --out DIRECTORY                    Save HTML, JSON & TXT        ║
  ║    --demo    --examples               Offline demo / recipes     ║
  ║  LOOKS & CONTROLS                                                  ║
  ║    --menu          --show-art          Menu / banner only          ║
  ║    --banner kitty|ghost|signal        Choose ASCII mascot        ║
  ║    --theme neon|ember|frost|mono      Choose color scheme        ║
  ║    --no-banner    --color never       Quiet / plain output       ║
  ╚════════════════════════════════════════════════════════════════════╝
  TIP: ./RUN.sh --phone '+14155552671' --fusion --out ./PhoneThornReports
  NOTE: Phone numbers never reveal live GPS. Use authorized data only.
""")

def main(argv=None):
    p = argparse.ArgumentParser(prog='phonethorn', description='Offline phone metadata, lost-device recovery and local diagnostics')
    p.add_argument('--demo', action='store_true', help='Run a safe offline synthetic demonstration')
    p.add_argument('--menu', action='store_true', help='Display standalone command switchboard, without running lookups')
    p.add_argument('--examples', action='store_true', help='Show copy-ready beginner recipes')
    p.add_argument('--geo-ip', help='Analyze IP address without making network calls unless --live-geo is set')
    p.add_argument('--live-geo', action='store_true', help='Opt in to a third-party approximate public IP geolocation lookup')
    p.add_argument('--coords', nargs=2, metavar=('LAT','LON'), help='Create map link from coordinates you already know')
    p.add_argument('--photo-gps', help='Read local photo GPS EXIF without uploading the photo')
    p.add_argument('--phone', help='Your number or a number you are authorized to research')
    p.add_argument('--region', default='US', help='Default number parsing region, e.g. US, GB, CA')
    p.add_argument('--rescue', choices=['android','iphone'], help='Add official lost-device recovery checklist')
    p.add_argument('--open-find', choices=['android','iphone'], help='Open official device-find sign-in in your browser')
    p.add_argument('--devices', action='store_true', help='Read-only local lsusb and adb devices inventory')
    p.add_argument('--web-intel', action='store_true', help='Generate public business/contact search links; no automatic search harvesting')
    p.add_argument('--web-url', help='Opt-in: inspect one public HTTPS business contact page for number matches')
    p.add_argument('--carrier', action='store_true', help='Opt in to billable Twilio Lookup v2 line type intelligence using TWILIO_API_KEY and TWILIO_API_SECRET')
    p.add_argument('--fusion', action='store_true', help='Combine offline phone data, public search links and evidence labels (no paid calls unless --carrier)')
    p.add_argument('--public-links', action='store_true', help='Build manual public search links for a phone number')
    p.add_argument('--out', help='Save reports in directory')
    p.add_argument('--format', choices=['all','html','json','txt'], default='all')
    p.add_argument('--color', choices=['auto','always','never'], default='auto')
    p.add_argument('--banner', choices=['kitty','ghost','signal'], default='kitty', help='Select original terminal ASCII artwork')
    p.add_argument('--theme', choices=['neon','ember','frost','mono'], default='neon', help='Set terminal-art color palette')
    p.add_argument('--no-banner', action='store_true', help='Suppress decorative terminal art')
    p.add_argument('--show-art', action='store_true', help='Preview selected ASCII artwork and exit')
    p.add_argument('--version', action='version', version='PHONETHORN ' + VERSION)
    args = p.parse_args(argv)
    colors = args.color == 'always' or (args.color == 'auto' and sys.stdout.isatty())
    if not args.no_banner:
        print_banner(args.banner, args.theme, args.color)
    if args.show_art:
        return 0
    if args.menu or not (argv if argv is not None else sys.argv[1:]):
        print_switch_menu()
        return 0
    if args.examples:
        print(EXAMPLES)
        return 0
    if args.demo:
        report = make_report(rescue='android')
        report['demo_ip'] = ip_geo('203.0.113.17')
        report['demo_coords'] = coordinate_geo(40.7128, -74.0060)
        report['demo_notice'] = 'Synthetic documentation IP and example NYC coordinates; no real phone location.'
        if args.out:
            for f in save_report(report, args.out, args.format): print('SAVED '+f)
        else:
            print(json.dumps(report, indent=2))
        return 0
    if (args.web_intel or args.web_url or args.carrier or args.fusion) and not args.phone:
        p.error('--web-intel, --web-url, --carrier and --fusion require --phone')
    if not any([args.phone, args.rescue, args.open_find, args.devices, args.geo_ip, args.coords, args.photo_gps]):
        p.print_help()
        return 0
    try:
        report = make_report(args.phone, args.region.upper(), args.rescue or args.open_find, args.devices, args.public_links)
        if args.phone and (args.web_intel or args.fusion or args.web_url):
            number = report.get('number_intelligence', {}).get('e164', args.phone)
            report['web_echo'] = web_echo(number, args.region.upper())
        if args.web_url:
            report['business_page_match'] = inspect_public_business_page(args.web_url, report['number_intelligence'].get('e164', args.phone))
        if args.web_url or args.carrier or args.live_geo:
            report['offline_lookup'] = False
        if args.carrier:
            report['twilio_line_intelligence'] = twilio_line_type(report['number_intelligence'].get('e164', args.phone))
        if args.fusion:
            report['fusion_evidence'] = fusion_evidence(report)
        if args.geo_ip:
            report['ip_geolocation'] = ip_geo(args.geo_ip, args.live_geo)
        if args.coords:
            report['supplied_coordinate_map'] = coordinate_geo(*args.coords)
        if args.photo_gps:
            report['photo_gps_metadata'] = photo_geo(args.photo_gps)
    except (RuntimeError, ValueError) as e:
        print(paint('ERROR: ' + str(e), 'yellow', colors), file=sys.stderr)
        return 2
    if args.phone and 'error' in report.get('number_intelligence', {}):
        print(paint('INVALID INPUT: ' + report['number_intelligence']['error'], 'yellow', colors))
    for k,v in report.items():
        if k == 'official_recovery_links' and not (args.rescue or args.open_find):
            continue
        if k in ('tool','version','generated_utc','offline_lookup','contact_or_live_location'):
            continue
        print(paint('\n◆ ' + k.upper(), 'cyan', colors))
        if isinstance(v, dict):
            for item, value in v.items():
                print('  ' + paint(item, 'green', colors) + ': ' + str(value))
        elif isinstance(v, list):
            for item in v:
                print('  • ' + item)
        else:
            print('  ' + str(v))
    if args.out:
        for f in save_report(report, args.out, args.format):
            print(paint('SAVED ', 'green', colors) + f)
    else:
        print(paint('\nSAVE OFF • terminal only', 'yellow', colors))
    if args.open_find:
        print('Opening official: ' + OFFICIAL[args.open_find])
        webbrowser.open(OFFICIAL[args.open_find])
    return 0
