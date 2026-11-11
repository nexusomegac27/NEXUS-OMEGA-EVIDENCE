from pathlib import Path
import http.server, functools, threading
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent.parent
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root))
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/tests/layout-fixture.html'
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page()
  for w,h in [(1280,800),(768,1024),(390,844),(320,640)]:
    page.set_viewport_size({'width':w,'height':h});page.goto(url);page.wait_for_function("document.documentElement.dataset.nexusBodytwinLayout==='PASS_ISOLATED_PANEL'")
    data=page.evaluate("""() => {
      let a=document.getElementById('viewer').getBoundingClientRect(),b=document.getElementById('nexus-bodytwin-live-c1').getBoundingClientRect(),m=document.querySelector('main').getBoundingClientRect();
      return {count:document.querySelectorAll('#nexus-bodytwin-live-c1').length, outsideMain:!document.querySelector('main').contains(document.getElementById('nexus-bodytwin-live-c1')), viewerBottom:a.bottom,panelTop:b.top, panelLeft:b.left, panelRight:b.right,viewport:innerWidth, layout:document.documentElement.dataset.nexusBodytwinLayout};
    }""")
    assert data['count']==1 and data['outsideMain'] and data['viewerBottom']<=data['panelTop'] and data['panelLeft']>=0 and data['panelRight']<=w, data
    print('PASS',w,'x',h,data)
  browser.close()
server.shutdown()
