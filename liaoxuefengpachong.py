import requests


prifix = 'http://www.liaoxuefeng.com'
url_1 = prifix + '/static/themes/default/css/codemirror.css'
url_2 = prifix + '/static/themes/default/css/highlight.css'
url_3 = prifix + '/static/themes/default/css/itranswarp.css'


with open('./static/css/lxfcss3.css', 'w+', encoding='utf-8') as f:
    t1 = requests.get(url_3).text
    f.write(t1)
