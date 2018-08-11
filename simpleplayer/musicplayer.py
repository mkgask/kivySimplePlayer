# coding: utf-8

from os.path import basename

from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from kivy.clock import Clock
from decimal import Decimal, ROUND_HALF_UP

from simpleplayer.popupchoosefile import PopupChooseFile

class MusicPlayer(BoxLayout):
    sound_path = ''
    sound = None
    popup = None
    is_playing = False
    is_manual_stop = False
    is_repeating = False
    pause_pos = 0
    value_before = 0
    lengh = 0

    def __init__(self, **kwargs):
        print('__init__')
        super(MusicPlayer, self).__init__(**kwargs)

        self._file = Window.bind(
            on_dropfile = self._on_file_drop
        )

    def _on_file_drop(self, window, file_path):
        print('_on_file_drop')
        self.select(file_path.decode('utf-8'))
        return

    def choose(self):
        print('choose')
        content = PopupChooseFile(select=self.select, cancel=self.cancel)
        self.popup = Popup(title='Select Music', content=content)
        self.popup.open()

    def cancel(self):
        print('cancel')
        self.popup.dismiss()

    def select(self, path):
        print('select')
        if self.sound:
            self._stop()
        
        self.sound = SoundLoader.load(path)
        self.sound_path = path
        # self.sound_name = basename(path).encode('utf-8')
        self.sound_name = basename(path)
        self.sound.on_stop = self._on_stop

        self.time_bar.max = self.sound.length

        try:
            self._volume(50)
            self._start()
#        except AttributeError:
#            self.status.text = 'shold mp3'
        finally:
            if self.popup:
                self.popup.dismiss()

    def _on_stop(self):
        print('_on_stop')
        if 0 < self.pause_pos:
            self._on_sound_pause()
        else:
            self._on_sound_stop()
        return

    def _on_sound_pause(self):
        print('_on_sound_pause')
        return

    def _on_sound_stop(self):
        print('_on_sound_stop')
        print('self.is_manual_stop: ' + str(self.is_manual_stop))
        print('self.is_repeating: ' + str(self.is_repeating))

        if self.is_manual_stop or not self.is_repeating:    # <- 変更
            # 手動停止またはリピート再生なしの時はリピート再生しない
            print('_on_sound_stop(): Stop')
            return

        # リピート再生
        print('_on_sound_stop(): Repeat start')
        self._start()
        return

    def repeat_mode_toggle(self):
        if self.is_repeating:
            self.is_repeating = False
            self.repeat_button.text = 'リピートなし'
        else:
            self.is_repeating = True
            self.repeat_button.text = 'リピート'
        return

    def play_or_stop(self):
        print('play_or_stop')
        if not self.sound:
            self.status.text = 'Select music file'
            return

        if self.sound.state == "play":
            self._pause()
        elif self.sound.state == 'stop':
            #self._restart()
            self._start()

    def stop(self):
        print('stop')
        if self.is_playing:
            self.is_manual_stop = True
            self._stop()

    def time_change(self, value):
        if not self.sound:
            self.status.text = 'Select music file'
        elif self.is_playing and value != self.value_before + 0.1:
            #self._pause()
            #self._restart(value)
            print(value)
            self.sound.seek(value)
        elif not self.is_playing:
            print('value: ' + str(value))
            self.pause_pos = value
            self.time_bar.value = value
            print('pause_pos save: ' + str(self.pause_pos))

            self.time_text.text = self._time_string(
                self.time_bar.value,
                self.lengh
            )

    def volume_change(self, value):
        self._volume(value)

    def _time_string(self, now, end):
        now_m, now_s = map(int, divmod(now, 60))
        now_str = "{0}:{1:02d}".format(now_m, now_s)

        end_m, end_s = map(int, divmod(end, 60))
        end_str = "{0}:{1:02d}".format(end_m, end_s)
        
        return "{}/{}".format(now_str, end_str)

    def _timer(self, val):
        if not self.sound:
            return False
        elif self.time_bar.max <= self.time_bar.value:
            self._stop()
            return False
        else:
            self.value_before = self.time_bar.value
            self.time_bar.value += 0.1

            self.time_text.text = self._time_string(
                self.time_bar.value,
                self.lengh
            )

    def _volume(self, vol):
        print('_volume')
        vol = round(vol)
        vol_value = vol / 100

        self.volume_text.text = str(vol)
        self.volume_bar.value = vol

        if not self.sound:
            return

        self.sound.volume = vol_value

    def _start(self):
        print('_start')

        self.sound.play()

        if 0 < self.pause_pos:
            print('pause_pos load: ' + str(self.pause_pos))
            self.sound.seek(self.pause_pos)

        self.is_playing = True
        self.is_manual_stop = False
        Clock.schedule_interval(self._timer, 0.1)

        self.play_button.text = 'ポーズ'
        self.status.text = 'Playing {}'.format(self.sound_name)

        self.lengh = self.sound.length
        self.pause_pos = 0

    def _restart(self, pos=None):
        print('_restart')
        self._start()
        self.sound.seek(pos if pos else self.pause_pos)
        self.pause_pos = 0

    def _stop(self, pause_pos=0):
        print('_stop')

        self.sound.stop()
        Clock.unschedule(self._timer)

        self.is_playing = False
        self.pause_pos = pause_pos
        self.time_bar.value = pause_pos
        
        self.time_text.text = self._time_string(
            self.time_bar.value,
            self.lengh
        )

        self.play_button.text = '再生'
        self.status.text = 'Stop {}'.format(self.sound_name)

    def _pause(self):
        print('_pause')
        pos = self.sound.get_pos() * 0.999
        print('pos save: ' + str(pos))
        self._stop(pause_pos=pos)
