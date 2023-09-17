from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QVBoxLayout, QDesktopWidget, QInputDialog, QMessageBox)
from PyQt5.QtGui import QCursor, QIcon
from os import path, makedirs
from sys import exit, argv
from PyQt5.QtCore import Qt, QEvent
from app.src._word_manager import MyWordApp
from app.src._pronunciation import MyPronounApp
from app.src._bg_word_manager import BgWordManager
from app.src._database_manager import connection_close


def make_dirs():
    _path = path.join('assets', 'sounds')
    if not path.exists(_path):
        makedirs(_path)


def center_window(window):
    framegm = window.frameGeometry()
    screen = QDesktopWidget().screenGeometry()
    x = screen.width() / 2 - framegm.width() / 2
    y = screen.height() / 2 - framegm.height() / 2
    window.move(int(x), int(y))


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.icon_1 = QIcon(path.join('assets', 'icons', 'main_icon.png'))
        self.setWindowIcon(self.icon_1)
        self.bg_window = None
        self.word_window = None
        self.pronoun_window = None
        self.pronoun_button = None
        self.word_button = None
        self.bg_word_button = None
        self.change_button = None
        self.minute_ = None
        self.word = None

        self.icon_2 = QIcon(path.join('assets', 'icons', 'word_icon.png'))
        self.icon_3 = QIcon(path.join('assets', 'icons', 'voice_icon.png'))

        self.icon_4 = QIcon(path.join('assets', 'icons', 'sound.png'))
        self.icon_5 = QIcon(path.join('assets', 'icons', 'sound_2.png'))
        self.icon_6 = QIcon(path.join('assets', 'icons', 'sound.jpg'))

        self.ui = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Seç')

        self.word_button = self.create_button('KELİME ÖĞREN', self.open_word_window)

        self.bg_word_button = QPushButton('\'x\' DAKİKADA BİR KELİME')
        self.bg_word_button.setStyleSheet('font: 75 17pt "Comic Sans MS";')
        self.bg_word_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.bg_word_button.setFixedSize(350, 60)
        self.bg_word_button.clicked.connect(self.bg_word_button_click)

        self.pronoun_button = self.create_button('TELAFFUZ ÖĞREN', self.open_pronoun_window)

        self.change_button = QPushButton('Dakikayı Değiştir')
        self.change_button.setStyleSheet('font: 75 11pt  "Comic Sans MS";')
        self.change_button.clicked.connect(self.change_minute)
        self.change_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.change_button.setFixedSize(350, 25)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout_2 = QVBoxLayout()
        layout.addWidget(self.word_button)
        layout.addLayout(layout_2)
        layout_2.addWidget(self.bg_word_button)
        layout_2.addWidget(self.change_button)
        layout.addWidget(self.pronoun_button)
        central_widget.setLayout(layout_2)
        central_widget.setLayout(layout)

        make_dirs()
        self.setGeometry(350, 350, 375, 350)
        self.setFixedSize(375, 350)
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
        button.setFixedSize(350, 60)
        return button

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            obj.setStyleSheet('font: 75 23pt "Comic Sans MS";')
        elif event.type() == QEvent.Leave:
            obj.setStyleSheet('font: 75 20pt "Comic Sans MS";')
        return super().eventFilter(obj, event)

    def show_main_window(self):
        self.show()

    def bg_word_button_click(self):
        if self.bg_window is None or not self.bg_window.isVisible():
            if self.minute_ is None:
                self.input_minute()
            else:
                self.open_bg_window()

    def input_minute(self):
        get_minute, ok = QInputDialog.getInt(self, "Dakika Belirleme", "Kaç dakikada bir kelime gelsin?:")
        if ok:
            if get_minute < 1:
                QMessageBox.warning(self, "Uyarı", "Hatalı sayı girdiniz!")
                self.minute_ = None
            else:
                self.minute_ = get_minute
                self.open_bg_window()

            if self.minute_ is not None and self.minute_ > 0:
                self.bg_word_button.setText(f'\'{self.minute_}\' DAKİKADA BİR KELİME')
            else:
                if self.minute_ is None:
                    self.bg_word_button.setText(f'\'x\' DAKİKADA BİR KELİME')

    def change_minute(self):
        get_minute, ok = QInputDialog.getInt(self, "Dakika Belirleme", "Kaç dakikada bir kelime gelsin?:")
        if ok:
            if get_minute < 1:
                QMessageBox.warning(self, "Uyarı", "Hatalı sayı girdiniz!")
                self.minute_ = None
            else:
                self.minute_ = get_minute

            if self.minute_ is not None and self.minute_ > 0:
                self.bg_word_button.setText(f'\'{self.minute_}\' DAKİKADA BİR KELİME')
            else:
                self.bg_word_button.setText(f'\'x\' DAKİKADA BİR KELİME')

    def open_word_window(self):
        self.word_window = MyWordApp(self)
        center_window(self.word_window)
        self.word_window.show()
        self.hide()

    def open_bg_window(self):
        self.bg_window = BgWordManager(self)
        center_window(self.bg_window)
        self.bg_window.show()
        self.hide()

    def open_pronoun_window(self):
        self.pronoun_window = MyPronounApp(self)
        center_window(self.pronoun_window)
        self.pronoun_window.show()
        self.hide()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Çıkış", "Uygulamayı kapatmak istiyor musunuz?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            connection_close()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(argv)
    app.setStyle("fusion")
    main_window = MyMainWindow()
    exit(app.exec_())
