from __future__ import print_function
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import cm, dp
from kivy.clock import Clock
from threading import Thread
from os import remove as remove_file
import requests
import zipfile
import traceback


class ApacheUpdater(object):
    own_ver = 1
    version_path = ''
    update_path = ''
    http_path = ''
    autoupdate = False
    prompts = True
    logger = None
    builds = []
    threaded_update = False
    on_check_update = []
    on_update = []
    def __init__(self):
        pass

    def logging(self, text):
        if self.logger:
            self.logger(text)
            print(text)

    def find_http_zips(self, text):
        versions = []
        while True:
            b = text.find('href="apd_ver')
            c = text[b:].find('.zip') + b
            if b != -1:
                versions.append({'ver': int(text[b+13:c]), 'link': self.http_path+text[b+6:c+4]})
                text = text[c+1:]
            else:
                version = sorted(versions, key=lambda k: k['ver'])
                return versions

    def download_file(self, url):
        r = requests.get(url, stream=True)
        size = int(r.headers['Content-Length'])
        printtime = [0.0, 0.1]
        with open(self.update_path+'temp.zip', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    printtime[0] += 1024.0
                    while True:
                        if size*printtime[1] < printtime[0]:
                            printtime[1] += 0.1
                        else:
                            if round(printtime[0]/size*100,2) < 100:
                                self.logging('Downloaded %s%s' % (round(printtime[0]/size*100,2),'%'))
                            break
        self.logging('Download %s%s' % (100,'%'))

    def extract_files(self, fpath='temp.zip'):
        self.logging('Extracting files')
        zifi = zipfile.ZipFile(fpath)
        zifi.extractall()
        self.logging('Finished extracting files')
        self.logging('Removing temp file')
        try:
            remove_file(fpath)
        except Exception as e:
            print(e)

    def check_update_thread(self, *args):
        Thread(target=self.check_update, kwargs=({'thread':True})).start()

    def check_update(self, thread=False):
        result = False
        self.threaded_update = thread
        f = open(self.version_path, 'r')
        own_ver = int(f.read())
        f.close()
        self.logging('Checked version, is %s' % (own_ver))
        r = requests.get(self.http_path)
        builds = self.find_http_zips(r.text)
        self.own_ver = own_ver
        self.builds = builds
        if builds != []:
            if builds[-1]['ver'] > own_ver:
                result = True
                for x in self.on_check_update:
                    x(True)
                self.logging('Found new version %s' % builds[-1]['ver'])
                if self.autoupdate:
                    self.update()
                elif self.prompts:
                    Clock.schedule_once(lambda x: self.update_dialog(own_ver, builds[-1]['ver']), 0)
            else:
                self.logging('No update available')
        else:
            self.logging('Update list is empty')
        if result == False:
            for x in self.on_check_update:
                x(False)

    def _update(self, *args):
        result = False
        if self.builds == []:
            raise Exception('No builds updates available, did you forget to check_update()?')
            self.logging('No builds updates available, did you forget to check_update()?')
        try:
            self.download_file(self.builds[-1]['link'])
            self.extract_files(fpath=self.update_path+'temp.zip')
            if self.prompts:
                Clock.schedule_once(lambda x: self.update_done_dialog(self.own_ver, self.builds[-1]['ver']), 0)
            result = True
        except Exception as e:
            self.logging('Update crashed')
            self.logging(traceback.format_exc())
        for x in self.on_update:
            x(result)

    def update(self, *args):
        if self.threaded_update:
            Thread(target=self._update).start()
        else:
            self._update()

    def update_dialog(self, cur_build, upd_build):
        popup = Popup(title='Update', content=ScrollView(), size_hint=(0.8,None), height=cm(5))
        grid = GridLayout(cols=1, spacing=0, size_hint_y=None)
        grid.bind(minimum_height= grid.setter('height'))
        con = StackLayout()
        grid.add_widget(con)
        popup.content.add_widget(grid)
        lbl1 = Label(text='Current build is %s' % (cur_build), size_hint_y=None, height=cm(1))
        lbl2 = Label(text='Build %s available' % (upd_build), size_hint_y=None, height=cm(1))
        btn1 = Button(text='Cancel', size_hint=(0.5, None), height=cm(1))
        btn2 = Button(text='Update', size_hint=(0.5, None), height=cm(1))
        btn1.bind(on_release=popup.dismiss)
        btn2.bind(on_release=lambda x: {self.update(), popup.dismiss()})
        for x in (lbl1, lbl2, btn1, btn2):
            con.add_widget(x)
        popup.open()

    def update_done_dialog(self, cur_build, upd_build):
        popup = Popup(title='Update done', content=ScrollView(), size_hint=(0.8,None), height=cm(5))
        grid = GridLayout(cols=1, spacing=0, size_hint_y=None)
        grid.bind(minimum_height= grid.setter('height'))
        con = StackLayout()
        grid.add_widget(con)
        popup.content.add_widget(grid)
        lbl1 = Label(text='Done updating from %s to %s' % (cur_build, upd_build), size_hint_y=None, height=cm(1))
        btn1 = Button(text='Close', size_hint=(1, None), height=cm(1))
        btn1.bind(on_release=popup.dismiss)
        for x in (lbl1, btn1):
            con.add_widget(x)
        popup.open()
