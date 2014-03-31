# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore, QtGui

from ui.tweet_dialog import TweetDialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class MainWindowUi(object):

    def __init__(self):
        super(MainWindowUi, self).__init__()

    def setup_ui(self, window):
        window.setWindowTitle(_fromUtf8("Tadoku Counter"))
        self.central_widget = QtGui.QWidget(window)
        window.setCentralWidget(self.central_widget)

        self.text_edit = QtGui.QTextEdit(self.central_widget)
        self.text_edit.setAcceptRichText(False)
        self.text_edit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self.central_widget)
        self.layout.addWidget(self.text_edit)

        self.buttons = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self.central_widget)

        self.setup_buttons(window)

        self.layout.addLayout(self.buttons)

    def setup_buttons(self, window):
        self.buttons.addStretch()

        self.media_group = QtGui.QButtonGroup()
        self.media_group.setExclusive(True)

        self.media_game = QtGui.QRadioButton(_fromUtf8("#game"))
        self.media_group.addButton(self.media_game)
        self.media_game.setChecked(True)
        self.media_fullgame = QtGui.QRadioButton(_fromUtf8("#fullgame"))
        self.media_group.addButton(self.media_fullgame)
        self.media_net = QtGui.QRadioButton(_fromUtf8("#net"))
        self.media_group.addButton(self.media_net)
        self.media_book = QtGui.QRadioButton(_fromUtf8("#book"))
        self.media_group.addButton(self.media_book)

        self.buttons.addWidget(self.media_game)
        self.buttons.addWidget(self.media_fullgame)
        self.buttons.addWidget(self.media_net)
        self.buttons.addWidget(self.media_book)
        
        self.count_button = QtGui.QPushButton(_fromUtf8("Count"))
        self.count_button.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttons.addWidget(self.count_button)

        self.clear_button = QtGui.QPushButton(_fromUtf8("Clear"))
        self.clear_button.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttons.addWidget(self.clear_button)
        
        self.save_button = QtGui.QPushButton(_fromUtf8("Save"))
        self.save_button.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttons.addWidget(self.save_button)
        
        self.buttons.addStretch()

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = MainWindowUi()
        self.ui.setup_ui(self)

        self.ui.count_button.clicked.connect(self.count)
        self.ui.clear_button.clicked.connect(self.clear)
        self.ui.save_button.clicked.connect(self.save)

        try:
            with open(os.path.join(os.getcwdu(), "sav", "_buffer.txt")) as f:
                raw = f.read()
                self.ui.text_edit.document().setPlainText(unicode(raw, "utf-8"))
        except IOError, e:
            # Can't open buffer file, may not exist yet.
            pass

    def count(self):
        chars = self.ui.text_edit.document().characterCount()
        media = {
            self.ui.media_game: '#game',
            self.ui.media_fullgame: '#fullgame',
            self.ui.media_net: '#net',
            self.ui.media_book: '#book',
        }[self.ui.media_group.checkedButton()]

        if media == '#game':
            chars_per_screen = 400.0 / 20.0
        elif media == '#fullgame':
            chars_per_screen = 400.0 / 6.0
        elif media in ('#net', '#book'):
            chars_per_screen = 400.0

        screens = round(chars / chars_per_screen)

        tweet_dialog = TweetDialog(self)
        tweet_dialog.set_tweet(screens, media)
        tweet_dialog.show()

    def clear(self):
        self.ui.text_edit.document().clear()

    def closeEvent(self, event):
        self.save()
        event.accept()

    def save(self):
        filename = os.path.join(os.getcwdu(), "sav", "_buffer.txt")
        try:
            with open(filename, 'wb') as f:
                data = unicode(self.ui.text_edit.document().toPlainText())
                f.write(data.encode("utf-8"))
        except IOError, e:
            print u"error: " + unicode(str(e), "utf-8")
            pass
