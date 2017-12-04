# -*- coding: utf-8 -*-

import CdnWarmUp
import web
import os
import json
import qcloud_cos
from mailsender.sender import MailSender

urls = ('/unw', 'UploadNWarmUp')

self_path = os.path.split(os.path.realpath(__file__))[0] + os.sep
config = json.load(open(self_path + 'config.json', 'r'))

qcloud_cos_bucket = 'acupdate'


class UploadNWarmUp:
    def upload_qcos(self, qcos, src, dst):
        result = qcos.upload_slice(src, qcloud_cos_bucket, dst)
        if result.get('code', -1) == 0:
            print('qcos upload success. {0} -> {1}'.format(src, dst))
            print(result)
            return True, result
        else:
            print('qcos upload failed. {0} -> {1}'.format(src, dst))
            print(result)
            return False, result

    def POST(self):
        info = json.loads(web.data())
        print type(info)
        qcos = qcloud_cos.Cos(str(config['qcloud_appid']), str(config['qcloud_secret_id']), str(config['qcloud_secret_key']))
        sender = MailSender()
        ok = '好了'
        result = ''
        for name in info['name']:
            src_path = '{0}/{1}'.format(config['local_root'], name)
            dst_path = '{0}/{1}'.format(config['dst_root'], name)
            ok1, res1 = self.upload_qcos(qcos, src_path, dst_path)
            if ok1:
                ok2, res2 = CdnWarmUp.go(dst_path)
                if ok2:
                    result += '{0}上传成功并且预热完成了\n'.format(name)
                else:
                    ok = '喔豁'
                    result += '{0}上传成功了但是预热出问题了：\n{1}\n'.format(name, str(res2))
            else:
                ok = '喔豁'
                result += '{0}上传出问题了：\n{1}\n'.format(name, str(res1))
        sender.send_mail(ok, result, config['receiver'])

if __name__ == "__main__":
    app = web.application(urls, globals())

    web.httpserver.runsimple(app.wsgifunc(), (config['self_ip'], config['port']))