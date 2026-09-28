#!/usr/bin/env python3
import http.server, io, json, os, re, secrets, sys, threading, time, urllib.request
from http import cookies
from pathlib import Path
from urllib.parse import urlsplit
from data import BEARS, MATCHES, SOURCES, public_bear, MEDIA_SOURCES
BASE=Path(__file__).resolve().parent
DB=BASE/'game.json';MEDIA=BASE/'media';MEDIA.mkdir(exist_ok=True)
PORT=int(os.environ.get('PORT','8765'))
VOTE_SECONDS=int(os.environ.get('VOTE_SECONDS','180'))
REVEAL_SECONDS=int(os.environ.get('REVEAL_SECONDS','12'))
SOURCES=dict(SOURCES)
PROFILES={}
for _b in BEARS:
    _pub=public_bear(_b)
    _pub['lead']=_b.get('tagline','')
    _pub['story']=_b.get('fact','')
    _pub['type']='Contender'
    _pub['before_key']=_b['before_key']
    _pub['card_key']=_b['card_key']
    _pub['official_info']='https://explore.org/meet-the-bears'
    _pub['source']=MEDIA_SOURCES.get(_b['sources']['card'],{}).get('url','')
    _pub['extra_label']=_b.get('card_caption','')
    PROFILES[_b['id']]=_pub
    if _b['id'].startswith('b'):PROFILES[_b['id'][1:]]=_pub
for _m in MATCHES:
    for _bid in _m[:2]:
        if _bid and _bid not in PROFILES:
            PROFILES[_bid]={'id':_bid,'name':f'Bear {_bid}','tagline':'A Brooks River contender.','lead':'A Brooks River contender.','fact':'A contender in the Fat Bear tournament.','story':'A contender in the Fat Bear tournament.','type':'Contender','official_info':'https://explore.org/meet-the-bears','source':'https://explore.org/fat-bear-week','extra_label':'Contender','media':{'before':{'key':f'b{_bid}','url':f'/media/b{_bid}','caption':'Contender','source':'Explore.org'},'card':{'key':f'b{_bid}','url':f'/media/b{_bid}','caption':'Contender','source':'Explore.org'}}}
mutex=threading.RLock()
revision=0

def revise():
    global revision
    revision+=1

def new_game(count):return {'players':{},'votes':{},'status':['queued']*15,'cursor':0,'family':{},'coin_toss':{},'started':False,'roster':[],'expected':count,'deadline':None,'transition_at':None}
def migrate(s,count):
    for k,value in (('players',{}),('votes',{}),('status',['queued']*15),('family',{}),('coin_toss',{})):s.setdefault(k,value)
    s.setdefault('expected',count)
    progress=s.get('cursor',0)>0 or any(s['votes'].values()) or any(x in ('locked','revealed') for x in s['status'])
    s.setdefault('started',progress);s.setdefault('roster',list(s['players']) if progress else [])
    phase=s['status'][s['cursor']]
    s.setdefault('deadline',time.time()+VOTE_SECONDS if s['started'] and phase=='open' else None)
    s.setdefault('transition_at',time.time()+(3 if phase=='locked' else REVEAL_SECONDS) if s['started'] and phase in ('locked','revealed') else None)
    if not s['started']:s['status'][0]='queued'
    return s
try:
    count=int(sys.argv[1]) if len(sys.argv)>1 else 2
    assert 2<=count<=30
except (ValueError,AssertionError):sys.exit('Usage: python3 server.py [2-30 players]')
state=migrate(json.loads(DB.read_text()),count) if DB.exists() else new_game(count)
def save():
    tmp=DB.with_suffix('.tmp');tmp.write_text(json.dumps(state,separators=(',',':')));os.replace(tmp,DB)
save()
def pair(i):return (state['family'].get('12'),state['family'].get('13')) if i==14 else MATCHES[i][:2]
def official(i):return MATCHES[i][0] if MATCHES[i][2]>MATCHES[i][3] else MATCHES[i][1]
def visible(i):
    if i<8:return True
    if i<12:return all(x=='revealed' for x in state['status'][:8])
    if i<14:return all(x=='revealed' for x in state['status'][:12])
    return state['status'][12]==state['status'][13]=='revealed'
def person(handler):
    cookie=cookies.SimpleCookie()
    try:cookie.load(handler.headers.get('Cookie',''))
    except cookies.CookieError:return None
    token=cookie.get('bear_player')
    if not token:return None
    for pid,p in state['players'].items():
        if secrets.compare_digest(token.value,p['token']):return pid
    return None
