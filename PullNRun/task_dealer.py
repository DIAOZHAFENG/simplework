# -*- coding: gbk -*-

import Queue
import json
import os
import threading
import time
import subprocess
from multiprocessing.managers import BaseManager
import signal
import web

urls = ('/showLog/(.*)', 'ShowLog',
        '/abort', 'Abort')
render = web.template.render('templates/')

# web.pid = -1
# web.task_id = -1
web.mutex = threading.Lock()
log_p = 'log/ai_test_log/{id}'
address = json.load(open('address.json'))


# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass


# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_stat_queue')

# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(address['master']['ip'], address['master']['port']), authkey='abc')



def is_busy():
    if '.lock' in os.listdir('.'):
        return True
    else:
        return False


class ShowLog:
    def GET(self, id):
        try:
            web.header("Content-Type", "text/html; charset=utf-8")
            web.mutex.acquire()
            with open('config.json', 'r') as f:
                cfg = json.load(f)
            web.mutex.release()
            cmd = cfg['cmd']
            arr = os.path.split(cmd)
            environment = arr[0]
            log_path = environment + '/' + log_p.format(id=id)
            res = {}
            if os.path.exists(log_path + '/error'):
                res['error'] = open(log_path + '/error', 'r').read()
            else:
                res['result'] = {}
                for fn in os.listdir(log_path):
                    for line in open(log_path + '/' + fn, 'r'):
                        if '#@!!' in line:
                            l = json.loads(line.split('#@!!')[1])
                            if res['result'].get(l['id']) is None:
                                res['result'][l['id']] = {}
                            if 'winner' in l:
                                res['result'][l['id']]['winner'] = l['winner']
                            else:
                                res['result'][l['id']]['session_id'] = l['session_id']
            return render.result(json.dumps(res))
        except IOError, e:
            print str(e)
            return '找不到show'
        except Exception, e:
            print str(e)
            return 'some unknown bug'

    # def POST(self):
    #     try:
    #         web.header("Content-Type", "text/html; charset=utf-8")
    #         web.task_id = web.data()
    #         cfg = json.load(open('config.json', 'r'))
    #         cmd = cfg['cmd']
    #         arr = os.path.split(cmd)
    #         environment = arr[0]
    #         log_path = environment + '/' + log_p.format(id=web.task_id)
    #         res = {}
    #         if os.path.exists(log_path + '/error'):
    #             res['error'] = open(log_path + '/error', 'r').read()
    #         else:
    #             res['result'] = {}
    #             for fn in os.listdir(log_path):
    #                 for line in open(log_path + '/' + fn, 'r'):
    #                     print line
    #                     if '#@!!' in line:
    #                         l = json.loads(line.split('#@!!')[1])
    #                         if res['result'].get(l['id']) is None:
    #                             res['result'][l['id']] = {}
    #                         if 'winner' in l:
    #                             res['result'][l['id']]['winner'] = l['winner']
    #                         else:
    #                             res['result'][l['id']]['session_id'] = l['session_id']
    #         return json.dumps(res)
    #     except IOError, e:
    #         print str(e)
    #         return '找不到show'
    #     except Exception, e:
    #         print str(e)
    #         return 'some unknown bug'

class Abort:
    def GET(self):
        try:
            if is_busy() and web.pid > 0:
                print 'kill subprocess {}'.format(web.pid)
                os.kill(web.pid, signal.SIGTERM)
                print 'kill GameHostServer'
                os.system("taskkill /f /im GameHostServer.exe")
                print 'remove .lock'
                os.remove('.lock')
                print 'done'
                return web.seeother('http:{}:{}/aiTest'.format(address['master']['ip'], address['master']['port']))
        except WindowsError, e:
            return '结束进程失败, pid: {}, error: {}'.format(web.pid, e)
        except Exception, e:
            print type(e), str(e)


class RegularExecute(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # 从网络连接:
        m.connect()
        print 'Connected'
        # 获取Queue的对象:
        self.task = m.get_task_queue()
        self.stat = m.get_stat_queue()

    def run(self):
        while True:
            global address
            status = {'address': '{ip}:{port}'.format(ip=address['dealer']['ip'], port=address['dealer']['port']), 'status': {'busy': is_busy(), 'id': -1}}
            try:
                status['status']['id'] = web.task_id
                print 'put id: {}'.format(web.task_id)
            except Exception:
                print 'no task'
            self.stat.put(status)
            if not is_busy():
                try:
                    config = self.task.get(timeout=1)
                    web.mutex.acquire()
                    with open('config.json', 'r') as f:
                        old_config = json.load(f)
                    old_config['times'] = config['times']
                    old_config['ai'] = config['ai']
                    old_config["update_host"] = config["update_host"]
                    old_config['log_path'] = log_p.format(id=config['id'])
                    old_config['id'] = config['id']
                    with open('config.json', 'w') as f:
                        json.dump(old_config, f)
                    web.mutex.release()
                    cmd = 'python run_with_local_cfg.py'
                    p = subprocess.Popen(cmd)
                    web.pid = p.pid
                    print web.pid
                    web.task_id = config['id']
                except Queue.Empty:
                    pass
            time.sleep(1)

if __name__ == '__main__':
    if os.path.exists('.lock'):
        try:
            os.remove('.lock')
        except WindowsError, e:
            print('尝试删除.lock失败，WindowsError:' + str(e))
        except Exception, e:
            print('尝试删除.lock失败，Exception:' + str(e))
    re = RegularExecute()
    re.start()
    app = web.application(urls, globals())
    web.httpserver.runsimple(app.wsgifunc(), (address['dealer']['ip'], address['dealer']['port']))