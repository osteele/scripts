# TODO
# [ ] remove url from internal links
# [ ] attached files
# [ ] check the missing pages
# [ ] jekyll

import datetime
import os
import re
import urllib

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

#%%

## Configuration

VERBOSE = True
RECURSE = False

site_url = 'https://sites.google.com/site/sd16spring/home/'
site_url = 'https://sites.google.com/site/sd16fall/assignments-and-mini-projects/setup-your-environment'
blacklist = [r'.*/system/.*', r'.*/last-year-in-class/.*']

output_dir = '/Users/osteele/sites/sd17spring.d'

menu_names = {'in-class-exercises': 'Day',
              'assignments-and-mini-projects': 'Assignments',
              'project-toolbox': 'Toolboxes',
              'project': 'Project',
              'homeworks': 'Homework'
              }

#%%

unvisited_links = {site_url}  # {url}
visited_links   = set()  # {url}
redirections    = dict()  # {url: url}
pages           = dict()  # {path: soup}
media_pages     = dict()  # {url: content-type}
error_links     = dict()  # {url: error_code}
last_modified   = dict()

while unvisited_links:
    u = unvisited_links.pop()
    if any(re.match(r, u) for r in blacklist):
        print('blacklisted; skipping', u)
        continue

    if VERBOSE: print('visiting', u, ';', len(unvisited_links), 'remaining')

    r = requests.head(u, allow_redirects=True)

    visited_links |= set(h.url for h in [r] + r.history)
    page_url = ([r] + r.history)[-1].url.split('?')[0]
    redirections.update((h.url, page_url) for h in r.history if h.url != page_url)
    page_path = page_url[len(site_url):] if page_url.startswith(site_url) else page_url

    if not 200 <= r.status_code <= 299:
        error_links[page_path] = r.status_code
        print('  {}: error code = {}; skipping'.format(u, r.status_code))
        continue

    content_type = r.headers['Content-Type'].split(';')[0]
    if content_type != 'text/html':
        media_pages[page_path] = content_type
        if VERBOSE: print('  {}: content type = {}; skipping'.format(u, content_type))
        continue

    r = requests.get(u)
    assert 200 <= r.status_code <= 299

    html = BeautifulSoup(r.text, 'lxml')
    if not html.body:
        print('  missing body: {}; skipping'.format(u))
        continue

    pages[page_path] = html
    last_modified[page_path] = datetime.datetime.strptime(r.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S GMT')

    if RECURSE:
        outgoing_links = {urllib.parse.urljoin(page_url, e.attrs['href']).split('#')[0].split('?')[0]
                          for e in html.body.find_all('a')
                          if 'href' in e.attrs}
        internal_links = {u for u in outgoing_links if u.startswith(site_url)}
        unvisited_internal_links = internal_links - visited_links - unvisited_links
        if unvisited_internal_links:
            unvisited_links |= unvisited_internal_links
            if VERBOSE: print('  adding', len(unvisited_internal_links), '/', len(internal_links), 'links')

print('visited', len(visited_links), 'links; retrieved', len(pages))


#%%
## Write media files

for rel_path in media_pages.keys():
    dst_path = os.path.join(output_dir, 'static', rel_path)
    os.makedirs(os.path.split(dst_path)[0], exist_ok=True)
    r = requests.get(urllib.parse.urljoin(site_url, rel_path), stream=True)
    with open(dst_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=4096):
            fd.write(chunk)
#%%

site_title_suffix = '- ' + ''.join(map(str, pages[''].head.title)); site_title_suffix

def extract_title(html):
    title = ''.join(map(str, html.head.title)).strip() if html.head and html.head.title else ''
    if title.endswith(site_title_suffix):
        title = title[:-len(site_title_suffix)].strip()
    return title

#%%


# u = 'https://sites.google.com/site/sd16spring/github-help'
# r = requests.get(u)
# pages = {u: BeautifulSoup(r.text, 'lxml')}
# last_modified = {u: datetime.datetime.strptime(r.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S GMT')}

for page_path, html in sorted(list(pages.items())):
    elts = html.body.find_all(None, {'class': 'sites-layout-tile'})
    if not elts:
        print('missing layout; skipping', page_path)
        continue
    if len(elts) > 1:
        print('multiple layouts:', page_path)

    title = ''.join(map(str, html.head.title)).strip() if html.head and html.head.title else ''
    if title.endswith(site_title_suffix):
        title = title[:-len(site_title_suffix)].strip()

    for e in elts[0].find_all('a'):
        if e.attrs.get('href', '').startswith(site_url):
            e.attrs['href'] = '/' + e.attrs['href'][len(site_url):]
    md = html2text.html2text(''.join(map(str, elts[0])))
    md = re.sub(r'\*\*\s*([^\*]+?)\s*\*\*', r'**\1** ', md)
    md = re.sub(r'_([^\*]+?)\s*_', r'_\1_ ', md)

    frontmatter = {
        'date': last_modified[page_path].isoformat(),
        'description': '',
        'title': title,
    }
    if page_path and len(page_path.split('/')) == 1:
        frontmatter['menu'] = 'main'
    elif len(page_path.split('/')) == 2:
        cat_name = menu_names.get(menu_names[page_path.split('/')[0]], extract_title(pages[page_path.split('/')[0]]))
        frontmatter['menu'] = {'main': {'parent': cat_name}}

    is_index = not page_path or any(other_path.startswith(page_path + '/') for other_path in pages.keys())
    output_rel_path = os.path.join(page_path, 'index.md') if is_index else page_path + '.md'
    if is_index:
        frontmatter['type'] = 'index'

    output_path = os.path.join(output_dir, 'content', output_rel_path)
    if VERBOSE: print(page_path, title, '->', output_path)
    os.makedirs(os.path.split(output_path)[0], exist_ok=True)
    with open(output_path, 'w') as fd:
        fd.write('---\n')
        yaml.dump(frontmatter, fd, default_flow_style=False)
        fd.write('---\n\n')
        fd.write(md)

print('done')

#%%
