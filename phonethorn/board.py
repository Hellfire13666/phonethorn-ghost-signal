"""Offline public contact research board, no remote embedded content."""
import html, json, base64
from pathlib import Path

def board_html(report):
    esc=lambda x: html.escape(str(x),quote=True)
    echo=report.get('web_echo',{})
    match=report.get('business_page_match')
    banner=Path(__file__).resolve().parent.parent/'PHONETHORN-COVER.png'
    banner_html=''
    if banner.exists():
        banner_html='<img class="cover" src="data:image/png;base64,'+base64.b64encode(banner.read_bytes()).decode()+'" alt="Original PHONETHORN cover artwork">'
    rows=[]
    for item in echo.get('public_search_references',[]):
        links=' · '.join('<a rel="noopener noreferrer" target="_blank" href="'+esc(url)+'">'+esc(label)+'</a>' for label,url in item['engines'].items())
        rows.append('<div class="card"><h3>'+esc(item['format'])+'</h3>'+links+'</div>')
    if match:
        rows.insert(0,'<div class="card"><h3>Checked public business page</h3><p>'+esc(match.get('url',''))+'</p><p>Status: '+esc('text mention found' if match.get('match_found') else 'no match or error')+'</p><small>Not proof of ownership</small></div>')
    raw=esc(json.dumps(report,indent=2,ensure_ascii=False))
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'"><title>PHONETHORN // PUBLIC EVIDENCE</title><style>*{box-sizing:border-box}body{background:#090911;color:#f0eefa;font:16px system-ui;margin:0}.wrap{max-width:1080px;margin:auto;padding:22px}.cover{display:block;max-width:100%;height:auto;margin:0 auto 30px;border-radius:12px}h1{color:#ff1493;font-size:clamp(30px,5vw,60px)}h2{color:#48e9f1}.card{background:#171424;border:1px solid #5f3d6c;border-radius:14px;padding:18px;margin:12px 0;overflow-wrap:anywhere}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px}a{color:#ff72c6}.warn{border-left:4px solid #ff1493;padding:16px;background:#211324}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}</style></head><body><main class="wrap">"""+banner_html+"""<h1>PHONETHORN // GHOST SIGNAL</h1><h2>PUBLIC CONTACT RESEARCH</h2><p class="warn">Search links are research shortcuts, not findings. No subscriber identity or phone GPS can be inferred. This file is local and private; do not publish it.</p><p>Research references: """+esc(echo.get('reference_count',0))+""" · Direct verified matches: not established</p><div class="grid">"""+''.join(rows)+"""</div><details class="card"><summary>Full metadata and evidence (JSON)</summary><pre>"""+raw+"""</pre></details></main></body></html>"""
