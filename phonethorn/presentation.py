"""Safe human-readable PHONETHORN terminal summaries."""
def print_clean(report, colors, paint):
    number = report.get('number_intelligence') or {}
    echo = report.get('web_echo') or {}
    print(paint('\n◆ PHONE INTELLIGENCE', 'cyan', colors))
    if number:
        def line(key, value):
            print('  {:<19} {}'.format(key, value))
        line('Phone', number.get('international', number.get('e164','Unknown')))
        line('Format valid', number.get('valid', 'Unknown'))
        line('Numbering region', number.get('region_description','Unknown'))
        line('Time-zone hint', ', '.join(number.get('time_zone_hints') or []) or 'Unknown')
        line('Line type', number.get('number_type','Unknown'))
        line('Current carrier', 'Not verified' if not report.get('twilio_line_intelligence') else 'See full report')
    if echo:
        print(paint('\n◆ PUBLIC RESEARCH', 'cyan', colors))
        print('  Number formats      {}'.format(len(echo.get('variants',[]))))
        print('  Research links      {}'.format(echo.get('reference_count', 0)))
        print('  Verified web hits   Not established from search links')
        print('  Search mode         Links only (no search-result scraping)')
    if 'business_page_match' in report:
        match = report['business_page_match']
        print(paint('\n◆ PUBLIC PAGE CHECK', 'cyan', colors))
        print('  Outcome             {}'.format('Text mention reported; review source' if match.get('match_found') else 'No verified mention'))
    if 'fusion_evidence' in report:
        print(paint('\n◆ FUSION', 'cyan', colors))
        print('  [PASS] Evidence categories: {}'.format(len(report['fusion_evidence'].get('evidence',[]))))
    for key, title in [('ip_geolocation','IP GEO'),('photo_gps_metadata','PHOTO METADATA'),('supplied_coordinate_map','COORDINATES'),('device_diagnostics','LOCAL DEVICES')]:
        if key in report:
            print(paint('\n◆ '+title, 'cyan', colors))
            print('  [READY] Details available in saved report or --verbose output')
    print(paint('\n◆ NOTICE', 'pink', colors))
    print('  Numbering region is not live GPS. Phone ownership is not verified.')
