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
from kivy.graphics import Color, Line
from kivy.uix.label import Label
from kivy.config import Config
import random
import paho.mqtt.client as mqtt
import json

class AppWidget(BoxLayout):
    control_center_x = 300
    control_center_y = 300
    control_outer_radius = 100
    control_inner_radius = 20
    previews_center_x = control_center_x
    previews_center_y = control_center_y
    def __init__(self, **kwargs):
        super(AppWidget, self).__init__(**kwargs)
        self.label = Label()
        self.add_widget(self.label)
        Window.bind(on_touch_move=self.mouse_pos, on_touch_up=self.mouse_reset)

    def mouse_reset(self, window, pos):
        self.previews_center_x = self.control_center_x
        self.previews_center_y = self.control_center_y
        self.canvas.clear()


        self.send_command(0, 0)
        with self.canvas:
            Label(text = str(int(pos.pos[0])) + ' - ' + str(int(pos.pos[1])) + ' Forward: 0 - Direction: 0', pos=[100, 100])
            Color(0.2, 0.5, 0.2)
            Line(circle=[self.control_center_x, self.control_center_y, self.control_outer_radius])
            Line(circle=[self.control_center_x, self.control_center_y, self.control_inner_radius])
    def compute_power(self, x, y):
        direction = float(x - self.control_center_x) * 100. / float(self.control_outer_radius)
        forward = float(y - self.control_center_y) * 100. / float(self.control_outer_radius)
        return [forward, direction]
    def mouse_pos(self, window, pos):
        #c1 = self.ids['cerc1']
        #c1.circle = [600, 600, 100]
        self.canvas.clear()
        with self.canvas:
            ctl = self.mouse_inner(int(pos.pos[0]),int(pos.pos[1]))
            dir = self.compute_power(int(ctl[0]),int(ctl[1]))
            self.send_command(dir[0], dir[1])
            Label(text = str(int(ctl[0])) + ' - ' + str(int(ctl[1])) + ' Forward: ' + str(dir[0]) + ' - Direction: ' + str(dir[1]), pos=[100, 100])
            Color(0.2, 0.5, 0.2)
            Line(circle=[self.control_center_x, self.control_center_y, self.control_outer_radius])
            Line(circle=[ctl[0], ctl[1], self.control_inner_radius])
            Line(points=[300, 300, ctl[0], ctl[1]])
    def mouse_inner(self, x, y):
        dx = abs(x - self.control_center_x)
        dy = abs(y - self.control_center_y)
        if dx ** 2 + dy ** 2 <= self.control_outer_radius ** 2:
            self.previews_center_x = x
            self.previews_center_y = y
            return [x, y]
        else:
            return [self.previews_center_x, self.previews_center_y]
    #def do_action(self, *args):

    #    lbl = self.ids['id_mouse_pos']
    #    lbl.text = 'aaaa'

    def send_command(self, forward, direction):
        client = mqtt.Client()
        client.connect("192.168.1.22", 1883, 60)
        client.publish("control/motor", json.dumps([forward, direction]))
        client.disconnect()

class MainApp(App):
    title = "Kivy Mouse Pos Demo"
    Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '800')

    def build(self):
        return AppWidget()


MainApp().run()