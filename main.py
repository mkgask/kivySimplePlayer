# coding: utf-8

from os import environ

from kivy.app import App

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

resource_add_path('{}\\{}'.format(environ['SYSTEMROOT'], 'Fonts'))
LabelBase.register(DEFAULT_FONT, 'MSGOTHIC.ttc')

from simpleplayer.musicplayer import MusicPlayer

class MainWindow(App):
    def build(self):
        return MusicPlayer()

if __name__ == "__main__":
    MainWindow().run()