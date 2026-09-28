#!/usr/bin/env python3
from pathlib import Path
import urllib.request
from data import GRID,EXTRA
media=Path(__file__).resolve().parent/'media';media.mkdir(exist_ok=True)
sources={**GRID,**{'b'+id:url for id,(url,_,_) in EXTRA.items()}}
loaded=0
for key,url in sources.items():
    path=media/(key+'.jpg')
    if path.exists() and path.stat().st_size>=1000:
        loaded+=1;print(key,'cached');continue
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 FatBearFamily/4.0'})
        with urllib.request.urlopen(req,timeout=12) as r:
            if not r.headers.get('Content-Type','').lower().startswith('image/'):raise ValueError('response is not image')
            content=r.read(9000001)
        if not 1000<len(content)<9000000:raise ValueError('image size invalid')
        path.write_bytes(content);loaded+=1;print(key,'downloaded',len(content),'bytes')
    except Exception as e:print(key,'MISSING:',str(e)[:150])
print('Cached',loaded,'/',len(sources),'source photos.')
