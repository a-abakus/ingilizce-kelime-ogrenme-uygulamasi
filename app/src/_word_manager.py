from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDesktopWidget, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QCursor
from app.src._database_manager import rand_query
from app.src._phonetic_manager import phon_to_word
from app.src._voice_manager import play_sound, down_sound


def add_wrongs(x, y):
    with open('ozet.txt', 'a', encoding='utf-8') as f:
        f.write(f'{x} : {y} \n')


def create_label(text, alignment=Qt.AlignCenter):
    label = QLabel(text)
    label.setAlignment(alignment)
    label.setStyleSheet('font: 75 20pt "Comic Sans MS";')
    return label


class MyWordApp(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowIcon(self.main_window.icon_2)
        self.line_label = None
        self.sound_button_1 = None
        self.sound_button_2 = None
        self.phonetic_label = None
        self.phonetic_label_1 = None
        self.phonetic_label_2 = None
        self.check_button = None
        self.error_label = None
        self.skip_button = None
        self.add_button = None
        self.back_button = None
        self.en_label = None
        self.us_label = None
        self.input_edit = None
        self.result_label = None
        self.question_label = None
        self.correct_word = None
        self.current_word = None
        self.phonetics = None
        self.m_y = None
        self.m_x = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kelime Öğren')

        with open('ozet.txt', 'w'):
            pass

        self.m_x = 0
        self.m_y = 0

        self.question_label = create_label(self.current_word)
        self.result_label = create_label('')
        self.input_edit = QLineEdit(self)
        self.input_edit.setStyleSheet('font: 75 20pt "Comic Sans MS";')
        self.check_button = self.create_button('Cevabı Kontrol Et', self.check_word)
        self.input_edit.returnPressed.connect(self.check_button.click)
        self.add_button = self.create_button('Özet', self.add_summary)
        self.phonetic_label = create_label('Fonetik Telaffuz')
        self.phonetic_label.setStyleSheet("border: 1px solid gray; font: 75 20pt 'Comic Sans MS';"
                                          "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1,"
                                          "y2:1, stop:0 rgba(126, 100, 100, 255), stop:1 rgba(255, 255, 255, 255));")
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
        self.skip_button = self.create_button('Sonraki Kelime', self.select_word)
        self.error_label = create_label('')
        self.back_button = self.create_button('<-', self.back)
        self.line_label = QLabel(self)
        self.line_label.setText(' \n')

        self.sound_button_1 = self.create_button('', lambda: self.run_('EN'))
        self.sound_button_1.setIcon(self.main_window.icon_4)
        self.sound_button_1.setIconSize(QSize(40, 40))
        self.sound_button_1.setFixedSize(35, 35)

        self.sound_button_2 = self.create_button('', lambda: self.run_('US'))
        self.sound_button_2.setIcon(self.main_window.icon_5)
        self.sound_button_2.setIconSize(QSize(40, 40))
        self.sound_button_2.setFixedSize(35, 35)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout_2 = QHBoxLayout()
        layout_list = [self.question_label, self.input_edit, self.error_label, self.check_button,
                       self.result_label, self.line_label, self.phonetic_label, self.skip_button,
                       self.add_button, self.back_button, self.sound_button_1, self.en_label,
                       self.us_label, self.sound_button_2, self.phonetic_label_1, self.phonetic_label_2]
        c = 0
        for i in layout_list:
            if c == 13:
                break
            if 6 < c < 9:
                layout.addLayout(hlayout)
                layout.addLayout(hlayout_2)
                hlayout.addWidget(layout_list[10])
                hlayout.addWidget(layout_list[11])
                hlayout.addWidget(layout_list[12])
                hlayout.addWidget(layout_list[13])
                hlayout_2.addWidget(layout_list[14])
                hlayout_2.addWidget(layout_list[15])
                layout.addWidget(layout_list[5])
                c = 10
            layout.addWidget(i)
            c += 1
        del i

        self.setLayout(hlayout)
        self.setLayout(hlayout_2)
        self.setLayout(layout)

        self.select_word()
        self.setGeometry(400, 400, 350, 450)
        self.setMaximumSize(620, 580)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_button(self, text, click_handler):
        button = QPushButton(text)
        button.setStyleSheet('font: 75 20pt "Comic Sans MS";')
        button.clicked.connect(click_handler)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.installEventFilter(self)
        button.setMaximumHeight(40)
        return button

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            obj.setStyleSheet('font: 75 21pt "Comic Sans MS";')
        elif event.type() == QEvent.Leave:
            obj.setStyleSheet('font: 75 20pt "Comic Sans MS";')
        return super().eventFilter(obj, event)

    def select_word(self):
        self.en_able_check()
        self.current_word, self.correct_word, *self.phonetics = rand_query()
        self.question_label.setText(self.current_word)
        list_ = [self.input_edit, self.error_label, self.result_label,
                 self.phonetic_label_1, self.phonetic_label_2]
        for i in list_:
            i.setText('')

    def check_word(self):
        input_word = self.input_edit.text()
        if input_word:
            if input_word == self.correct_word:
                self.result_label.setText('Cevap Doğru')
                self.dis_able_check()
                self.m_x += 1
                self.get_phonetic()
            else:
                self.result_label.setText(f'Cevap Yanlış : {self.correct_word}')
                self.dis_able_check()
                add_wrongs(self.current_word, self.correct_word)
                self.m_y += 1

    def get_phonetic(self):
        if self.phonetics[0] is not None:
            self.phonetic_label_1.setText(self.phonetics[0])
            self.phonetic_label_2.setText(self.phonetics[1])
        else:
            phon = phon_to_word(self.current_word)
            if phon == "wrong":
                phon = phon_to_word(self.correct_word)
            if phon == "wrong" or phon is None:
                self.error_label.setText('Fonetik okunuş bulunamadı.')
            else:
                self.phonetic_label_1.setText(phon[0])
                self.phonetic_label_2.setText(phon[1])

    def dis_able_check(self):
        self.input_edit.setEnabled(False)
        self.check_button.setEnabled(False)

    def en_able_check(self):
        self.input_edit.setEnabled(True)
        self.check_button.setEnabled(True)

    def dis_able_button(self):
        self.sound_button_1.setEnabled(False)
        self.sound_button_2.setEnabled(False)

    def en_able_button(self):
        self.sound_button_1.setEnabled(True)
        self.sound_button_2.setEnabled(True)

    def run_(self, x):
        self.dis_able_button()
        self.get_voice(x)

    def get_voice(self, x):
        voice = play_sound(self.current_word, x)
        if not voice:
            voice = play_sound(self.correct_word, x)
        if not voice:
            voice = down_sound(self.current_word, x)
        if not voice:
            voice = down_sound(self.correct_word, x)
        if not voice:
            self.error_label.setText('Kelime Bulunamadı')
        self.en_able_button()

    def add_summary(self):
        with open('ozet.txt', 'a', encoding='utf-8') as f:
            f.write(f'\nDoğru Sayısı : {self.m_x}\nYanlış Sayısı : {self.m_y}\n')

    def back(self):
        self.close()

    def closeEvent(self, event):
        self.main_window.show_main_window()
        event.accept()
