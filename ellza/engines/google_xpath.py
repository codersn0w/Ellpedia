# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re, html

def g_search(query, ua):
  try:
    values = {
      'q': query,
      'oq': query,
    }
    s_url = 'https://www.google.co.jp/search?safe=active&pws=0&source=hp&' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    base_xpath = root.xpath('.//div[@class="rc"]')
    title_xpath = './div[@class="r"]/a/h3//text()'
    link_xpath = './div[@class="r"]/a/@href'
    descr_xpath = './div[@class="s"]/div/span[@class="st"]//text()'
    g_urls = []
    g_wikis = []
    g_top_results = []

    for g in base_xpath:
      title = g.xpath(title_xpath)[0]
      url = g.xpath(link_xpath)[0]
      idescr = g.xpath(descr_xpath)
      descr = ''.join(idescr)

      if len(url) > 30:
        d_url = url[:30] + '...'
      else:
        d_url = url

      if 'ja.wikipedia.org/wiki/' in url or 'en.wikipedia.org/wiki/' in url:
        if not descr == '' and  g_wikis == []:
          g_wikis.append({
            'url': html.escape(url, quote=True),
            'd_url': html.escape(d_url, quote=True),
            'title': html.escape(title, quote=True),
            'descr': html.escape(descr, quote=True),
            })

      elif g_top_results == []:
        if not descr == '':
          g_top_results.append({
            'url': html.escape(url, quote=True),
            'd_url': html.escape(d_url, quote=True),
            'title': html.escape(title, quote=True),
            'descr': html.escape(descr, quote=True),
            })

      else:
        pass

    if g_wikis == [] and g_top_results != []:
       g_wikis = [{}]
    if g_top_results == [] and g_wikis != []:
       g_top_results = [{}]

    return g_wikis, g_top_results
  except:
    return [], []
