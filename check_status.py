#encoding=utf-8

import sys
import os

__version__ = "1.0"
current_path = os.path.abspath('.')


def run_cmd(cmd):
    import subprocess
    #print 'Run : %s' % cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = [line for line in p.stdout.readlines()]
    retval = p.wait()
    return retval, result


def run_cmd_async(cmd):
    import subprocess
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def do_check():
    try:
        no_commits = []
        #print u'开始检查AndroidLibs提交情况......'
        fs = os.listdir(current_path)
        i = 0
        for lib_dir in fs:
            i += 1
            print 'Please waiting...%s/%s\r' % (i, len(fs)),
            if lib_dir.endswith('-lib') and os.path.isdir(lib_dir):
                master_dir = '%s/%s/master' % (current_path, lib_dir)
                if os.path.exists(master_dir):
                    os.chdir(master_dir)
                    ret, result = run_cmd("git status")
                    os.chdir(current_path)
                    if ret == 0 and len(result) > 1:
                        is_commit = False
                        for r in result:
                            if r.find('nothing to commit') > -1:
                                is_commit = True
                        if not is_commit:
                            no_commits.append(lib_dir)
                            
        if len(no_commits) == 0:
            print u'AndroidLibs全部提交啦，你可以洗洗睡了！！！'
        else:
            print u'工程 %s 没有提交，快滚去提交...' % ",".join(no_commits)
    except Exception, e:
        print u'出错啦！', e


if len(sys.argv) <= 1:
    do_check()
    sys.exit()

if '--version' in sys.argv:
    print 'Version: %s' % __version__

