from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QCursor
from app.src._database_manager import rand_query
from app.src._phonetic_manager import phon_to_word
from app.src._voice_manager import play_sound, down_sound


def create_label(text, alignment=Qt.AlignCenter):
    label = QLabel(text)
    label.setAlignment(alignment)
    label.setStyleSheet('font: 75 20pt "Comic Sans MS";')
    return label


def create_button(text, click_handler):
    button = QPushButton(text)
    button.setStyleSheet('font: 75 20pt "Comic Sans MS";')
    button.clicked.connect(click_handler)
    button.setCursor(QCursor(Qt.PointingHandCursor))
    button.setMaximumHeight(40)
    return button


class BgWordManager(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(self.main_window.icon_2)
        self.timer = None
        self.sound_button_1 = None
        self.sound_button_2 = None
        self.phonetic_label_1 = None
        self.phonetic_label_2 = None
        self.en_label = None
        self.us_label = None
        self.input_edit = None
        self.result_label = None
        self.question_label = None
        self.next_button = None
        self.skip_button = None
        self.correct_word = None
        self.current_word = None
        self.phonetics = None
        self.clickCount = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'{self.main_window.minute_} DAKİKADA BİR KELİME')

        self.question_label = create_label(self.current_word)

        self.input_edit = QLineEdit(self)
        self.input_edit.setStyleSheet('font: 75 20pt "Comic Sans MS";')
        self.input_edit.returnPressed.connect(self.check_word)

        self.result_label = create_label('')

        self.en_label = create_label('İngiliz Aksanı')
        self.en_label.setStyleSheet("font: 75 20pt 'Comic Sans MS';"
                                    "text-decoration: underline;")
        self.en_label.setFixedSize(220, 40)
        self.us_label = create_label('Amerikan Aksanı')
        self.us_label.setStyleSheet("font: 75 20pt 'Comic Sans MS';"
                                    "text-decoration: underline;")
        self.us_label.setFixedSize(220, 40)
        self.phonetic_label_1 = create_label('')
        self.phonetic_label_2 = create_label('')

        self.skip_button = create_button('Kelimeyi Değiştir', self.change_word)
        self.next_button = create_button('Sonraki Kelime İçin Bekle', self.next_time)

        self.sound_button_1 = create_button('', lambda: self.run_voice('EN'))
        self.sound_button_1.setIcon(self.main_window.icon_4)
        self.sound_button_1.setIconSize(QSize(40, 40))
        self.sound_button_1.setFixedSize(35, 35)

        self.sound_button_2 = create_button('', lambda: self.run_voice('US'))
        self.sound_button_2.setIcon(self.main_window.icon_5)
        self.sound_button_2.setIconSize(QSize(40, 40))
        self.sound_button_2.setFixedSize(35, 35)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout_2 = QHBoxLayout()
        layout_list = [self.question_label, self.input_edit, self.result_label, self.sound_button_1,
                       self.en_label, self.us_label, self.sound_button_2, self.phonetic_label_1,
                       self.phonetic_label_2, self.skip_button, self.next_button]
        c = 0
        for i in layout_list:
            if c == 3:
                layout.addLayout(hlayout)
                layout.addLayout(hlayout_2)
                hlayout.addWidget(layout_list[3])
                hlayout.addWidget(layout_list[4])
                hlayout.addWidget(layout_list[5])
                hlayout.addWidget(layout_list[6])
                hlayout_2.addWidget(layout_list[7])
                hlayout_2.addWidget(layout_list[8])
                layout.addWidget(layout_list[9])
                layout.addWidget(layout_list[10])
                break
            layout.addWidget(i)
            c += 1

        self.setLayout(hlayout)
        self.setLayout(hlayout_2)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.ended_timer)
        self.clickCount = 0

        self.select_word()
        self.setGeometry(400, 400, 350, 450)
        self.setMaximumSize(620, 580)
        self.show()

    def select_word(self):
        self.input_edit.setEnabled(True)
        self.current_word, self.correct_word, *self.phonetics = rand_query()
        self.question_label.setText(self.current_word)
        list_ = [self.input_edit, self.result_label,
                 self.phonetic_label_1, self.phonetic_label_2]
        for i in list_:
            i.setText('')

    def check_word(self):
        input_word = self.input_edit.text()
        if input_word:
            if input_word == self.correct_word:
                self.result_label.setText('Cevap Doğru')
                self.input_edit.setEnabled(False)
                self.get_phonetic()
            else:
                self.result_label.setText(f'Cevap Yanlış : {self.correct_word}')
                self.input_edit.setEnabled(False)

    def get_phonetic(self):
        if self.phonetics[0] is not None:
            self.phonetic_label_1.setText(self.phonetics[0])
            self.phonetic_label_2.setText(self.phonetics[1])
        else:
            phon = phon_to_word(self.current_word)
            if phon == "wrong":
                phon = phon_to_word(self.correct_word)
            if phon is None or phon == 'wrong':
                self.phonetic_label_1.setText("Fonetik")
                self.phonetic_label_2.setText("bulunamadı")
            else:
                self.phonetic_label_1.setText(phon[0])
                self.phonetic_label_2.setText(phon[1])

    def change_word(self):
        self.clickCount += 1
        if self.clickCount >= 3:
            self.next_time()
            self.clickCount = 0
        else:
            self.select_word()

    def get_voice(self, x):
        voice = play_sound(self.current_word, x)
        if not voice:
            voice = play_sound(self.correct_word, x)
        if not voice:
            voice = down_sound(self.current_word, x)
        if not voice:
            voice = down_sound(self.correct_word, x)
        if not voice:
            self.input_edit.setText('Kelime Bulunamadı')
        self.en_able_button()

    def dis_able_button(self):
        self.sound_button_1.setEnabled(False)
        self.sound_button_2.setEnabled(False)

    def en_able_button(self):
        self.sound_button_1.setEnabled(True)
        self.sound_button_2.setEnabled(True)

    def run_voice(self, x):
        self.dis_able_button()
        self.get_voice(x)

    def next_time(self):
        self.timer.start(self.main_window.minute_ * 60000)   # ------
        self.hide()

    def ended_timer(self):
        self.timer.stop()
        self.select_word()
        self.show()

    def closeEvent(self, event):
        self.main_window.show_main_window()
        event.accept()
