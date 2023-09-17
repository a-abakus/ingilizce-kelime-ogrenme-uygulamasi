from PyQt5.QtWidgets import (QWidget, QLineEdit, QPushButton, QVBoxLayout, QDesktopWidget, QLabel, QHBoxLayout)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QSize
from app.src._voice_manager import to_pronun
from app.src._phonetic_manager import phon_to_pronun
from app.src._database_manager import select_query, word_is_exist


def create_button(text, click_handler):
    button = QPushButton(text)
    button.setStyleSheet('font: 75 20pt "Comic Sans MS";')
    button.setCursor(QCursor(Qt.PointingHandCursor))
    button.clicked.connect(click_handler)
    return button


def create_label(text, alignment=Qt.AlignCenter):
    label = QLabel(text)
    label.setAlignment(alignment)
    label.setStyleSheet('font: 75 20pt "Comic Sans MS";')
    return label


class MyPronounApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(self.main_window.icon_3)
        self.sound_1 = None
        self.sound_2 = None
        self.label_3 = None
        self.label_4 = None
        self.input = None
        self.label = None
        self.label_2 = None
        self.voice_1_button = None
        self.voice_2_button = None
        self.back_button = None
        self.phons = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Telaffuz Öğren')
        self.input = QLineEdit(self)
        self.input.setPlaceholderText('İngilizce Kelime Gir..')
        self.input.setStyleSheet('font: 75 20pt "Comic Sans MS";')
        self.input.returnPressed.connect(self.check_word)
        self.label = create_label('')
        self.label_2 = create_label('')
        self.sound_1 = create_button('', lambda: self.get_voice('EN'))
        self.sound_1.setIcon(self.main_window.icon_6)
        self.sound_1.setIconSize(QSize(30, 30))
        self.sound_1.setFixedSize(40, 40)
        self.sound_2 = create_button('', lambda: self.get_voice('US'))
        self.sound_2.setIcon(self.main_window.icon_6)
        self.sound_2.setIconSize(QSize(30, 30))
        self.sound_2.setFixedSize(40, 40)
        self.label_3 = create_label('  İngiliz Aksanı       ->')
        self.label_3.setFixedSize(260, 40)
        self.label_4 = create_label('  Amerikan Aksanı  ->')
        self.label_4.setFixedSize(260, 40)
        self.back_button = create_button('<-', self.back)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout_2 = QHBoxLayout()
        hlayout_3 = QHBoxLayout()
        layout.addWidget(self.input)
        layout.addLayout(hlayout)
        hlayout.addWidget(self.sound_1)
        hlayout.addWidget(self.label_3)
        hlayout.addWidget(self.label)
        layout.addLayout(hlayout_2)
        hlayout_2.addWidget(self.sound_2)
        hlayout_2.addWidget(self.label_4)
        hlayout_2.addWidget(self.label_2)
        layout.addLayout(hlayout_3)
        hlayout_3.addWidget(self.back_button)
        self.setLayout(hlayout)
        self.setLayout(hlayout_2)
        self.setLayout(layout)
        self.setLayout(hlayout_3)

        self.setGeometry(350, 350, 500, 350)
        self.setMaximumSize(700, 350)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def check_word(self):
        if self.input.text().isspace() or not self.input.text():
            self.input.setPlaceholderText('Kelime Gir!')
        else:
            p = word_is_exist(self.input.text(), 0) or word_is_exist(self.input.text(), 1)
            if not p:
                self.phons = phon_to_pronun(self.input.text(), "not")
                self.is_none(self.phons)
            else:
                self.phons = select_query(self.input.text(), 0)
                if len(self.phons) == 0 or self.phons is None:
                    self.phons = select_query(self.input.text(), 1)
                if self.phons[0] is None:
                    self.phons = phon_to_pronun(self.input.text(), "add")
                    self.is_none(self.phons)
                else:
                    self.is_none(self.phons)

    def is_none(self, x):
        if x is None:
            self.input.clear()
            self.input.setPlaceholderText('Fonetik Okunuş Bulunamadı.!')
            self.label.clear()
            self.label_2.clear()
        else:
            self.label.setText(x[0])
            self.label_2.setText(x[1])

    def get_voice(self, x):
        self.dis_able_button()
        if not self.input.text():
            self.input.setPlaceholderText('İngilizce Kelime Gir!')
        else:
            if x == 'EN':
                res = to_pronun(self.input.text(), 'EN')
            else:
                res = to_pronun(self.input.text(), 'US')
            if res is False:
                self.input.setPlaceholderText('Kelime Bulunamadı.!')
        self.check_word()
        self.en_able_button()

    def dis_able_button(self):
        self.sound_1.setEnabled(False)
        self.sound_2.setEnabled(False)

    def en_able_button(self):
        self.sound_1.setEnabled(True)
        self.sound_2.setEnabled(True)

    def back(self):
        self.close()

    def closeEvent(self, event):
        self.main_window.show_main_window()
        event.accept()
