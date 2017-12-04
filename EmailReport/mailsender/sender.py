# -*- coding: utf8 -*-
import json

import time

import smtplib
import sys
import os

self_path = os.path.split(os.path.realpath(__file__))[0] + '/'
sys.path.append(self_path + '..\\')
import chardet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Logger:
    def __init__(self, filename="log"):
        self.terminal = sys.stdout
        self.log = open(filename, 'w')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()

    def flush(self):
        self.log.flush()
        self.terminal.flush()

class MailSender:
    def __init__(self):
        self.groups_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'groups.json'

        with open(self.groups_path, 'r') as f:
            self.groups = json.loads(f.read())

        return

    def send_mail(self, title, content, group_name):
        me = 'acmoba-auto@7fgame.com'
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = me
        if group_name in self.groups:
            msg['To'] = ', '.join(self.groups[group_name])
        else:
            msg['To'] = group_name + '@7fgame.com'

        mail_body = "<html><head></head><body><pre>" + content + "</pre></body></html>"

        if not isinstance(mail_body, unicode):
            charset = chardet.detect(mail_body)
            mail_body = mail_body.decode(charset['encoding'], 'ignore')

        mail_body.encode('utf-8')

        msg.attach(MIMEText(mail_body, 'html', _charset='utf-8'))

        s = smtplib.SMTP('smtp.7fgame.com')
        s.login('acmoba-auto', 'Mail@rtx')
        if group_name in self.groups:
            s.sendmail(me, self.groups[group_name], msg.as_string())
        else:
            s.sendmail(me, [group_name + '@7fgame.com'], msg.as_string())
        s.quit()
        return


if __name__ == '__main__':
    # test
    sys.stdout = Logger()
    ms = MailSender()
    with open('version.log', 'r') as f:
        lines = f.readlines()
    for line in lines:
        print line,
    sys.stdout.flush()
    sys.stdout.close()
    with open('log', 'r') as f:
        content = "<pre>" + f.read() + "</pre>"
    ms.send_mail('auto-test', content, 'shudingwen')
