import json,sys,time,urllib.request,urllib.parse
UA={'User-Agent':'gap-search-script/1.0'}
def get(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=60) as r: return json.load(r)
def crossref(q,n=30):
    u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':q,'rows':n,'select':'DOI,title,container-title,issued,type'})
    d=get(u)['message']; time.sleep(4)
    return d['total-results'],[(i.get('title',[''])[0] if i.get('title') else '', i['DOI'], (i.get('issued',{}).get('date-parts') or [[None]])[0][0], (i.get('container-title') or [''])[0]) for i in d['items']]
def epmc(q,n=30,sort=None):
    p={'query':q,'format':'json','pageSize':n,'resultType':'lite'}
    if sort: p['sort']=sort
    u='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urllib.parse.urlencode(p)
    d=get(u); time.sleep(1)
    return d['hitCount'],[(i.get('title',''),i.get('doi',''),i.get('pubYear',''),i.get('journalTitle','')) for i in d.get('resultList',{}).get('result',[])]
def openalex(q,n=30,filt=None):
    p={'search':q,'per-page':n}
    if filt: p['filter']=filt
    u='https://api.openalex.org/works?'+urllib.parse.urlencode(p)
    d=get(u); time.sleep(1)
    return d['meta']['count'],[(i.get('title') or '',(i.get('doi') or '').replace('https://doi.org/',''),i.get('publication_year'),((i.get('primary_location') or {}).get('source') or {}).get('display_name','')) for i in d['results']]
def epmc_cited(q,n=30): return epmc(q,n,'CITED desc')
def openalex_title(q,n=30):
    # q = "TITLE||ABSTRACT" ; title.search and abstract.search filters, sorted by citations
    t,a=q.split('||'); f='title.search:'+t+(',abstract.search:'+a if a else '')
    u='https://api.openalex.org/works?'+urllib.parse.urlencode({'filter':f,'per-page':n,'sort':'cited_by_count:desc'})
    d=get(u); time.sleep(1)
    return d['meta']['count'],[(i.get('title') or '',(i.get('doi') or '').replace('https://doi.org/',''),i.get('publication_year'),((i.get('primary_location') or {}).get('source') or {}).get('display_name','')) for i in d['results']]
import xml.etree.ElementTree as ET
def arxiv(q,n=30):
    u='http://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':q,'max_results':n,'sortBy':'relevance'})
    req=urllib.request.Request(u,headers=UA)
    x=urllib.request.urlopen(req,timeout=60).read(); time.sleep(4)
    ns={'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
    r=ET.fromstring(x); cnt=r.find('o:totalResults',ns).text
    return cnt,[(' '.join(e.find('a:title',ns).text.split()),e.find('a:id',ns).text.split('/abs/')[-1],e.find('a:published',ns).text[:4],'arXiv') for e in r.findall('a:entry',ns)]
out=[]
for line in open(sys.argv[1]):
    line=line.rstrip('\n')
    if not line or line.startswith('#'): continue
    qid,src,q=line.split('\t',2)
    f={'crossref':crossref,'epmc':epmc,'epmc_cited':epmc_cited,'openalex':openalex,'openalex_title':openalex_title,'arxiv':arxiv}[src]
    try: cnt,items=f(q)
    except Exception as e: cnt,items=f'ERROR {e}',[]
    out.append({'id':qid,'source':src,'query':q,'count':cnt,'items':items})
    print(f'== {qid} [{src}] {q}\n   count={cnt}',flush=True)
    for k,(t,doi,y,j) in enumerate(items,1): print(f'   {k:2d}. {t[:150]} | {y} | {j[:40]} | {doi}')
json.dump(out,open(sys.argv[2],'w'),indent=1)
