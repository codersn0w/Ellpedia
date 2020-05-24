# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import unicodedata
from json import loads
from urllib.parse import urljoin

def bn_search(query, ua):
  try:
    values = {
      'q': query,
      'pq': query,
      'setlang': 'en-us',
      }
    s_url = 'https://www.bing.com/news/search?setmkt=en-us&' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    base_xpath = root.xpath('//div[contains(@class, "newsitem")]//div[@class="caption"]')
    link_xpath = './div[@class="t_s"]/div[@class="t_t"]/a/@href'
    title_xpath = './div[@class="t_s"]/div[@class="t_t"]/a//text()'
    source_xpath = './div[@class="source"]/a/text()'
    time_xpath = './div[@class="source"]/span[2]//text()'
    results = []
    num = 0
    for n in base_xpath:
      if num<=3:
        url = n.xpath(link_xpath)[0]
        title = ''.join(n.xpath(title_xpath))
        source = n.xpath(source_xpath)[0]
        time = n.xpath(time_xpath)[0] + ' ago'
        results.append({'url': url,
                    'title': title,
                    'num': num,
                    'source': source,
                    'time': time,
                    })
        num+=1
      else:
        break
    return results

  except:
    return []
