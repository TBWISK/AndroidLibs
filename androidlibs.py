#encoding=utf-8

import sys
import os

__version__ = "0.1"
current_path = os.path.abspath('.')

def show_help():
  help_text = '''
使用说明: androidlibs [--version] [-c androidlibs.txt] [-h] [指令]
  
参数说明：
  --version       版本号
  -c              指定androidlibs.txt的完整路径
  -h              帮助文档

指令说明：
  update          更新代码。以同步方式更新，可以看到每个工程的更新结果
  update-async    异步更新代码。无法看到每个工程的更新结果
  clean           清除所有Library工程
  '''
  print help_text

def get_config():
  if '-c' in sys.argv and sys.argv[sys.argv.index('-c')+1]:
    config_arg = sys.argv[sys.argv.index('-c')+1]
  else:
    config_arg = 'androidlibs.txt'
  config_file = open(config_arg, 'r')
  config_str = [line.replace("\n","") for line in config_file.readlines()]
  config_str = "".join(config_str)
  exec(config_str)
  print '找到以下Library工程，准备开始更新啦...'
  print '============'
  for tag in androidlibs_config:
    print ' ', tag['name']
  print '============'
  return androidlibs_config

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
  
def do_update(async=False):
  try:
    print '首先更新最新的Library工程配置'
    ret, result = run_cmd("git pull origin master")
    if ret == 0:
      print 'Library工程配置更新完毕'
    else:
      print 'Library工程配置更新失败！！！请检查你当前目录是否正确，再试一次。'
      sys.exit()
  except Exception, e:
    print e
  
  try:
    config = get_config()
    if config:
      for lib in config:
      	if lib['tags']:
          for tag in lib['tags']:
            print '开始更新 %s 工程 %s 分支，请稍候……' % (lib['name'], tag)
            target = '%s-lib/master' % lib['name'] if tag == 'master'else '%s-lib/releases/%s' % (lib['name'], tag)
            if os.path.exists(target):
              if tag == 'master':
                os.chdir('%s/%s' % (current_path, target))
                cmd = 'git pull origin master'
                if async:
                  run_cmd_async(cmd)
                else:
                  ret, result = run_cmd(cmd)
                  if ret != 0:
                    print 'master分支更新失败'
                os.chdir(current_path)
              else:
                print '%s 已经有了，我就不更新啦。' % target
                 
            else:
              if tag == 'master':
                cmd = "git clone %s %s" % (lib['repo'], target)
              else:
                cmd = "git clone --single-branch -b %s %s %s" % (tag, lib['repo'], target)
              if async:
                run_cmd_async(cmd)
              else:
                ret, result = run_cmd(cmd)
                if ret != 0:
                  print '%s分支更新失败' % tag
            print ' %s 工程更新完毕。' % lib['name']
            print ' '
          
  except IOError, ioe:
    print '找不到配置文件。', e
  except Exception, e:
    print '出错啦！', e
  
def do_clean():
  run_cmd("rm -rf *-lib")
  
if len(sys.argv) <= 1:
  show_help()
  sys.exit()
  
if '-h' in sys.argv:
  show_help()
  sys.exit()
  
if 'update' in sys.argv:
  try:
    do_update()
  except Exception, e:
    print e
  sys.exit()


if 'update-async' in sys.argv:
  try:
    do_update(True)
  except Exception, e:
    print e
  sys.exit()


if 'clean' in sys.argv:
  try:
    do_clean()
  except Exception, e:
    print e


