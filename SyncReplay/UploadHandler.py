# -*- coding: utf-8 -*-
import shutil
import threading
import time
import CdnWarmUp
import os
import json
import qcloud_cos
import logging

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='record.log',
                filemode='a')

self_path = os.path.split(os.path.realpath(__file__))[0] + os.sep
config = json.load(open(self_path + 'config.json', 'r'))
qcos = qcloud_cos.Cos(str(config['qcloud_appid']), str(config['qcloud_secret_id']), str(config['qcloud_secret_key']))

process_list = []
sync_dir = '{}/sync'.format(config['local_root'])
mutex = threading.Lock()
request_mutex = threading.Lock()


def upload_qcos(src, dst):
    result = qcos.upload_slice(src, str(config['qcloud_cos_bucket']), dst)
    if result.get('code', -1) == 0:
        print('qcos upload success. {0} -> {1}'.format(src, dst))
        print(result)
        return True, result
    else:
        print('qcos upload failed. {0} -> {1}'.format(src, dst))
        if result['code'] == -177:
            qcos.deleteFile(str(config['qcloud_cos_bucket']), dst)  # 迷之上传失败留下一具尸体
        elif result['code'] == -4018:
            os.remove(src)  # 重复上传
        print(result)
        return False, result


def upload(name):
    src_path = '{0}/{1}'.format(config['local_root'], name)
    dst_path = '{0}/{1}'.format(config['dst_root'], '{}.zip'.format(name.split('_')[0]))
    ok, res = upload_qcos(src_path, dst_path)
    if ok:
        logging.info('{0}上传成功'.format(name))
    else:
        logging.warning('{0}上传出问题了：\n\t{1}'.format(name, str(res)))
    return ok


def warm_up(name):
    dst_path = '{0}/{1}'.format(config['dst_root'], '{}.zip'.format(name.split('_')[0]))
    ok, res = CdnWarmUp.go(dst_path)
    if ok:
        logging.info('{0}上传成功并且预热完成了'.format(name))
    else:
        logging.warning('{0}上传成功了但是预热出问题了：\n\t{1}'.format(name, str(res)))


class UploadHandler(threading.Thread):
    def run(self):
        while True:
            mutex.acquire()
            dir_list = os.listdir(config['local_root'])
            to_process_list = [n for n in dir_list if n not in process_list and '.zip' in n and n[0:-4] not in dir_list]
            if len(to_process_list) == 0:
                mutex.release()
                time.sleep(1)
                continue
            n = to_process_list[0]
            process_list.append(n)
            mutex.release()
            res = upload(n)
            if res:
                if not os.path.exists(sync_dir):
                    os.makedirs(sync_dir)
                if os.path.exists('{0}/{1}'.format(sync_dir, n)):
                    os.remove('{0}/{1}'.format(sync_dir, n))
                    logging.warning('{0}上传好像重复了'.format(n))
                shutil.move('{0}/{1}'.format(config['local_root'], n), '{0}/{1}'.format(sync_dir, n))
            mutex.acquire()
            process_list.remove(n)
            mutex.release()
            if res:
                request_mutex.acquire()
                try:
                    warm_up(n)
                except CdnWarmUp.ResponseException:
                    try:
                        # try again
                        warm_up(n)
                    except Exception:
                        # keep fail record
                        fail_list = []
                        try:
                            fail_list = json.load(open(self_path + 'fail.json', 'r'))
                        except Exception:
                            pass
                        fail_list.append(n)
                        json.dump(fail_list, open(self_path + 'fail.json', 'w'))
                request_mutex.release()

if __name__ == '__main__':
    threads = []
    for i in xrange(config["thread_num"]):
        threads.append(UploadHandler())
        threads[i].start()
