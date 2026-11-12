"""Renderiza 'placas' 3D (cor + profundidade + matriz de câmera) com three.js no Chrome headless.
Uso: python3 plates.py specs.json OUT_DIR   (pula placas que já existem -> retomável)
spec: {"id":..., "set":"beach", "light":"night", "w":2560, "h":1440, "cam":{"pos":[x,y,z],"look":[x,y,z],"fov":40}, "opts":{...}}
"""
import sys, os, json, base64, hashlib, threading, http.server, socketserver, functools, time
from playwright.sync_api import sync_playwright

WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'web')

def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WEB)
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    httpd = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=WEB))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd.server_address[1]

def key(spec):
    s = dict(spec); s.pop('id', None)
    return hashlib.md5(json.dumps(s, sort_keys=True).encode()).hexdigest()[:10]

def render_all(specs, out):
    os.makedirs(out, exist_ok=True)
    todo = [s for s in specs if not os.path.exists(os.path.join(out, s['id'] + '.json'))]
    if not todo: return
    port = serve()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        pg = b.new_page()
        pg.on('console', lambda m: print('[js]', m.text) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: print('[pageerror]', e))
        pg.goto(f'http://127.0.0.1:{port}/index.html'); pg.wait_for_function('window.ready === true', timeout=60000)
        for i, s in enumerate(todo):
            t0 = time.time()
            r = pg.evaluate('async (s) => await window.renderPlate(s)', s)
            for k in ('color', 'depth'):
                open(os.path.join(out, f"{s['id']}_{k}.png"), 'wb').write(base64.b64decode(r[k].split(',', 1)[1]))
            json.dump({'P': r['P'], 'far': r['far'], 'w': r['w'], 'h': r['h'], 'spec': s}, open(os.path.join(out, s['id'] + '.json'), 'w'))
            print(f"placa {s['id']} ({i+1}/{len(todo)}) {time.time()-t0:.1f}s", flush=True)
        b.close()

if __name__ == '__main__':
    render_all(json.load(open(sys.argv[1])), sys.argv[2])
