from PyQt5 import QtWidgets

from . roulette import game
from . signals import signals


class ButtonWidget(QtWidgets.QWidget):
    """ The buttons to play the game."""

    def __init__(self, parent=None):
        super(ButtonWidget, self).__init__(parent)  # call superclass constructor

        # Buttons
        self.button_black = QtWidgets.QPushButton("Black")
        self.button_red = QtWidgets.QPushButton("Red")
        self.button_green = QtWidgets.QPushButton("Green")
        
        # Button styling
        self.button_black.setStyleSheet("color: white; font: bold 16px; background-color: black")
        self.button_red.setStyleSheet("color: white; font: bold 16px; background-color: red")
        self.button_green.setStyleSheet("color: white; font: bold 16px; background-color: green")

        # Layout (horizontal)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.button_black)
        self.layout.addWidget(self.button_red)
        self.layout.addWidget(self.button_green)
        self.setLayout(self.layout)

        # event handling
        self.button_red.clicked.connect(lambda: self.button_clicked('red'))
        self.button_black.clicked.connect(lambda: self.button_clicked('black'))
        self.button_green.clicked.connect(lambda: self.button_clicked('green'))

    def button_clicked(self, color):
        print('Clicked Button: {}'.format(color))
        game.place_bet(color)  # interacting with the game... in a larger program this should be handled by a controller 
        print('Win? {}'.format(game.result))
        signals.bet_placed.emit()  # signal emitted
