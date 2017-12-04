# -*- coding: utf8 -*-
import sys
import os
import sender
import web
from threading import Thread
from urllib import unquote_plus
import time
self_path = os.path.split(os.path.realpath(__file__))[0] + '/'
sys.path.append(self_path + '..\\')
sys.path.append(self_path + '..\\VersionMachine')

urls = (
    '/(.*)/(.*)', 'service'
)


# 如果邮件服务器down了，send_mail会阻塞，所以索性这里开了个线程发
def send_mail(title, data, receiver_group):
    ms = sender.MailSender()
    ms.send_mail(unquote_plus(title), unquote_plus(data), receiver_group)
    print 'a mail has been sent to ' + receiver_group
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    record = timestamp + '\r\n' + title + '\r\n' + receiver_group + '\r\n' + data + '\r\n----------------------------------------------------------\r\n'
    with open("{path}mail_record/{name}.txt".format(path=self_path, name=timestamp.replace(":", "-")), 'w') as f:
        f.write(record)


t = None


class service:
    def POST(self, title, receiver_group):
        global t
        t = Thread(target=send_mail, args=(title, web.data(), receiver_group,))
        t.start()
        return "."


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
