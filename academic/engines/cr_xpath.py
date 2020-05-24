# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re

def cr_search(query, page, ua):
  try:
    values = {
      'q': query,
      'page': page,
    }
    s_url = 'https://search.crossref.org/?' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    base_xpath = root.xpath('..//tr')
    title_xpath = './td/p[@class="lead"]/text()'
    link_xpath = './td/div[@class="item-links-outer"]/div[@class="item-links"]/a/@href'
    descr_xpath = './td/p[@class="extra"]//text()'
    cr_urls = []
    cr_results = []
    rc = re.compile('http(s)?://(www.)?')
    for c in base_xpath:
      title = c.xpath(title_xpath)[0].lstrip('\n').rstrip('\n')
      url = c.xpath(link_xpath)[0]
      if title == '':
        title = url
      if rc.match(url):
        reurl = url.lstrip('http(s)?://(www.)?')
      else:
        reurl = url
      if reurl[-1:] == '/':
        reurl = reurl.rstrip('/')
      reurl = reurl.lower()
      cr_urls.append(reurl)
      idescr = c.xpath(descr_xpath)
      descr = ''.join(idescr).replace('\n', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').lstrip(' ').rstrip(' ')
      if len(url) > 60:
        d_url = url[:60] + '...'
      else:
        d_url = url
      cr_results.append({
        'url': url,
        'd_url': d_url,
        'title': title,
        'descr': descr,
        'engine': 'CrossRef'
        })
    return cr_results, cr_urls
  except:
    return [], []