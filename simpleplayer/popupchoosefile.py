# encoding: utf-8

from os.path import dirname, abspath

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class PopupChooseFile(BoxLayout):
    current_dir = dirname(abspath(__file__))
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

