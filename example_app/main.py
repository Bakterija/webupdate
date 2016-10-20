from __future__ import print_function
from kivy.app import App
from kivy.utils import platform
import sys
if platform != 'android':
    sys.dont_write_bytecode = True
else:
    from jnius import autoclass, cast
from web_updater.apache_updater import ApacheUpdater
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.metrics import cm
from threading import Thread
from time import sleep
from sys import path
from webbrowser import open_new_tab
import traceback


class WebUpdate(StackLayout):
    running = True
    def __init__(self, **kwargs):
        super(WebUpdate, self).__init__(**kwargs)
        self.rv_append('Init Apache App')
        self.apu = ApacheUpdater()
        if platform == 'android':
            self.apu.version_path = path[4]+'/web_updater/version.txt'
            self.apu.update_path = path[4]+'/'
            self.ids.fcs.path = path[4]
        else:
            self.apu.version_path =path[0]+'/web_updater/version.txt'
            self.apu.update_path = path[0]+'/'
            self.ids.fcs.path = path[0]
        self.apu.http_path = 'http://localhost/'
        self.apu.logger = self.rv_append
        try:
            self.apu.check_update_thread()
        except:
            self.rv_append(traceback.format_exc())

        self.ids.pep_widget.on_pep1 = self.browse_pep1
        self.ids.pep_widget.on_pep8 = self.browse_pep8
        self.ids.pep_widget.on_pep249 = self.browse_pep249
        self.ids.pep_widget.on_pep255 = self.browse_pep255

    def rv_append(self, text):
        text = str(text)
        self.ids.rv.data.append({'text':text})
        self.ids.rv.refresh_from_data()

    def browse_pep1(self, *args):
        open_new_tab('https://www.python.org/dev/peps/pep-0001/')

    def browse_pep8(self, *args):
        open_new_tab('https://www.python.org/dev/peps/pep-0008/')

    def browse_pep249(self, *args):
        open_new_tab('https://www.python.org/dev/peps/pep-0249/')

    def browse_pep255(self, *args):
        open_new_tab('https://www.python.org/dev/peps/pep-0255/')


class WebUpdateApp(App):
    def build(self):
        self.looping = True
        self.root_widget = WebUpdate()
        return self.root_widget

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_stop(self):
        self.looping = False

if __name__ == '__main__':
    try:
        WebUpdateApp().run()
    except Exception as e:
        traceback.print_exc()
