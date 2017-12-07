# -*- coding: utf8 -*-
import Queue
import json
import os
import signal
import subprocess
import threading
import time
import web
from multiprocessing.managers import BaseManager

urls = ('/aiTest', 'AITest',
        '/showLog', 'ShowLog')
render = web.template.render('templates/')

web.mutex = threading.Lock()
web.record_mutex = threading.Lock()
c = json.load(open('cfg_temp.json', 'r'))
web.task_id = c.get('id', 0)

address = json.load(open('address.json'))

# 发送任务的队列:
task_queue = Queue.Queue()
# 接收结果的队列:
stat_queue = Queue.Queue()


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


def get_task_queue():
    return task_queue


def get_stat_queue():
    return stat_queue

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=get_task_queue)
QueueManager.register('get_stat_queue', callable=get_stat_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=(address['master']['ip'], address['master']['port']), authkey='abc')

web.status = {}


class AITest:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return render.index(web.status)

    def POST(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        info = web.input()
        print info
        try:
            web.mutex.acquire()
            web.task_id += 1
            config = json.load(open('cfg_temp.json', 'r'))
            config['ai'] = [
                {
                    "enable": info.get('en1'),
                    "ai_path": config['ai'][0]["ai_path"],
                    "ai_ver": info['v1'] or 'HEAD',
                    "ai_branch": info['b1'] or 'develop'
                },
                {
                    "enable": info.get('en2'),
                    "ai_path": config['ai'][1]["ai_path"],
                    "ai_ver": info['v2'] or 'HEAD',
                    "ai_branch": info['b2'] or 'develop'
                }
            ]
            config["id"] = int(web.task_id)
            config["times"] = int(info['t'])
            config["update_host"] = info.get('update')
            web.mutex.release()
            web.record_mutex.acquire()
            with open('record.json', 'r') as rf:
                record = json.load(rf)
                record[config["id"]] = {'v1': config['ai'][0]['ai_ver'], 'v2': config['ai'][1]['ai_ver']}
                print record
            with open('record.json', 'w') as rf:
                json.dump(record, rf)
            web.record_mutex.release()
            print config
            web.task.put(config)
            return '<h3>测试任务id: {}</h3>测试结束后可以来<a href = \'/showLog\'>这里</a>查看运行结果'.format(web.task_id)
        except Exception, e:
            return '{}，我猜json格式有毒'.format(e)


class ShowLog:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return render.log(json.load(open('record.json')))


class UpdateStatus(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if web.stat.qsize() > 0 :
                try:
                    new_status = web.stat.get(timeout=1)
                    web.status[new_status['address']] = new_status['status']
                    print 'get {}'.format(new_status)
                    if new_status['status']['busy']:
                        print 'acquiring'
                        web.record_mutex.acquire()
                        print 'acquired'
                        with open('record.json', 'r') as rf:
                            record = json.load(rf)
                        if record.get(str(new_status['status']['id'])) and record.get(str(new_status['status']['id'])).get('dealer') is None:
                            record[str(new_status['status']['id'])]['dealer'] = new_status['address']
                            print 'dump id:{}; dealer:{}'.format(new_status['status']['id'], new_status['address'])
                            with open('record.json', 'w') as rf:
                                json.dump(record, rf)
                        web.record_mutex.release()
                except Queue.Empty:
                    time.sleep(1)
                except Exception, e:
                    print 'I guess stat_queue goes wrong, {}: {}'.format(type(e), e)
                    web.record_mutex.release()
            else:
                time.sleep(1)

if __name__ == "__main__":
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    web.task = manager.get_task_queue()
    web.stat = manager.get_stat_queue()
    updater = UpdateStatus()
    updater.start()
    app = web.application(urls, globals())
    app.run()
