# -*- coding: utf8 -*-
import json
import os
import web
import logging

urls = ('/getFile', 'GetFile')
render = web.template.render('templates/')
self_path = os.path.split(os.path.realpath(__file__))[0] + os.sep
config = json.load(open(self_path + 'config.json', 'r'))

url_pattern = "http://{0}-{1}.file.myqcloud.com/{2}/".format(config['qcloud_cos_bucket'], config['qcloud_appid'], config['dst_root'])


class GetFile:
    def GET(self):
        return render.index()

    def POST(self):
        info = web.input()
        id = info['id']
        try:
            id = hex(int(id))[2:]
            if id[-1] == 'L':
                id = id[:-1]
        except ValueError:
            pass
        raise web.seeother("{0}/{1}.zip".format(url_pattern, id))


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
