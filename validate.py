#!/usr/bin/env python3
"""Validate generated pages, metadata, catalog coverage and local shell links."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent/'site'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
files=[ROOT/'index.html',*ROOT.glob('game/*/index.html'),*ROOT.glob('category/*/index.html'),ROOT/'all-games/index.html',ROOT/'search/index.html']
errors=[];missing_games=[];titles=[];descriptions=[];ifs=[]
for file in files:
 p=Page();text=file.read_text();p.feed(text); tags=p.tags
 for name,test in [('title','<title>' in text),('canonical',any(t=='link' and a.get('rel')=='canonical' for t,a in tags)),('description',any(t=='meta' and a.get('name')=='description' for t,a in tags)),('h1',sum(t=='h1' for t,a in tags)==1),('og',any(a.get('property')=='og:title' for t,a in tags)),('twitter',any(a.get('name')=='twitter:card' for t,a in tags)),('analytics',any(a.get('src')=='/assets/analytics.js' for t,a in tags))]:
  if not test:errors.append(str(file.relative_to(ROOT))+': '+name)
 titles.append(text.split('<title>')[1].split('</title>')[0]);descriptions.extend(a['content'] for t,a in tags if t=='meta' and a.get('name')=='description')
 for t,a in tags:
  url=a.get('href') if t in ('a','link') else a.get('src') if t in ('img','script','iframe') else None
  if not url or not url.startswith('/') or url.startswith('//'):continue
  path=unquote(urlsplit(url).path)
  if path.startswith('/games/'):
   ifs.append(url)
   if not (ROOT/path.lstrip('/')).exists():missing_games.append(url)
   continue
  dest=ROOT/path.lstrip('/');dest=dest/'index.html' if path.endswith('/') else dest
  if not dest.exists():errors.append(str(file.relative_to(ROOT))+': missing '+url)
 if '/game/' in str(file):
  if sum(t=='iframe' for t,a in tags)!=1:errors.append(str(file)+': iframe count')
  if sum('data-ad-slot' in a for t,a in tags)!=5:errors.append(str(file)+': ad slot count')
 if any(a.get('role')=='dialog' or 'data-modal' in a for t,a in tags):errors.append(str(file)+': modal')
urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
result={'html_pages':len(files),'game_pages':len(list(ROOT.glob('game/*/index.html'))),'category_pages':len(list(ROOT.glob('category/*/index.html'))),'sitemap_urls':len(urls),'unique_titles':len(set(titles)),'unique_descriptions':len(set(descriptions)),'iframe_paths':len(ifs),'shell_errors':len(errors),'missing_original_game_files':len(missing_games),'errors':errors[:30],'note':'Missing original games are a deployment dependency, NOT replaced with placeholders. Game loads remain unverified.'}
(ROOT.parent/'VALIDATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if errors:raise SystemExit(1)
