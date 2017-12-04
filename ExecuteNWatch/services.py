# -*- coding: utf8 -*-
import json
import os
import subprocess
import web

urls = ('/', 'Index',
        '/execute', 'Execute',
        '/showLog', 'ShowLog')
render = web.template.render('templates/')

web.user = 'unknown'
self_path = os.path.split(os.path.realpath(__file__))[0] + os.sep
config = json.load(open(self_path + 'conf.json', 'r'))


class Index:
    def GET(self):
        return render.index()


class Execute:
    def GET(self):
        show = open(self_path + 'show', 'w')
        p = subprocess.Popen(config['cmd'], stdout=show, stderr=show)


class ShowLog:
    def GET(self):
        try:
            web.header("Content-Type", "text/html; charset=gbk")
            return open(self_path + 'show', 'r').read()
        except IOError, e:
            print str(e)
            return '找不到show'
        except Exception, e:
            print str(e)
            return 'some unknown bug'

if __name__ == "__main__":
    app = web.application(urls, globals())

    web.httpserver.runsimple(app.wsgifunc(), (config['self_ip'], config['port']))
