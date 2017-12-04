from urllib import request

resp = request.urlopen('https://movie.douban.com/nowplaying/shanghai/')
html_data = resp.read().decode('utf-8')
