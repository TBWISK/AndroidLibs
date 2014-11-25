#encoding=utf-8

import sys
import os

__version__ = "1.0"


def show_help():
  help_text = u'''
使用说明: check_status [--version] [-p d:/androidlibs] [-h]

参数说明：
  --version       版本号
  -p              指定AndroidLibs目录
  -h              帮助文档

  '''
  print help_text

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
    current_path = os.path.abspath('.')
    if '-p' in sys.argv and sys.argv[sys.argv.index('-p')+1]:
        current_path = sys.argv[sys.argv.index('-p')+1]
    os.chdir(current_path)
    try:
        no_commits = []
        #print u'开始检查AndroidLibs提交情况......'
        fs = os.listdir(current_path)
        i = 0
        for lib_dir in fs:
            i += 1
            print u'Please waiting...%s/%s\r' % (i, len(fs)),
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
            print u'All android libs already commited, good day !!!'
        else:
            print u'Projects [%s] not commit...' % ",".join(no_commits)
    except Exception, e:
        print e

if '--version' in sys.argv:
    print 'Version: %s' % __version__

if '-h' in sys.argv:
  show_help()
  sys.exit()

do_check()
