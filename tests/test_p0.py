import http.cookiejar
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

class P0Smoke(unittest.TestCase):
    def test_inline_scripts_parse(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('Install Node.js to check browser script syntax')
        for name in ('display.html', 'index.html', 'photos.html'):
            html = (ROOT / name).read_text()
            scripts = html.split('<script>')[1:]
            self.assertTrue(scripts, name)
            for script in scripts:
                source = script.split('</script>', 1)[0]
                result = subprocess.run([node, '--check', '--input-type=commonjs'], input=source, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, f'{name}: {result.stderr}')

    def test_lobby_vote_reveal_and_advance(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('server.py', 'data.py', 'display.html', 'index.html', 'photos.html', 'style.css'):
                shutil.copy2(ROOT / name, Path(tmp) / name)
            with socket.socket() as sock:
                sock.bind(('127.0.0.1', 0))
                port = sock.getsockname()[1]
            env = dict(os.environ, PORT=str(port), VOTE_SECONDS='15', REVEAL_SECONDS='1')
            proc = subprocess.Popen(['python3', 'server.py', '2'], cwd=tmp, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            url = f'http://127.0.0.1:{port}'
            a = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
            b = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
            def get(client, path):
                import json
                return json.load(client.open(url + path, timeout=2))
            def post(client, path, payload):
                import json
                request = urllib.request.Request(url + path, json.dumps(payload).encode(), {'Content-Type': 'application/json'})
                return json.load(client.open(request, timeout=2))
            try:
                for _ in range(50):
                    try:
                        self.assertIn(b'FAT BEAR', a.open(url + '/display', timeout=1).read())
                        break
                    except (OSError, AssertionError):
                        time.sleep(.1)
                else:
                    self.fail('Server did not start')
                self.assertFalse(get(a, '/api/state')['started'])
                post(a, '/api/join', {'name': 'Alice'})
                post(b, '/api/join', {'name': 'Bob'})
                state = get(a, '/api/state')
                self.assertTrue(state['started'])
                self.assertEqual(state['games'][0]['status'], 'open')
                self.assertEqual(state['me'], 'Alice')
                post(a, '/api/vote', {'choice': '132'})
                post(b, '/api/vote', {'choice': '284'})
                self.assertEqual(get(a, '/api/state')['games'][0]['status'], 'locked')
                deadline = time.monotonic() + 7
                while time.monotonic() < deadline:
                    state = get(a, '/api/state')
                    if state['cursor'] == 1:
                        break
                    time.sleep(.1)
                self.assertEqual(state['cursor'], 1)
                self.assertEqual(state['games'][0]['status'], 'revealed')
                self.assertEqual(state['games'][0]['winner'], '132')
                self.assertEqual(state['games'][1]['status'], 'open')
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()

if __name__ == '__main__':
    unittest.main()
