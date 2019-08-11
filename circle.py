'''
Circle Example
==============

This example exercises circle (ellipse) drawing. You should see sliders at the
top of the screen with the Kivy logo below it. The sliders control the
angle start and stop and the height and width scales. There is a button
to reset the sliders. The logo used for the circle's background image is
from the kivy/data directory. The entire example is coded in the
kv language description.
'''

from kivy.app import App


from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import random

class AppWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(AppWidget, self).__init__(**kwargs)
        self.label = Label()
        self.add_widget(self.label)
        Window.bind(on_touch_down=self.mouse_pos)

    def mouse_pos(self, window, pos):
        lbl = self.ids['id_mouse_pos']
        lbl.text = str(pos.pos)
        c1 = self.ids['cerc1']
        c1.circle = [600, 600, 100]

    def do_action(self, *args):

        lbl = self.ids['id_mouse_pos']
        lbl.text = 'aaaa'


class MainApp(App):
    title = "Kivy Mouse Pos Demo"

    def build(self):
        return AppWidget()


MainApp().run()