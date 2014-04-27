# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class TweetDialog(QtGui.QDialog):

    def __init__(self, window):
        super(TweetDialog, self).__init__(window)

        self.setWindowTitle(_fromUtf8("Score"))
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)

        self.label = QtGui.QLabel(_fromUtf8("Tweet this to log your score:"))
        self.layout.addWidget(self.label)

        self.tweet_box = QtGui.QLineEdit(self)
        self.tweet_box.setReadOnly(True)
        self.layout.addWidget(self.tweet_box)

    def set_tweet(self, count, media):
        TWEET_FMT = "@TadokuBot %d %s;"
        tweet_text = TWEET_FMT % (count, media)
        assert(len(tweet_text) <= 140)
        self.tweet_box.setText(tweet_text)
        self.tweet_box.selectAll()
