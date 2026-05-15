import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[2]
SECRETS = Path('/data/.openclaw/credentials/user-secrets.json')
REPO = 'wilmington-market-site'
VERCEL_BIN = '/data/.npm-global/bin/vercel'

data = json.load(SECRETS.open())
gh_token = (((data.get('tokens') or {}).get('github') or {}).get('personalAccessToken'))
vercel_token = (((data.get('tokens') or {}).get('vercel') or {}).get('token'))
if not gh_token:
    raise SystemExit('Missing GitHub token')
if not vercel_token:
    raise SystemExit('Missing Vercel token')

def gh(method, path, body=None):
    payload = None if body is None else json.dumps(body).encode()
    req = Request('https://api.github.com' + path, data=payload, method=method)
    req.add_header('Authorization', f'Bearer {gh_token}')
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('X-GitHub-Api-Version', '2022-11-28')
    if payload: req.add_header('Content-Type', 'application/json')
    try:
        with urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or '{}')
    except HTTPError as e:
        text=e.read().decode()
        if e.code == 422 and method == 'POST' and path == '/user/repos':
            return e.code, {'exists': True, 'raw': text}
        raise SystemExit(f'GitHub API error {e.code}: {text}')

status, user = gh('GET', '/user')
owner = user['login']
status, created = gh('POST', '/user/repos', {'name': REPO, 'private': False, 'auto_init': False, 'description': 'Port City AI Growth Wilmington AI-focused local growth site'})
remote = f'https://x-access-token:{gh_token}@github.com/{owner}/{REPO}.git'
subprocess.run(['git','remote','remove','origin'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(['git','remote','add','origin',remote], cwd=ROOT, check=True)
subprocess.run(['git','push','-u','origin','main'], cwd=ROOT, check=True)
print(f'GITHUB_URL https://github.com/{owner}/{REPO}')

env = os.environ.copy()
env['VERCEL_TOKEN'] = vercel_token
cmd = [VERCEL_BIN, 'deploy', '--prod', '--yes', '--token', vercel_token]
proc = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
last_url = None
for line in proc.stdout:
    sys.stdout.write(line)
    sys.stdout.flush()
    if 'https://' in line and 'Inspect:' not in line:
        for part in line.strip().split():
            if part.startswith('https://'):
                last_url = part
ret = proc.wait()
if ret:
    raise SystemExit(ret)
if last_url:
    print('VERCEL_URL', last_url)
