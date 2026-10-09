#!/usr/bin/env python3
# 静态新闻生成与本机编辑服务，无第三方运行依赖。
import argparse, datetime as dt, html, json, re, posixpath
import yaml
from markdown_it import MarkdownIt
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = 'https://guide.bubbpackage.com'
CATEGORIES = ['公司新闻', '行业动态', '知识文章']
CATEGORY_DIRS = dict(zip(['company', 'industry', 'knowledge'], CATEGORIES))
PUBLIC = ROOT / 'news/articles-data.json'

def today():
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date().isoformat()

def load():
    posts=[]
    for file in sorted((ROOT/'articles').rglob('*.md')):
        if file.name.startswith('_') or file.name=='README.md':continue
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',file.stem):
            raise ValueError(f'{file.name}: 文件名请使用小写英文、数字和中划线')
        raw=file.read_text(encoding='utf-8-sig').replace('\r\n','\n')
        match=re.match(r'\A---\n(.*?)\n---(?:\n|$)(.*)\Z',raw,re.S)
        if not match:raise ValueError(f'{file.name}: 缺少开头的文章信息区')
        info=yaml.safe_load(match[1])
        if not isinstance(info,dict):raise ValueError(f'{file.name}: 文章信息格式错误')
        for key in ['title','date','category','summary']:
            if key not in info or not str(info[key]).strip():raise ValueError(f'{file.name}: 请填写 {key}')
        if not isinstance(info.get('published',True),bool):raise ValueError(f'{file.name}: published 必须为 true 或 false')
        info['category'] = CATEGORY_DIRS.get(file.parent.name, info.get('category'))
        if info['category'] == '包装知识': info['category'] = '知识文章'
        posts.append({**info,'slug':file.stem,'body':match[2].strip(),'status':'published' if info.get('published',True) else 'draft','cover':info.get('cover','')})
    return posts

def validate(posts):
    if not isinstance(posts, list) or len(posts) > 500:
        raise ValueError('文章数量必须在 0–500 之间。')
    slugs = set()
    result = []
    for post in posts:
        if not isinstance(post, dict):
            raise ValueError('文章格式错误。')
        item = {key: str(post.get(key, '')).strip() for key in ['slug', 'title', 'category', 'date', 'summary', 'body', 'cover', 'status']}
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item['slug']) or len(item['slug']) > 80:
            raise ValueError('网址名称请用小写英文字母、数字及中划线，最多 80 个字符。')
        if item['slug'] in CATEGORY_DIRS or item['slug'] in slugs:
            raise ValueError('文章网址名称重复：' + item['slug'])
        slugs.add(item['slug'])
        if not 1 <= len(item['title']) <= 100 or len(item['summary']) > 300 or len(item['body']) > 100000:
            raise ValueError('请填写标题（最多100字）；摘要最多300字，正文最多100000字。')
        if item['category'] not in CATEGORIES or item['status'] not in ['draft', 'published']:
            raise ValueError('文章分类或状态无效。')
        dt.date.fromisoformat(item['date'])
        if item['date'] > today() and item['status'] == 'published':
            raise ValueError('未来日期的文章请保存为草稿；当前不支持定时发布。')
        if item['status'] == 'published' and not item['body']:
            raise ValueError('发布文章需要填写正文。')
        if item['cover']:
            url = urlparse(item['cover'])
            if url.scheme != 'https' or not url.netloc or url.username or url.password:
                raise ValueError('封面请填写 https 图片地址，或留空。')
        result.append(item)
    return result

def escape(value):
    return html.escape(value, quote=True)

def body_html(body):
    return MarkdownIt('commonmark', {'html': False}).enable('table').render(body)

def page(title, description, path, content, schema=None):
    structured = '' if not schema else '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script>'
    document = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}｜印个泡泡</title><meta name="description" content="{escape(description)}"><link rel="canonical" href="{DOMAIN}{path}"><link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/news.css">{structured}</head><body><header class="site-header compact-header"><a class="brand" href="/"><img class="logo-mark" src="/assets/logo.png" alt="印个泡泡"><span><strong>印个泡泡</strong><small>新闻与包装知识</small></span></a><a class="back-home" href="https://bubbpackage.com/">返回包装平台 →</a></header><main class="news-main">{content}</main><footer class="site-footer"><div><strong>印个泡泡</strong><span>包装定制指南 · 新闻与文章</span></div><a href="/">浏览行业指南 →</a></footer></body></html>'''


    # Explicit relative files work both on GitHub Pages and when opened locally.
    def local_link(match):
        attribute, target = match.groups()
        clean, separator, fragment = target.partition('#')
        if clean.endswith('/'): clean += 'index.html'
        relative = posixpath.relpath(clean, path)
        return attribute + '="' + relative + (separator + fragment if separator else '') + '"'
    return re.sub(r'(href|src)="(/[^"\s]*)"', local_link, document)


def article(post, preview=False):
    label = '<p class="draft-note">草稿预览，尚未上线</p>' if preview else ''
    cover = '<img class="news-cover" src="' + escape(post['cover']) + '" alt="' + escape(post['title']) + '">' if post['cover'] else ''
    content = f'''<a class="news-back" href="/news/">← 新闻与文章</a>{label}<article class="news-article"><p class="eyebrow">{escape(post['category'])}</p><h1>{escape(post['title'])}</h1><p class="news-date">{escape(post['date'])} · 印个泡泡</p><p class="news-lead">{escape(post['summary'])}</p>{cover}<div class="news-body">{body_html(post['body'])}</div><div class="news-cta"><p>为你的产品，找到适合的包装。</p><a class="primary-cta" href="https://bubbpackage.com/product">选包装，获取报价 →</a></div></article>'''
    schema = {'@context': 'https://schema.org', '@type': 'Article', 'headline': post['title'], 'description': post['summary'], 'datePublished': post['date'], 'author': {'@type': 'Organization', 'name': '印个泡泡'}, 'mainEntityOfPage': DOMAIN + '/news/' + post['slug'] + '/'}
    return page(post['title'], post['summary'], '/news/' + post['slug'] + '/', content, schema)

