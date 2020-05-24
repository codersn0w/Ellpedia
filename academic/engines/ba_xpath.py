# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re

def ba_search(query, ua):
  try:
    values = {
      'lookfor': query,
    }
    s_url = 'https://www.base-search.net/Search/Results?type=all&ling=1&oaboost=1&name=&thes=&refid=dcresen&newsearch=1&' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    base_xpath = root.xpath('.//div[contains(@class, "record-panel")]')
    title_xpath = './div[@class="panel-heading"]/div/div[@class="col-xs-11" or @class="col-xs-12"]/a/text()'
    link_xpath = './div[@class="panel-heading"]/div/div[@class="col-xs-11" or @class="col-xs-12"]/a/@href'
    descr_xpath1 = './div[@class="panel-body"]/div[contains(@class, "row")][1]/div[contains(@class, "col-sm-9")]/text()'
    descr_xpath2 = './div[@class="panel-body"]/div[contains(@class, "row")][2]/div[contains(@class, "col-sm-9")]/text()'
    panel_xpath5 = './div[@class="panel-body"]/div[contains(@class, "row")][5]'
    descr_xpathd = './div[@class="panel-body"]/div[contains(@class, "row")][1]/div[contains(@class, "col-sm-3")]/text()'
    ba_urls = []
    ba_results = []
    rc = re.compile('http(s)?://(www.)?')
    rn = re.compile(r'^[0-9]+\.')
    for b in base_xpath:
      title = b.xpath(title_xpath)[0]
      if rn.match(title):
        title = re.sub(r'^[0-9]+\.', '', title)
      url = b.xpath(link_xpath)[0]
      if rc.match(url):
        reurl = url.lstrip('http(s)?://(www.)?')
      else:
        reurl = url
      if reurl[-1:] == '/':
        reurl = reurl.rstrip('/')
      reurl = reurl.lower()
      ba_urls.append(reurl)
      if b.xpath(panel_xpath5):
        idescr=b.xpath(descr_xpath2)
      else:
        if b.xpath(descr_xpathd)[0] == 'Description:':
          idescr=b.xpath(descr_xpath1)
        else:
          idescr=[]
      descr = ''.join(idescr).replace('\n', '').replace('\r', '').replace('\t', '').rstrip()
      if len(url) > 60:
        d_url = url[:60] + '...'
      else:
        d_url = url
      ba_results.append({
        'url': url,
        'd_url': d_url,
        'title': title,
        'descr': descr,
        })
    return ba_results, ba_urls
  except:
    return [], []