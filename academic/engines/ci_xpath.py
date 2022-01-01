# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re
from flask import Markup

def ci_search(query, page, ua):
  try:
    start = 10 * (page - 1) + 1
    values = {
      'q': query,
      'range': '0',
      'sortorder': '1',
      'count': '10',
      'start': start,
    }
    s_url = 'https://ci.nii.ac.jp/search?' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    base_xpath = root.xpath('.//div[@id="itemlistbox"]/ul//li')
    title_xpath1 = './div/dl/dt/a/text()'
    title_xpath2 = './div/dl/dt/a/span/text()'
    title_xpath3 = './div/dl/dt/a/span/following-sibling::text()'
    link_xpath = './div/dl/dt/a//@href'
    #author_xpath = './div/dl/dd/p[@class="item_subData item_authordata"]//text()' 
    descr_xpath1 = './div/dl/dd/p[@class="item_extraData item_journaldata"]/span//text()'
    descr_xpath2 = './div/dl/dd/p[@class="item_extraData item_journaldata"]/span/span/text()'
    descr_xpath3 = './div/dl/dd/p[@class="item_extraData item_journaldata"]/span/span/following-sibling::text()'
    ci_urls = []
    ci_results = []
    rc = re.compile('http(s)?://(www.)?')
    for c in base_xpath:
      try:
        title1 = c.xpath(title_xpath1)[0].strip()
      except:
        title1 = ''
      try:
        title2 = ' ' + c.xpath(title_xpath2)[0].strip() + ' '
      except:
        title2 = ''
      try:
        title3 = c.xpath(title_xpath3)[0].strip()
      except:
        title3 = ''
      title = title1 +  title2 + title3
      url = 'https://ci.nii.ac.jp' + c.xpath(link_xpath)[0]
      if rc.match(url):
        reurl = url.lstrip('http(s)?://(www.)?')
      else:
        reurl = url
      if reurl[-1:] == '/':
        reurl = reurl.rstrip('/')
      reurl = reurl.lower()
      ci_urls.append(reurl)
      #author = c.xpath(author_xpath)[0]
      try:
        descr1 = c.xpath(descr_xpath1)[0]
      except:
        descr1 = ''
      try:
        descr2 = ' ' + c.xpath(descr_xpath2)[0]
      except:
        descr2 = ''
      try:
        descr3 = c.xpath(descr_xpath3)[0]
      except:
        descr3 = ''
      descr = descr1 +  descr2 + descr3
      if len(url) > 60:
        d_url = url[:60] + '...'
      else:
        d_url = url
      ci_results.append({
        'url': url,
        'd_url': d_url,
        'title': title,
        #'author': author,
        'descr': descr,
        'engine': 'CiNii',
        })
    return ci_results, ci_urls
  except:
    return [], []
