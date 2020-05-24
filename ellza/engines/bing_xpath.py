# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re
from engines.google_xpath import g_search

def b_search(query, ua, g_urls, g_wikis):
  try:
    values = {
      'mkt': 'ja-JP',
      'q': query,
      'pq': query,
      'adlt': 'strict',
    }
    s_url = 'https://www.bing.com/search?' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    base_xpath = root.xpath('//div[@id="b_content"]/ol[@id="b_results"]//li[@class="b_algo"]')
    title_xpath = './/h2/a//text()'
    link_xpath = './/h2/a/@href'
    descr_xpath = './div[contains(@class, "b_caption")]//p//text()'
    b_wikis = []
    b_top_results = []
    b_results = []
    rc = re.compile('http(s)?://(www.)?')
    i = 1
    for b in base_xpath:
      url = b.xpath(link_xpath)[0]
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

        if 'ja.wikipedia.org/wiki/' in url or 'en.wikipedia.org/wiki/' in url:
          wtitle = [g_wikis[w-1]['title'] for w in range(len(g_wikis))]
          if title not in wtitle:
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
      i+=1
	
    return b_wikis, b_top_results, b_results

  except:
    return [], [], []
