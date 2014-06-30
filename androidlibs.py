#encoding=utf-8

import sys
import os

__version__ = "0.1"
current_path = os.path.abspath('.')

def show_help():
  help_text = '''
ʹ��˵��: androidlibs [--version] [-c androidlibs.txt] [-h] [ָ��]
  
����˵����
  --version       �汾��
  -c              ָ��androidlibs.txt������·��
  -h              �����ĵ�

ָ��˵����
  update          ���´��롣��ͬ����ʽ���£����Կ���ÿ�����̵ĸ��½��
  update-async    �첽���´��롣�޷�����ÿ�����̵ĸ��½��
  clean           �������Library����
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
  print '�ҵ�����Library���̣�׼����ʼ������...'
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
    print '���ȸ������µ�Library��������'
    ret, result = run_cmd("git pull origin master")
    if ret == 0:
      print 'Library�������ø������'
    else:
      print 'Library�������ø���ʧ�ܣ����������㵱ǰĿ¼�Ƿ���ȷ������һ�Ρ�'
      sys.exit()
  except Exception, e:
    print e
  
  try:
    config = get_config()
    if config:
      for lib in config:
      	if lib['tags']:
          for tag in lib['tags']:
            print '��ʼ���� %s ���� %s ��֧�����Ժ򡭡�' % (lib['name'], tag)
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
                    print 'master��֧����ʧ��'
                os.chdir(current_path)
              else:
                print '%s �Ѿ����ˣ��ҾͲ���������' % target
                 
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
                  print '%s��֧����ʧ��' % tag
            print ' %s ���̸�����ϡ�' % lib['name']
            print ' '
          
  except IOError, ioe:
    print '�Ҳ��������ļ���', e
  except Exception, e:
    print '��������', e
  
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


