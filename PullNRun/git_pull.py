import os
import json
import shutil


def pull_git(commit='HEAD', branch='develop'):
    print('pull git with branch {0} and commit {1}'.format(branch, commit))
    os.system(r'git checkout ' + branch + ' --force')
    os.system("git pull")
    os.system(r'git checkout ' + branch + ' --force')
    if commit != 'HEAD':
        os.system(r'git reset --hard ' + commit)


def update_svn(revision=None, no_revert=False):
    os.system(r'svn cleanup')
    if not no_revert:
        os.system(r'svn revert -R . ')
    if revision is not None:
        os.system(r'svn update -r {} --accept theirs-full'.format(revision))
    else:
        os.system(r'svn update --accept theirs-full')


def get_version_ready():
    cfg = json.load(open('config.json', 'r'))["ai"]
    for ai in cfg:
        if ai['enable']:
            if not os.path.exists(ai['ai_path']):
                ai_p = os.path.split(ai['ai_path'])[0] + '/ai'
                shutil.copytree(ai_p, ai['ai_path'])
            os.chdir(ai['ai_path'])
            if '.git' in os.listdir('.'):
                pull_git(ai['ai_ver'], ai['ai_branch'])
            else:
                try:
                    update_svn(int(ai['ai_ver']))
                except ValueError:
                    update_svn()

if __name__ == '__main__':
    get_version_ready()