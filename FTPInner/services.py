# -*- coding: utf8 -*-
import json
import os
import sys
import urllib
import web
from ftplib import FTP

cfg = json.load(open('conf.json'))
log_path = 'log.log'
ftp_folder = cfg['ftp_folder']
http_folder = cfg['http_folder']
urls = ('/download', 'download',
        '/download/(.*)', 'download')
render = web.template.render('templates/')
reload(sys)
sys.setdefaultencoding('gbk')



class download:
    def GET(self, path=None):
        web.header("Content-Type","text/html; charset=utf-8")
        if path is None:
            return render.index()
        else:
            p = urllib.unquote_plus(str(path))
            parse_path = p.split('/')
            file_dir = '/'.join(parse_path[3:-1]) + '/'
            filename = parse_path[-1]
            dir_path = http_folder + file_dir    # 文件保存路径
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            file_path = dir_path + filename
            urllib.urlretrieve(p.encode('utf-8'), file_path)
            urllib.urlcleanup()
            return render.ok('同步成功')

    def POST(self):
        web.header("Content-Type","text/html; charset=utf-8")
        log = open(log_path, 'a')
        try:
            info = web.input()
            parse_path = info['path'].split('/')
            ftp_ip = parse_path[2]
            if '@' in ftp_ip:
                ftp_ip = ftp_ip.split('@')[1]
            file_dir = '/'.join(parse_path[3:-1]) + '/'
            filename = parse_path[-1]
            log.write('ftp ip: {0}; file directory: {1}; file name: {2}\r\n'.format(ftp_ip, file_dir, filename))
            log.write('username: {0}; password: {1}\r\n'.format(info['username'], info['password']))

            ftp = FTP()
            timeout = 30
            port = 0
            ftp.connect(ftp_ip, port, timeout)  # 连接FTP服务器
            ftp.login(info['username'], info['password'])  # 登录
            ftp.cwd(file_dir)    # 设置FTP路径
            dir_list = ftp.nlst()       # 获得目录列表
            for name in dir_list:
                print(name)
            path = ftp_folder + file_dir    # 文件保存路径
            if not os.path.exists(path):
                os.makedirs(path)

            file_path = path + filename
            f = open(file_path.encode("gbk"), 'wb')         # 打开要保存文件
            ftp.retrbinary('RETR %s' % filename, f.write)  # 保存FTP上的文件
            f.close()
            ftp.quit()                  # 退出FTP服务器
            return render.ok('OK')
        except Exception, e:
            print str(e)
            log.write('something went wrong: {0}: {1}'.format(type(e), str(e)))
            return render.not_ok('喔豁 :{0}'.format(str(e)))
        finally:
            log.close()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
