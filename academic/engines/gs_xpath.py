# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re

def gs_search(query, page, ua):
  try:
    values = {
      'q': query,
    }
    offset = 10 * (page - 1)
    s_url = 'https://scholar.google.co.jp/scholar?hl=ja&start=' + str(offset) + '&num=10&' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    base_xpath = root.xpath('.//div[@class="gs_ri"]')
    title_xpath = './h3[@class="gs_rt"]/a//text()'
    link_xpath = './h3[@class="gs_rt"]/a/@href'
    descr_xpath = './div[@class="gs_rs"]//text()'
    g_urls = []
    gs_results = []
    rc = re.compile('http(s)?://(www.)?')
    for g in base_xpath:
      ititle = g.xpath(title_xpath)
      title = ''.join(ititle)
      if g.xpath(link_xpath):
        url = g.xpath(link_xpath)[0]
      else:
        continue
      if rc.match(url):
        reurl = url.lstrip('http(s)?://(www.)?')
      else:
        reurl = url
      if reurl[-1:] == '/':
        reurl = reurl.rstrip('/')
      reurl = reurl.lower()
      g_urls.append(reurl)
      idescr = g.xpath(descr_xpath)
      descr = ''.join(idescr)
      if len(url) > 60:
        d_url = url[:60] + '...'
      else:
        d_url = url
      gs_results.append({
        'url': url,
        'd_url': d_url,
        'title': title,
        'descr': descr,
        'engine': 'Google Scholar',
        })
    return gs_results, g_urls
  except:
    return [], []
