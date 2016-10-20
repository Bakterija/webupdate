from __future__ import print_function
from sys import path
from threading import Thread
from time import sleep
from os.path import expanduser
from sys import argv
import os
import shutil
import subprocess
import sys
import colorama
colorama.init(autoreset=True)

class BuildUpdater(object):
    logger = None
    www_path = '/var/www/html'
    def __init__(self, buildoze='none', **kwargs):
        if 'webpath' in kwargs:
            self.www_path = kwargs['webpath']
        self.printer('Increasing build number by 1 in %s' % (path[0]+'/version.txt'))
        ver = self.increase_version_number(path[0]+'/version.txt')
        if buildoze == 'none':
            self.build_no_buildozer(ver)
        elif buildoze == 'android':
            self.buildozer_android_debug()
            self.build(ver)
        elif buildoze == 'android_new':
            self.buildozer_android_new_debug()
            self.build(ver)

    def printer(self, text):
        print(colorama.Fore.BLUE + '[BuildUpdater]', text)

    def increase_version_number(self, ver_path):
        with open(ver_path, "r") as f:
            ver = int(f.read())
            ver += 1
        with open(ver_path, "w") as f:
            f.write(str(ver))
            return str(ver)

    def build(self, ver):
        var1 = ('apd_ver'+ver, 'apd_ver'+ver+'.zip')
        var2 = self.www_path
        home = expanduser("~")
        pwd = os.getcwd()

        self.printer('Archiving buildozer/android/app/ contents into %s' % (var1[1]))
        shutil.make_archive(home+'/'+var1[0], 'zip', root_dir='.buildozer/android/app/')
        r = self.try_move(home+'/'+var1[1], var2)

        if r == True:
            self.printer(colorama.Fore.GREEN + 'Build update successful')
        else:
            self.printer(colorama.Fore.RED + 'Build update failed')

    def build_no_buildozer(self, ver):
        var1 = ('apd_ver'+ver, 'apd_ver'+ver+'.zip')
        var2 = self.www_path
        home = expanduser("~")
        pwd = os.getcwd()
        tempdir = 'temporary_apupdater_folder1111'
        temppath = '%s/Desktop/%s/' % (home, tempdir)
        self.printer('Creating tempdir "%s"' % (temppath))
        self.mkdir(temppath)

        self.printer('Moving bin and .buildozer to tempdir')
        self.try_move('bin', temppath)
        self.try_move('.buildozer', temppath)

        self.printer('Archiving active folder contents into %s' % (var1[1]))
        shutil.make_archive(home+'/'+var1[0], 'zip', root_dir='.')
        r = self.try_move(home+'/'+var1[1], var2)

        self.printer('Moving bin and .buildozer back to active dir')
        self.try_move(temppath+'/bin', pwd+'/')
        self.try_move(temppath+'/.buildozer', pwd+'/')

        self.printer('Removing tempdir')
        self.rmdir(temppath)
        if r == True:
            self.printer(colorama.Fore.GREEN + 'Build update successful')
        else:
            self.printer(colorama.Fore.RED + 'Build update failed')

    def try_move(self, source, target):
        try:
            shutil.move(source, target)
            return True
        except Exception as e:
            self.printer(e)
            return False

    def mkdir(self, target):
        if not os.path.exists(target):
            os.makedirs(target)

    def rmdir(self, target):
        if os.path.exists(target):
            os.removedirs(target)

    def buildozer_android_debug(self):
        self.subprocess_cmd('buildozer android debug')

    def buildozer_android_new_debug(self):
        self.subprocess_cmd('buildozer android_new debug')

    def logging(self, text):
        if self.logger:
            self.logger(text)

    def subprocess_cmd(self, command, *args):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() is not None:
                break
            sys.stdout.write(nextline)
            sys.stdout.flush()
        output = process.communicate()[0]
        exitCode = process.returncode
        if (exitCode == 0):
            return output
        else:
            raise ProcessException(command, exitCode, output)

if __name__ == '__main__':
    kwargs = {}
    buildoze = 'none'
    if '--buildozer-android' in argv:
        buildoze = 'android'
    elif '--buildozer-android_new' in argv:
        buildoze = 'android_new'
    for i, x in enumerate(argv):
        if x == '--webpath':
            kwargs['webpath'] = argv[i+1]
    BuildUpdater(buildoze=buildoze, **kwargs)
