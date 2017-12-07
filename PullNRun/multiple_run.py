import threading
import os
import json
import shutil
import make_host_copy

count = 0
mutex = threading.Lock()
start_port = 5001


class MyThread(threading.Thread):
    def __init__(self, cmd, port, environment, exe, log_path):
        threading.Thread.__init__(self)
        self.cmd = cmd.replace('bin', 'bin{}'.format(port-start_port))
        self.port = port
        self.log_to_path = './ret_{}.txt'.format(self.port)
        self.environment = environment
        self.exe = exe
        self.log_path = log_path

        self.parseCmd()
        self.refreshLogFile()

    def parseCmd(self):
        if not os.path.exists(os.path.join(self.cmd.split(self.exe)[0], self.log_path)):
            os.makedirs(os.path.join(self.cmd.split(self.exe)[0], self.log_path))
        self.abspath = os.path.join(self.cmd.split(self.exe)[0], self.log_path, self.log_to_path)


    def run(self):

        while True:
            mutex.acquire()
            global count
            if count > 0:
                count -= 1
                battle_id = count
                print 'a new battle is starting, {} battles remain...'.format(count)
                mutex.release()
                os.system('{} -port={} -noplatform -test_version_battle={} -version_battle_log_path={}'.format(self.cmd, self.port, battle_id, os.path.join(self.log_path, self.log_to_path)))
            else:
                mutex.release()
                break

    def refreshLogFile(self):
        #if os.path.exists(abspath):
        #    os.remove(abspath)
        log_file = file(self.abspath, 'w')
        log_file.close()


def processResult(cfg, threads, environment, log_path):
    data = []
    for t in threads:
        f = file(t.abspath, 'r')
        for line in f.readlines():
            json_value = json.loads(line)
            data.append({'id':json_value['id'],'line':line})

    data.sort(lambda x, y : cmp(x['id'], y['id']))

    f = file(os.path.join(threads[0].environment, log_path, 'final_ret.txt'), 'a')
    for row in data:
        f.write('{}'.format(row['line']))

    f.close()


def run():
    cfg = json.load(open('config.json', 'r'))
    global count
    count = int(cfg['times'])
    cmd = cfg['cmd']
    main_cmd = cmd.split(' ', 1)[0]
    arr = os.path.split(main_cmd)
    environment = arr[0]
    exe = arr[1]
    log_path = cfg['log_path'] or '.'

    need_new_copy = cfg.get('make_new_copy', False)
    folder = cfg['cmd'].split('bin')[0] + 'bin'
    if need_new_copy:
        print 'delete logs'
        make_host_copy.del_log(folder)

    if os.path.exists(os.path.join(environment, log_path)):
        shutil.rmtree(os.path.join(environment, log_path))
    os.makedirs(os.path.join(environment, log_path))

    f = file(os.path.join(environment, log_path, 'final_ret.txt'), 'w')
    f.close()
    threads = []
    for i in xrange(cfg["thread_num"]):
        print 'create thread {}'.format(i)
        if need_new_copy or (not os.path.exists(folder+str(i))):
            print 'make new GameHostServer copy...'
            make_host_copy.make_copy(folder, folder+str(i))
        threads.append(MyThread(cmd, start_port + i, environment, exe, log_path))
    for t in threads:
        print 'thread {} start!'.format(i)
        t.start()

    for t in threads:
        t.join()

    processResult(cfg, threads, environment, log_path)