def launch():
    if not state['started'] and len(state['players'])>=state['expected']:
        state['started']=True;state['roster']=list(state['players']);state['status'][0]='open';state['deadline']=time.time()+VOTE_SECONDS
        state['transition_at']=None;revise()
def all_voted(i):return all(pid in state['votes'].get(str(i),{}) for pid in state['roster'])
def tick():
    if not state['started']:return False
    i=state['cursor'];phase=state['status'][i];now=time.time()
    if phase=='open' and (all_voted(i) or now>=state['deadline']):
        state['status'][i]='locked';state['deadline']=None;state['transition_at']=now+3;return True
    if phase=='locked' and state['transition_at'] is not None and now>=state['transition_at']:
        if i>=12:
            a,b=pair(i);votes=list(state['votes'].get(str(i),{}).values());av=votes.count(a);bv=votes.count(b)
            if av==bv:state['family'][str(i)]=secrets.choice([a,b]);state['coin_toss'][str(i)]=True
            else:state['family'][str(i)]=a if av>bv else b
        state['status'][i]='revealed';state['transition_at']=now+REVEAL_SECONDS;return True
    if phase=='revealed' and state['transition_at'] is not None and now>=state['transition_at']:
        if i==14:state['transition_at']=None;return True
        state['cursor']=i+1;state['status'][i+1]='open';state['deadline']=now+VOTE_SECONDS;state['transition_at']=None;return True
    return False
def timer():
    while True:
        with mutex:
            if tick():
                revise();save()
        time.sleep(.5)
def snapshot(pid):
    games=[]
    for i in range(15):
        a,b=pair(i);show=visible(i);phase=state['status'][i]
        g={'id':i,'round':0 if i<8 else 1 if i<12 else 2 if i<14 else 3,'a':a if show else None,'b':b if show else None,'status':phase if show else 'hidden','voted':len(state['votes'].get(str(i),{})) if show else 0}
        if show and pid:g['my_pick']=state['votes'].get(str(i),{}).get(pid)
        if show and phase=='revealed':
            g['winner']=official(i) if i<12 else state['family'].get(str(i))
            g['official']=i<12;g['totals']=MATCHES[i][2:] if i<12 else None;g['coin_toss']=bool(state['coin_toss'].get(str(i)))
            tally={a:0,b:0}
            for v in state['votes'].get(str(i),{}).values():
                if v in tally:tally[v]+=1
            g['family_votes']=tally
        games.append(g)
    players=[]
    for user_id,p in sorted(state['players'].items(),key=lambda x:x[1]['name'].casefold()):
        score=0;history=[]
        for i,g in enumerate(games):
            choice=state['votes'].get(str(i),{}).get(user_id)
            if g['status']=='revealed':
                if i<12:
                    item='correct' if choice==g['winner'] else 'wrong' if choice else 'missed';score+=item=='correct'
                else:item='prediction' if choice else 'missed'
            else:item='pending' if choice and user_id==pid else 'none'
            history.append(item)
        players.append({'name':p['name'],'score':score,'history':history,'voted':user_id in state['votes'].get(str(state['cursor']),{}) if state['started'] else False})
    return {'me':state['players'][pid]['name'] if pid else None,'games':games,'players':players,
            'cursor':state['cursor'],'phase':str(state['cursor'])+':'+state['status'][state['cursor']],'revision':revision,'expected':state['expected'],'joined':len(state['players']),'roster':len(state['roster']),
            'started':state['started'],'deadline':state['deadline'],'transition_at':state['transition_at'],'now':time.time(),
            'photos_cached':sum((MEDIA/(key+'.jpg')).exists() or (MEDIA/key).exists() for key in SOURCES),'photos_total':len(SOURCES)}
