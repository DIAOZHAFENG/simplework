# -*- coding: utf8 -*-
import json
import os
import sys
import web
from ftplib import FTP

urls = ('/compile', 'compile')
render = web.template.render('templates/')
reload(sys)
sys.setdefaultencoding('gbk')

class compile:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.index()

    def POST(self):
        info = web.input()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
