import os
import shutil
import json


def del_log(src):
    log_path = os.path.join(src, 'win/log')
    if os.path.exists(log_path):
        shutil.rmtree(log_path)


def make_copy(src, des):
    if os.path.exists(des):
        shutil.rmtree(des)
    os.mkdir(des)
    shutil.copytree(src+'/config', des+'/config')
    shutil.copytree(src+'/win', des+'/win')


if __name__ == '__main__':
    cfg = json.load(open('config.json', 'r'))
    folder = cfg['cmd'].split('bin')[0] + 'bin'
    del_log(folder)
    for i in range(cfg['thread_num']):
        make_copy(folder, folder+str(i))
