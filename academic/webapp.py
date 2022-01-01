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
from engines.gs_xpath import gs_search
from engines.cr_xpath import cr_search
from engines.ar_xpath import ar_search
from engines.ci_xpath import ci_search
from concurrent.futures import ThreadPoolExecutor
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
  if request.method == 'GET':
    if request.args.get('q'):
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
  else:
    query = request.form['q']
    if int(request.form['p']) < 1 or int(request.form['p']) > 20:
      page = 1
    else:
      page = int(request.form['p'])
  if len(query) > 70:
      query = query[:70]
  ua = generate_ua()
  results=[]
  with ThreadPoolExecutor(max_workers=10) as executor:
    gs = gs_search(query, page, ua)
    cr = cr_search(query, page, ua)
    ar = ar_search(query, page)
    ci = ci_search(query, page, ua)
  results = gs[0]+cr[0]+ar[0]+ci[0]
  get_url = "http://localhost:50002/search?" + up.urlencode({'q': query, 'p': page})
  if page == 1:
    page_back = 1
    page_next = 2
  elif page == 20:
    page_back = 19
    page_next = 1
  else:
    page_back = page - 1
    page_next = page + 1
  if gs == ([],[]) and cr == ([],[]) and ar == ([],[]) and ci == ([],[]):
  	no_result = {
    'url': '/',
    'descr': 'No Result',
    'top': 'Back to main page',
    }
  else:
    no_result = {}
  return render_template('search.html',
                         query = query,
                         no_result = no_result,
                         results = results,
                         get_url = get_url,
                         page_back = page_back,
                         page_next = page_next,
                         )

app.run(port=50002, debug=False)
