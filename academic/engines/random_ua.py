# coding: utf-8
import random
def generate_ua():
  b_tuple = ('ed', 'fr', 'ch', 'op', 'sf', 'vi')
  browser = random.choice(b_tuple)
  
  if browser == 'ed':
    edd = ({'chv': '51.0.2704.79', 'edv': '14.14393'},
    	   {'chv': '46.0.2486.0', 'edv': '13.10586'},)
    ver = random.choice(edd)
    base = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0[chv]} Safari/537.36 Edge/{0[edv]}'
    ua = base.format(ver)
    return ua

  elif browser == 'fr':
	  edd = ({'os': 'Windows NT 10.0', 'wintel': 'Win64; x64', 'rv': '50.0'},
		    {'os': 'Windows NT 10.0', 'wintel': 'Win64; x64', 'rv': '45.0'},
		    {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10.12', 'rv': '50.0'},
		    {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10.11', 'rv': '50.0'},
		    {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10.10', 'rv': '50.0'},
		    {'os': 'X11', 'wintel': 'Linux i686', 'rv': '50.0'},
		    {'os': 'X11', 'wintel': 'Linux x86_64', 'rv': '50.0'},
		    {'os': 'X11', 'wintel': 'Ubuntu; Linux i686', 'rv': '50.0'},
		    {'os': 'X11', 'wintel': 'Ubuntu; Linux x86_64', 'rv': '50.0'},)
	  ver = random.choice(edd)
	  base = 'Mozilla/5.0 ({0[os]}; {0[wintel]}; rv:{0[rv]}) Gecko/20100101 Firefox/{0[rv]}'
	  ua = base.format(ver)
	  return ua

  elif browser == 'ch':
	  edd = ({'os': 'Windows NT 10.0', 'wintel': 'Win64; x64', 'chv': '55.0.2883.87'},
	         {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_12_2', 'chv': '55.0.2883.95'},
		     {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_11_6', 'chv': '55.0.2883.95'},
		     {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_10_5', 'chv': '55.0.2883.95'},
		     {'os': 'X11', 'wintel': 'Linux x86_64', 'chv': '55.0.2883.87'},)
	  ver = random.choice(edd)
	  base = 'Mozilla/5.0 ({0[os]}; {0[wintel]}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0[chv]} Safari/537.36'
	  ua = base.format(ver)
	  return ua

  elif browser == 'op':
	  edd = ({'os': 'Windows NT 10.0', 'wintel': 'Win64; x64'},
		     {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_12_6'},
		     {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_11_3'},
		     {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_10_3'},
		     {'os': 'X11', 'wintel': 'Linux i686'},
		     {'os': 'X11', 'wintel': 'Linux x86_64'},)
	  ver = random.choice(edd)
	  base = 'Mozilla/5.0 ({0[os]}; {0[wintel]}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94'
	  ua = base.format(ver)
	  return ua

  elif browser == 'sf':
	  edd = ('10_12_5', '10_11_4', '10_10_2')
	  ver = random.choice(edd)
	  base = 'Mozilla/5.0 (Macintosh; Intel Mac OS X {0}) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12'
	  ua = base.format(ver)
	  return ua

  elif browser == 'vi':
	  edd = ({'os': 'Windows NT 10.0', 'wintel': 'Win64; x64', 'viv': '1.6.689.40'},
		     {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_12_4', 'viv': '1.6.689.40'},
		     {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_11_5', 'viv': '1.6.689.40'},
		     {'os': 'Macintosh', 'wintel': 'Intel Mac OS X 10_10_4', 'viv': '1.6.689.40'},
		     {'os': 'X11', 'wintel': 'Linux i686', 'viv': '1.6.689.46'},
		     {'os': 'X11', 'wintel': 'Linux x86_64', 'viv': '1.6.689.46'},
		     {'os': 'X11', 'wintel': 'Fedora; Linux i686', 'viv': '1.6.689.46'},
		     {'os': 'X11', 'wintel': 'Fedora; Linux x86_64', 'viv': '1.6.689.46'},)
	  ver = random.choice(edd)
	  base = 'Mozilla/5.0 ({0[os]}; {0[wintel]}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.98 Safari/537.36 Vivaldi/{0[viv]}'
	  ua = base.format(ver)
	  return ua

  else:
    return 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
