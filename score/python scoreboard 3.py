import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.text import LabelBase
import os

# Register the custom font
font_path = './font/Liliita.ttf'
if os.path.exists(font_path):
    LabelBase.register(name='Liliita', fn_regular=font_path)
else:
    print("Font file not found: {}".format(font_path))
    exit(1)

class EditableLabel(TextInput):
    def __init__(self, text='', max_length=10, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.text = text
        self.max_length = max_length  # Maximum length allowed for input
        self.background_color = (0, 0, 0, 0)
        self.font_name = 'Liliita'
        self.font_size = '40sp'
        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0, 0, 0, 1)
        self.padding = [20, 10]

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_length:
            substring = substring[:self.max_length - len(self.text)]
        super().insert_text(substring, from_undo=from_undo)

    def on_focus(self, instance, value):
        if value:  # When focused (clicked)
            self.text = ''  # Clear current text for editing
        else:  # When focus lost (edited)
            if not self.text.strip():  # Restore original text if nothing entered
                self.text = self.original_text

class ScoreboardApp(App):
    def build(self):
        self.player1_score = 0
        self.player2_score = 0

        # Set window configuration
        Config.set('graphics', 'resizable', '0')  # Fixed window size
        Window.size = (1493, 887)  # Initial window size

        layout = FloatLayout()

        # Load and scale the background image
        background = Image(source='./image/dama_bg.png', allow_stretch=True, keep_ratio=False, size_hint=(None, None), size=(1493, 887))
        layout.add_widget(background)

        # Player 1 editable label with max length of 10 characters
        self.player1_label = EditableLabel(text='Player 1', max_length=10, size_hint=(None, None), size=(500, 300), pos=(350, 530))
        self.player1_label.bind(focus=self.on_player1_label_edit)
        layout.add_widget(self.player1_label)

        self.player1_score_label = Label(text='0 pts', font_name='Liliita', font_size='40sp', size_hint=(None, None), size=(150, 100), pos=(50, 747), color=(0, 0, 0, 1))
        layout.add_widget(self.player1_score_label)

        # Player 2 editable label with max length of 10 characters
        self.player2_label = EditableLabel(text='Player 2', max_length=10, size_hint=(None, None), size=(500, 300), pos=(950, 530))
        self.player2_label.bind(focus=self.on_player2_label_edit)
        layout.add_widget(self.player2_label)

        self.player2_score_label = Label(text='0 pts', font_name='Liliita', font_size='40sp', size_hint=(None, None), size=(150, 100), pos=(1300, 747), color=(0, 0, 0, 1))
        layout.add_widget(self.player2_score_label)

        # Buttons for score handling
        button1_add = Button(text='+1', font_size='20sp', size_hint=(None, None), size=(100, 50), pos=(80, 680), color=(0, 0, 0, 1))
        button1_add.bind(on_press=self.increment_player1)
        layout.add_widget(button1_add)

        button1_subtract = Button(text='-1', font_size='20sp', size_hint=(None, None), size=(100, 50), pos=(80, 630), color=(0, 0, 0, 1))
        button1_subtract.bind(on_press=self.decrement_player1)
        layout.add_widget(button1_subtract)

        button2_add = Button(text='+1', font_size='20sp', size_hint=(None, None), size=(100, 50), pos=(1320, 680), color=(0, 0, 0, 1))
        button2_add.bind(on_press=self.increment_player2)
        layout.add_widget(button2_add)

        button2_subtract = Button(text='-1', font_size='20sp', size_hint=(None, None), size=(100, 50), pos=(1320, 630), color=(0, 0, 0, 1))
        button2_subtract.bind(on_press=self.decrement_player2)
        layout.add_widget(button2_subtract)

        return layout

    def on_player1_label_edit(self, instance, value):
        if not value:  # When focus lost (edited)
            if not self.player1_label.text.strip():  # Restore original text if nothing entered
                self.player1_label.text = 'Player 1'

    def on_player2_label_edit(self, instance, value):
        if not value:  # When focus lost (edited)
            if not self.player2_label.text.strip():  # Restore original text if nothing entered
                self.player2_label.text = 'Player 2'

    def increment_player1(self, instance):
        self.player1_score += 1
        self.player1_score_label.text = f'{self.player1_score} pts'

    def decrement_player1(self, instance):
        if self.player1_score > 0:
            self.player1_score -= 1
            self.player1_score_label.text = f'{self.player1_score} pts'

    def increment_player2(self, instance):
        self.player2_score += 1
        self.player2_score_label.text = f'{self.player2_score} pts'

    def decrement_player2(self, instance):
        if self.player2_score > 0:
            self.player2_score -= 1
            self.player2_score_label.text = f'{self.player2_score} pts'

if __name__ == '__main__':
    ScoreboardApp().run()
