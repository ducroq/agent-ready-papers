import json,sys,time,urllib.request,urllib.parse
UA={'User-Agent':'gap-search-script/1.0'}
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
for doi in sys.argv[1:]:
    try:
        m=get('https://api.crossref.org/works/'+urllib.parse.quote(doi))['message']
        au=m.get('author',[{}]); a=(au[0].get('family','') if au else '')+(' et al.' if len(au)>2 else (' & '+au[1].get('family','') if len(au)==2 else ''))
        y=(m.get('issued',{}).get('date-parts') or [[None]])[0][0]
        print(f"OK  {doi} | {a} {y} | {m.get('title',[''])[0][:110]} | {(m.get('container-title') or [''])[0][:50]} {m.get('volume','')}({m.get('issue','')}) {m.get('page','')}")
    except Exception as e: print(f"ERR {doi} | {e}")
    time.sleep(4)
