# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re
def ar_search(query, page):
  try:
    values = {
      'search_query': query,
    }
    offset = 10 * (page - 1)
    s_url = 'http://export.arxiv.org/api/query?start=' + str(offset) + '&max_results=10&' + up.urlencode(values)
    res = req.urlopen(s_url).read()
    root = lh.fromstring(res)
    base_xpath = root.xpath('.//entry')
    title_xpath = './/title/text()'
    link_xpath = './/id/text()'
    descr_xpath = './/summary/text()'
    a_urls = []
    ar_results = []
    rc = re.compile('http(s)?://(www.)?')
    for a in base_xpath:
      title = a.xpath(title_xpath)[0]
      url = a.xpath(link_xpath)[0]
      if rc.match(url):
        reurl = url.lstrip('http(s)?://(www.)?')
      else:
        reurl = url
      if reurl[-1:] == '/':
        reurl = reurl.rstrip('/')
      reurl = reurl.lower()
      a_urls.append(reurl)
      descr = a.xpath(descr_xpath)[0].replace('\n', ' ').strip()
      if len(url) > 60:
        d_url = url[:60] + '...'
      else:
        d_url = url
      if len(descr) > 250:
        descr = descr[:250] + '...'
      ar_results.append({
        'url': url,
        'd_url': d_url,
        'title': title,
        'descr': descr,
        'engine': 'arXiv',
        })
    return ar_results, a_urls
  except:
    return [], []
