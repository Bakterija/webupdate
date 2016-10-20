from __future__ import print_function
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
import random

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

kv = '''
#: import bba modules.label_button.LabelButton
<PepWidget>:
    pepsize: 0.1
    text: ['More colors now!', 'One', 'Last', 'Time']
    LabelButton:
        id: pep_label
        size_hint: None, None
        text: root.text[3]
        size: (root.width * root.pepsize), (root.height * root.pepsize)
        pos: 0, 0
        font_size: dp(0.25) * min(self.width, self.height)
        markup: True
        textcol: 1, 1, 1
        canvcol: 0.6, 0.2, 0.3
        on_release: root.browse_pep8()
        canvas.before:
            Color:
                rgb: self.canvcol
            Rectangle:
                pos: self.pos
                size: self.size
    LabelButton:
        id: pep_label2
        size_hint: None, None
        text: root.text[2]
        size: (root.width * (1 - root.pepsize)), (root.height * (1 - root.pepsize))
        font_size: dp(0.25) * min(self.width, self.height)
        markup: True
        pos: root.width - self.width, root.height - self.height
        textcol: 1, 1, 1
        canvcol: 0.3, 0.2, 0.6
        on_release: root.browse_pep1()
        canvas.before:
            Color:
                rgb: self.canvcol
            Rectangle:
                pos: self.pos
                size: self.size
    LabelButton:
        id: pep_label3
        size_hint: None, None
        text: root.text[1]
        size: pep_label.width, pep_label2.height
        font_size: dp(0.25) * min(self.width, self.height)
        pos: 0, root.height - self.height
        markup: True
        textcol: 1, 1, 1
        canvcol: 0.9, 0.8, 0.4
        on_release: root.browse_pep255()
        canvas.before:
            Color:
                rgb: self.canvcol
            Rectangle:
                pos: self.pos
                size: self.size
    LabelButton:
        id: pep_label4
        size_hint: None, None
        text: root.text[0]
        size: pep_label2.width, pep_label.height
        font_size: dp(0.25) * min(self.width, self.height)
        pos: root.width - self.width, 0
        markup: True
        textcol: 1, 1, 1
        canvcol: 0.2, 0.6, 0.3
        on_release: root.browse_pep249()
        canvas.before:
            Color:
                rgb: self.canvcol
            Rectangle:
                pos: self.pos
                size: self.size
'''

class PepWidget(FloatLayout):
    pep_colors = []
    on_pep8 = None
    on_pep1 = None
    on_pep249 = None
    on_pep255 = None
    def __init__(self, **kwargs):
        super(PepWidget, self).__init__(**kwargs)
        self.timer_size = 2
        self.timer_textcol = 2
        self.after_init()
        Clock.schedule_once(self.increase_size, 1)
        Clock.schedule_interval(self.text_color_animation, self.timer_textcol)
        Clock.schedule_interval(self.change_text_color, 0)
        # Clock.schedule_interval(lambda x: print(self.canvcol), 0.2)

    def after_init(self, *args):
        colors = [
            [1, 0.8, 0.8],
            [1, 0.5, 0],
            [0.5, 1, 0.3],
            [0, 0.5, 0.1],
            [0, 0.8, 1],
            [0.3, 0.3, 1],
            [1, 0.4, 1],
            [0.9, 0, 0.2],
            [0.8, 0, 0.7],
            [1, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ]
        for x in colors:
            self.pep_colors.append(x)

    def increase_size(self, *args):
        anim = Animation(pepsize=0.9, d=self.timer_size, t='in_out_circ')
        anim.start(self)
        Clock.schedule_once(self.reduce_size, self.timer_size)

    def reduce_size(self, *args):
        anim = Animation(pepsize=0.1, d=self.timer_size, t='in_out_circ')
        anim.start(self)
        Clock.schedule_once(self.increase_size, self.timer_size)

    def change_text_color(self, *args):
        for i, x in enumerate(self.children):
            rgbval = int(x.textcol[0]*255), int(x.textcol[1]*255), int(x.textcol[2]*255)
            color = rgb_to_hex(rgbval)
            x.text = '[color=%s]%s[/color]' % (color, self.text[i])

    def text_color_animation(self, *args):
        if self.pep_colors != []:
            for x in self.children:
                ran = random.randrange(0, len(self.pep_colors)-1)
                pc = self.pep_colors[ran]
                anim = Animation(textcol=[pc[0], pc[1], pc[2]], d=2)
                anim.start(x)

                ran = random.randrange(0, len(self.pep_colors)-1)
                pc = self.pep_colors[ran]
                anim = Animation(canvcol=[pc[0], pc[1], pc[2]], d=2)
                anim.start(x)

    def browse_pep1(self, *args):
        if self.on_pep1:
            self.on_pep1()

    def browse_pep8(self, *args):
        if self.on_pep8:
            self.on_pep8()

    def browse_pep249(self, *args):
        if self.on_pep249:
            self.on_pep249()

    def browse_pep255(self, *args):
        if self.on_pep255:
            self.on_pep255()

Builder.load_string(kv)
