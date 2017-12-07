import os
import json
import git_pull
import make_host_copy

if __name__ == '__main__':
    try:
        cfg = json.load(open('config.json', 'r'))
        self_path = os.getcwd()
        f = open('.lock', 'w')
        f.close()
        git_pull.get_version_ready()
        folder = cfg['cmd'].split('bin')[0] + 'bin'
        if cfg['update_host']:
            git_pull.update_svn(revision=cfg['update_host'], no_revert=True)
        os.chdir(self_path)
        os.system('{} -startupmode=3 -testaiex={} -port=5001 -noplatform -test_version_battle2 -version_battle_log_path={} -multi_thread_count={} < nul'.format(cfg['cmd'], cfg['times'], cfg['log_path'], cfg['thread_num']))
        if '.lock' in os.listdir('.'):
            os.remove('.lock')
    except Exception, e:
        print '.something_bad_happened'
        if '.lock' in os.listdir('.'):
            os.remove('.lock')
        cmd = cfg['cmd']
        main_cmd = cmd.split(' ', 1)[0]
        arr = os.path.split(main_cmd)
        environment = arr[0]
        log_path = cfg['log_path'] or '.'
        d = environment + '/' + log_path
        if not os.path.exists(d):
            os.mkdir(d)
        f = open(d + '/error', 'w')
        f.write(str(type(e)) + str(e))
