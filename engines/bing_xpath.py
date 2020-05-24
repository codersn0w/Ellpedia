# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re
from engines.google_xpath import g_search

def b_search(query, page, ua, g_urls, g_wikis):
  try:
    values = {
      'mkt': 'ja-JP',
      'q': query,
      'pq': query,
      'adlt': 'moderate',
    }
    offset = 10 * (page - 1) + 1
    s_url = 'https://www.bing.com/search?count=10&first=' + str(offset) + '&' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    base_xpath = root.xpath('//div[@id="b_content"]/main/ol[@id="b_results"]//li[@class="b_algo"]')
    title_xpath = './h2/a//text()'
    link_xpath = './h2/a/@href'
    descr_xpath = './div[contains(@class, "b_caption")]/p//text()'
    w_descr_xpath = './div[contains(@class, "b_caption")]/div[@class="b_snippet"]/p//text()'
    b_wikis = []
    b_top_results = []
    b_results = []
    rc = re.compile('http(s)?://(www.)?')
    i = 1
    for b in base_xpath:
      try:
        url = b.xpath(link_xpath)[0]
      except:
        break
      if rc.match(url):
        reurl = url.lstrip('http(s)?://(www.)?')
      else:
        reurl = url
      if reurl[-1:] == '/':
        reurl = reurl.rstrip('/')
      reurl = reurl.lower()
      if reurl not in g_urls: 
        ititle = b.xpath(title_xpath)
        title = ''.join(ititle)
        idescr = b.xpath(descr_xpath)
        descr=''.join(idescr)
        if len(url) > 60:
          d_url = url[:60] + '...'
        else:
          d_url = url
        if ('ja.wikipedia.org/wiki/' in url or 'en.wikipedia.org/wiki/' in url) and page == 1:
          wtitle = [g_wikis[w-1]['title'] for w in range(len(g_wikis))]
          if title not in wtitle:
            if b.xpath(w_descr_xpath):
              idescr = b.xpath(w_descr_xpath)
              descr = ''.join(idescr)
            b_wikis.append({
              'url': url,
              'd_url': d_url,
              'title': title,
              'descr': descr,
              })
        elif i <= 3:
          b_top_results.append({
            'url': url,
            'd_url': d_url,
            'title': title,
            'descr': descr,
            })
        else:
          b_results.append({
            'url': url,
            'd_url': d_url,
            'title': title,
            'descr': descr,
            })
      if i < 4:
        i+=1
    return b_wikis, b_top_results, b_results
  except:
    return [], [], []