class Handler(http.server.BaseHTTPRequestHandler):
    server_version='FatBearClean/4.0'
    def log_message(self,*args):pass
    def send(self,status,body,kind='application/json; charset=utf-8',cookie=None,cache='no-store'):
        data=body if isinstance(body,bytes) else json.dumps(body,separators=(',',':')).encode()
        try:
            self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control',cache);self.send_header('X-Content-Type-Options','nosniff')
            if cookie:self.send_header('Set-Cookie',cookie)
            self.end_headers();self.wfile.write(data)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError,OSError):pass
    def fail(self,code,message):self.send(code,{'error':message})
    def do_GET(self):
        path=urlsplit(self.path).path
        pages={'/':'index.html','/display':'display.html','/host':'display.html','/photos':'photos.html'}
        if path in pages:self.send(200,(BASE/pages[path]).read_bytes(),'text/html; charset=utf-8');return
        if path=='/style.css':self.send(200,(BASE/'style.css').read_bytes(),'text/css; charset=utf-8');return
        if path=='/api/profiles':self.send(200,PROFILES,cache='private, max-age=3600');return
        if path=='/api/state':
            with mutex:body=snapshot(person(self))
            self.send(200,body);return
        if path=='/join-qr.svg':
            host=self.headers.get('Host','')
            if not re.fullmatch(r'[A-Za-z0-9.:-]{1,253}',host):self.fail(400,'Invalid Host');return
            if host.split(':')[0] in ('localhost','127.0.0.1'):self.fail(400,'Open via iPhone Wi-Fi IP');return
            try:
                import segno
                output=io.BytesIO();segno.make_qr('http://'+host+'/').save(output,kind='svg',scale=8)
                self.send(200,output.getvalue(),'image/svg+xml')
            except ImportError:self.fail(503,'Segno missing: run sh setup.sh');return
            return
        if path.startswith('/media/'):
            key=path[7:-4] if path.endswith('.jpg') else path[7:]
            if key not in SOURCES:self.fail(404,'Unknown photo');return
            file=MEDIA/(key+'.jpg') if (MEDIA/(key+'.jpg')).exists() else (MEDIA/key if (MEDIA/key).exists() else MEDIA/(key+'.jpg'))
            if not file.exists():
                try:
                    req=urllib.request.Request(SOURCES[key],headers={'User-Agent':'Mozilla/5.0 FatBearFamily/4.0'})
                    with urllib.request.urlopen(req,timeout=10) as resp:
                        if not resp.headers.get('Content-Type','').lower().startswith('image/'):raise ValueError('not image')
                        data=resp.read(9000001)
                    if not 1000<len(data)<9000000:raise ValueError('bad image size')
                    file.write_bytes(data)
                except Exception:self.fail(404,'Source photo unavailable');return
            data=file.read_bytes();mime='image/png' if data.startswith(b'\x89PNG') else 'image/webp' if data.startswith(b'RIFF') else 'image/avif' if b'ftypavif' in data[:32] else 'image/jpeg'
            self.send(200,data,mime,cache='private, max-age=86400');return
        self.fail(404,'Not found')
    def do_POST(self):
        path=urlsplit(self.path).path
        if path not in ('/api/join','/api/vote'):self.fail(404,'Not found');return
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<1 or n>4096:raise ValueError()
            data=json.loads(self.rfile.read(n))
        except (ValueError,TypeError,json.JSONDecodeError):self.fail(400,'Invalid request');return
        with mutex:
            if path=='/api/join':
                name=str(data.get('name','')).strip()
                if not 1<=len(name)<=24 or any(ord(c)<32 for c in name):self.fail(400,'Name must be 1–24 characters');return
                if person(self):self.send(200,{'ok':True});return
                if state['started'] or len(state['players'])>=state['expected']:self.fail(409,'Room full');return
                pid=secrets.token_urlsafe(12);token=secrets.token_urlsafe(32);state['players'][pid]={'name':name,'token':token};revise();launch();save()
                self.send(200,{'ok':True},cookie='bear_player='+token+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=86400');return
            if path=='/api/vote':
                pid=person(self)
                if not pid or pid not in state['roster']:self.fail(401,'Join before the game starts');return
                i=state['cursor'];a,b=pair(i)
                if state['status'][i]!='open':self.fail(409,'Vote closed');return
                choice=str(data.get('choice',''))
                if choice not in (a,b):self.fail(400,'Invalid bear');return
                state['votes'].setdefault(str(i),{})[pid]=choice;revise();tick();save();self.send(200,{'ok':True});return
        self.fail(404,'Not found')
class Server(http.server.ThreadingHTTPServer):daemon_threads=True;allow_reuse_address=True
if __name__=='__main__':
    try:import segno
    except ImportError:print('WARNING: QR is unavailable. Run: sh setup.sh',flush=True)
    threading.Thread(target=timer,daemon=True).start()
    print('Bear game '+('resuming' if state['started'] else 'waiting for %s players'%state['expected']),flush=True)
    print('Guests: http://:%s/'%PORT,flush=True)
    print('Display: http://:%s/display'%PORT,flush=True)
    Server(('0.0.0.0',PORT),Handler).serve_forever()