def build(posts=None):
    posts = validate(load() if posts is None else posts)
    published = sorted((p for p in posts if p['status'] == 'published'), key=lambda p: (p['date'], p['slug']), reverse=True)
    PUBLIC.parent.mkdir(exist_ok=True)
    PUBLIC.write_text(json.dumps([{k: p[k] for k in ['slug', 'title', 'category', 'date', 'summary', 'cover']} for p in published], ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    news = ROOT / 'news'; news.mkdir(exist_ok=True)
    previous_manifest = news / 'generated-articles.json'
    previous = json.loads(previous_manifest.read_text()) if previous_manifest.exists() else [p.stem for p in (ROOT/'articles').rglob('*.md') if not p.name.startswith('_') and p.name!='README.md']
    slugs = [p['slug'] for p in published]
    for slug in previous:
        if slug not in slugs and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            file = news / slug / 'index.html'
            if file.exists(): file.unlink()
            folder = news / slug
            if folder.exists() and not any(folder.iterdir()): folder.rmdir()
    for post in published:
        folder = news / post['slug']; folder.mkdir(exist_ok=True)
        (folder / 'index.html').write_text(article(post), encoding='utf-8', newline='\n')
    previous_manifest.write_text(json.dumps(slugs) + '\n', encoding='utf-8', newline='\n')
    groups = ''
    for category in CATEGORIES:
        cards = ''.join(f'''<a class="news-card" href="/news/{p['slug']}/"><time>{escape(p['date'])}</time><h3>{escape(p['title'])}</h3><p>{escape(p['summary'])}</p><span>阅读文章 →</span></a>''' for p in published if p['category'] == category)
        groups += f'<section class="news-group" id="{dict(zip(CATEGORIES, ["company", "industry", "knowledge"]))[category]}"><h2>{category}</h2><div class="news-grid">{cards or "<p class=\"news-empty\">暂无更新，欢迎先浏览下方包装指南。</p>"}</div></section>'
    content = '<p class="eyebrow">NEWS & ARTICLES</p><h1>新闻与文章</h1><p class="news-lead">平台动态、行业资讯与包装知识，在这里持续更新。</p><nav class="news-tabs"><a href="/news/company/">公司新闻</a><a href="/news/industry/">行业动态</a><a href="/news/knowledge/">知识文章</a><a href="/">全部包装指南 →</a></nav>' + groups + '<section class="news-group"><h2>先从包装指南开始</h2><div class="news-grid"><a class="news-card" href="/xiaopiliang-baozhuang-dingzhi/"><h3>小批量包装定制指南</h3><p>从试样到选材，了解包装定制的基本流程。</p><span>阅读指南 →</span></a><a class="news-card" href="/coffee-bean-packaging/"><h3>咖啡豆包装指南</h3><p>了解袋型、材料与品牌包装设计。</p><span>阅读指南 →</span></a><a class="news-card" href="/food-beverage/"><h3>食品饮料包装指南</h3><p>根据产品需求选择包装结构和材料。</p><span>阅读指南 →</span></a></div></section>'
    (news / 'index.html').write_text(page('新闻与文章', '印个泡泡公司新闻、行业动态与包装知识文章。', '/news/', content), encoding='utf-8', newline='\n')
    for directory, category in CATEGORY_DIRS.items():
        folder = news / directory; folder.mkdir(exist_ok=True)
        cards = ''.join(f'<a class="news-card" href="/news/{p["slug"]}/"><time>{escape(p["date"])}</time><h3>{escape(p["title"])}</h3><p>{escape(p["summary"])}</p><span>阅读文章 →</span></a>' for p in published if p['category'] == category)
        content = '<a class="news-back" href="/news/">← 全部新闻与文章</a><h1>' + category + '</h1><div class="news-grid">' + (cards or '<p class="news-empty">暂无文章，发布后将在这里自动展示。</p>') + '</div>'
        (folder / 'index.html').write_text(page(category, category + '最新文章', '/news/' + directory + '/', content), encoding='utf-8', newline='\n')
    feed = [{k: p[k] for k in ['slug', 'title', 'category', 'date', 'summary', 'cover']} for p in published]
    (news / 'feed.json').write_text(json.dumps(feed, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    (news / 'feed.js').write_text('window.BubbNews=' + json.dumps(feed, ensure_ascii=False).replace('<', '\\u003c') + ';\n', encoding='utf-8', newline='\n')
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'; ET.register_namespace('', ns)
    sitemap = ROOT / 'sitemap.xml'; tree = ET.parse(sitemap); base = tree.getroot()
    for entry in list(base):
        loc = entry.find('{' + ns + '}loc')
        if loc is not None and (loc.text or '').startswith(DOMAIN + '/news/'):
            base.remove(entry)
    for path in ['/news/'] + ['/news/' + d + '/' for d in CATEGORY_DIRS] + ['/news/' + p['slug'] + '/' for p in published]:
        item = ET.SubElement(base, '{' + ns + '}url')
        ET.SubElement(item, '{' + ns + '}loc').text = DOMAIN + path
        ET.SubElement(item, '{' + ns + '}lastmod').text = today()
    ET.indent(tree); sitemap.write_bytes(ET.tostring(base, encoding='utf-8', xml_declaration=True))
    return len(published)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['build'])
    parser.parse_args()
    print('Generated', build(), 'published articles.')
