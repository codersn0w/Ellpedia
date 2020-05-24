# coding: utf-8
'''
Ellpedia is released under the AGPL-3.0 Licence.
See the LICENCE file.
(C) ThunderRa1n, <podsn0w@gmail.com>
'''
from flask import Flask, render_template, request
import urllib.parse as up
import re
from engines.random_ua import generate_ua
from engines.google_xpath import g_search
from engines.bing_xpath import b_search
from engines.bnews_xpath import bn_search
from engines.gimage_xpath import gi_search
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
  spel = 0
  if request.method == 'GET':
    if request.args.get('q') and request.args.get('q') != 'i:':
      query = request.args.get('q')
    else:
      return render_template('index.html')
    if request.args.get('p'):
      if int(request.args.get('p')) < 1 or int(request.args.get('p')) > 20:
        page = 1
      else:
        page = int(request.args.get('p'))
    else:
      page = 1
    if request.args.get('spl') and request.args.get('spl') =='1':
      spel = 1
  else:
    query = request.form['q']
    if int(request.form['p']) < 1 or int(request.form['p']) > 20:
      page = 1
    else:
      page = int(request.form['p'])
    if query == 'i:':
      return render_template('index.html')
    if request.form['spl']=="1":
      spel = 1
  if len(query) > 70:
    query = query[:70]
  top_n = 0
  top_i = 0
  top_nw = 0
  top_iw = 0
  no_ggl1 = 0
  if re.match('n:', query):
    query = query.lstrip('n:')
    top_n = 1
  if re.match('i:', query):
    query = query.lstrip('i:')
    top_i = 1
  if page == 1:
    im_word = ['logo', 'icon', 'wallpaper', 'image', '壁紙', '背景', '画像', 'アイコン', 'ロゴ', '写真', 'パノラマ', '風景', '夜景', '景色', 'スクショ', 'スクリーンショット', '画面']
    if 'news' in query.lower() or 'ニュース' in query:
      top_nw = 1
    for i in im_word:
      if i in query.lower():
        top_iw = 1
        break
  ua = generate_ua()
  ggl = g_search(query, page, spel, ua)
  spell = ggl[4]
  orig = ggl[5]
  g_wikis = ggl[0]
  g_urls = ggl[3]
  bng = b_search(query, page, ua, g_urls, g_wikis)
  wiki_results = ggl[0] + bng[0]
  if len(wiki_results)<=1 and len(ggl[1])<=1:
    top_results = ggl[1] + bng[1]
    no_ggl1 = 1
  else:
    top_results = ggl[1]
  if len(wiki_results) >= 3:
    if len(top_results) == 0:
      sec_wiki = wiki_results[3:]
      wiki_results = wiki_results[:3]
    else:
      sec_wiki = wiki_results[2:]
      wiki_results = wiki_results[:2]
  else:
    sec_wiki = []
  if page == 1:
    b_news = bn_search(query, ua)
    notif = int(len(b_news))
  else:
    b_news = []
    notif = 0
  if no_ggl1 == 1:
    if sec_wiki != []:
      g_results = sec_wiki + ggl[2]
    else:
      g_results = ggl[2]
  else:
    if sec_wiki != []:
      g_results = sec_wiki + bng[1] + ggl[2]
    else:
      g_results = bng[1] + ggl[2]
  if page == 1:
    im_results = gi_search(query, ua)
  else:
    im_results = []
  b_results = bng[2]
  if top_n == 1:
    query = 'n:' + query
  if top_i == 1:
    query = 'i:' + query
  if top_nw == 1:
    top_n = 1
  if top_iw == 1:
    top_i = 1
  get_url = "http://localhost:50000/search?" + up.urlencode({'q': query, 'p': page})
  if page == 1:
    page_back = 1
    page_next = 2
  elif page == 20:
    page_back = 19
    page_next = 1
  else:
    page_back = page - 1
    page_next = page + 1
  if spel == 1:
    get_url = get_url + "&spl=1"
  sug = ggl[6]
  if ggl == ([],[],[],[],'','', []) and bng == ([],[],[]):
  	no_result = {
    'url': '/',
    'descr': '表示結果なし(データ取得エラー)',
    'top': 'TOPへ',
    }
  else:
    no_result = {}
  return render_template('search.html',
                         query = query,
                         spell = spell,
                         orig = orig,
                         top_n = top_n,
                         top_i = top_i,
                         no_result = no_result,
                         wiki_results = wiki_results,
  	                     top_results = top_results,
  	                     b_news = b_news,
  	                     notif = notif,
  	                     g_results = g_results,
  	                     im_results = im_results,
  	                     b_results = b_results,
                         get_url = get_url,
                         page_back = page_back,
                         page_next = page_next,
                         sug = sug,
                         )

app.run(port=50000, debug=False)
