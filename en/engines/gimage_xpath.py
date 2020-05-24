# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
from json import loads
import re

def gi_search(query, ua):
  try:
    values = {
      'q': query,
    }
    s_url = 'http://www.google.com/search?gl=us&hl=en&tbm=isch&gws_rd=cr&safe=active&pws=0&gbv=1&' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    image_xpath = root.xpath('//table[4]//a')
    link_xpath = './@href'
    thumb_xpath = './img/@src'
    results = []
    rc = re.compile('&sa=U&ved=0.*')
    num = 0
    for im in image_xpath:
      if num <= 7:
        url = im.xpath(link_xpath)[0].lstrip('/url?q=')
        url = rc.sub('', url)
        thumb_src = im.xpath(thumb_xpath)[0]
        d_url = url
        img_src = url
        results.append({'url': url,
          'd_url': d_url,
          'thumb_src': thumb_src,
          'img_src': img_src,
          })
        num+=1
      else:
        pass
    return results

  except:
    return []
