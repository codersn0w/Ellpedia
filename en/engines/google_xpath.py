# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re

def g_search(query, page, spel, ua):
  try:
    values = {
      'q': query,
      'oq': query,
    }
    offset = 10 * (page - 1)
    if spel and spel == 1:
      s_url = 'https://www.google.com/search?gl=us&hl=en&gws_rd=cr&tbs=li:1&safe=active&pws=0&source=hp&start=' + str(offset) + '&num=10&' + up.urlencode(values)
    else:
      s_url = 'https://www.google.com/search?gl=us&hl=en&gws_rd=cr&safe=active&pws=0&source=hp&start=' + str(offset) + '&num=10&' + up.urlencode(values)
    headers = {
          "User-Agent": ua,
          }
    request = req.Request(url=s_url, headers=headers)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    spellist = root.xpath('.//a[@class="gL9Hy"]//text()')
    origlist = root.xpath('.//a[@class="spell_orig"]//text()')
    if spellist:
      spell = ''.join(spellist)
    else:
      spell = ''
    if origlist:
      orig = ''.join(origlist)
    else:
      orig = ''
    base_xpath = root.xpath('.//div[@class="g"]')
    title_xpath = './/div[@class="tF2Cxc"]/div[@class="yuRUbf"]/a/h3/text()'
    link_xpath = './/div[@class="tF2Cxc"]/div[@class="yuRUbf"]/a/@href'
    descr_xpath = './/div[@class="IsZvec"]/div//text()'
    g_urls = []
    g_wikis = []
    g_top_results = []
    g_results = []
    sug_results = []
    rc = re.compile('http(s)?://(www.)?')
    i = 1
    l = 0
    for g in base_xpath:
      title = g.xpath(title_xpath)[0]
      url = g.xpath(link_xpath)[0]
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

      if 'en.wikipedia.org/wiki/' in url and page == 1:
        if not descr == '':
          g_wikis.append({
            'url': url,
            'd_url': d_url,
            'title': title,
            'descr': descr,
            })

      elif i <= 3:
        if not descr == '':
          g_top_results.append({
            'url': url,
            'd_url': d_url,
            'title': title,
            'descr': descr,
            })

      else:
        g_results.append({
          'url': url,
          'd_url': d_url,
          'title': title,
          'descr': descr,
          })
      i+=1
    '''try:
      sug_base_xpath = root.xpath('.//div[@id="botstuff"]//a[@class="k8XOCe"]/div[@class="s75CSd OhScic AB4Wff"]/b//text()')
      while l<=2:
        sug = sug_base_xpath[l]
        if not query in sug:
          sug = query + ' ' + sug
        sug_results.append({
          'word': sug,
          'num': l,
          })
        l+=1
    except:
      pass'''
    return g_wikis, g_top_results, g_results, g_urls, spell, orig, []
  except:
    return [], [], [], [], '', '', []