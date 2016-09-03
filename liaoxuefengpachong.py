import requests


prifix = 'http://www.liaoxuefeng.com'
url_1 = prifix + '/static/themes/default/css/codemirror.css'
url_2 = prifix + '/static/themes/default/css/highlight.css'
url_3 = prifix + '/static/themes/default/css/itranswarp.css'


with open('./static/css/bootstrap3.3.min.css', 'w+', encoding='utf-8') as f:
    t1 = requests.get('http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css').text
    f.write(t1)
