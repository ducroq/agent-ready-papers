import re,sys,html
t=open(sys.argv[1],errors='replace').read()
titles=re.findall(r'<h3[^>]*class="[^"]*"[^>]*>\s*<a[^>]*>(.*?)</a>',t,flags=re.S) or re.findall(r'<a href="https://www.equator-network.org/reporting-guidelines/[^"]+"[^>]*>(.*?)</a>',t,flags=re.S)
nf='Nothing Found' in t
titles=[html.unescape(re.sub(r'<[^>]+>|\s+',' ',x)).strip() for x in titles]
print('NOTHING_FOUND' if nf else f'{len(titles)} titles')
for x in dict.fromkeys(titles): print('  -',x[:160])
