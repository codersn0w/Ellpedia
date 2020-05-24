# coding: utf-8
import requests
import json
import collections as cl
import time
from datetime import datetime

# APIキーの指定 - 以下を書き換えてください★ --- (※1)
apikey = "23210da5b41a86e22ddbdbde038a6b0d"

# 天気を調べたい都市の一覧 --- (※2)
cities = ["Tokyo,JP", "New York,US", "Cupertino,US", "London,UK",]
# APIのひな型 --- (※3)
api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

# 温度変換(ケルビン→摂氏) --- (※4)
k2c = lambda k: k - 273.15
# 各都市の温度を取得する --- (※5)
ys = cl.OrderedDict()
try:
  for name in cities:
    now_data = cl.OrderedDict()
    # APIのURLを得る --- (※6)
    url = api.format(city=name, key=apikey)
    # 実際にAPIにリクエストを送信して結果を取得する
    r = requests.get(url, timeout=10)
    # 結果はJSON形式なのでデコードする --- (※7)
    data = json.loads(r.text)    
    # 結果を画面に表示 --- (※8)
    city = data["name"]
    now_data["weather"] = data["weather"][0]["description"]
    now_data["temp"] = '%.2f' % k2c(data["main"]["temp"])
    now_data["icon"] = data["weather"][0]["icon"]
    ys[city] = now_data
    time.sleep(3)
  ys["time"] = datetime.now().strftime("%m/%d %H:%M (JST)")
  fw = open('/path/to/weather.json', 'w')
  json.dump(ys, fw, indent = 4)

except:
    pass
