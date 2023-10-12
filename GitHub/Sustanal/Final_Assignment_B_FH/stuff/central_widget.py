from PyQt5 import QtWidgets, QtGui
from . signals import signals
from . roulette import game
from . button_widget import ButtonWidget


class CentralWidget(QtWidgets.QWidget):

    """
    Our central widget of the main window.
    """

    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)

        # image (shown usually via a QLabel)
        self.label = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap('image_roulette.jpg')
        self.label.setPixmap(self.pixmap)

        # label showing whether you won or lost
        initial_text = "Welcome to Roulette. Now place your bet!"
        self.label_win_loose = QtWidgets.QLabel(initial_text, self)
        self.label_win_loose.setStyleSheet("font: 30pt Comic Sans MS")

        # label showing statistics
        self.label_stats = QtWidgets.QLabel("Money: {}.".format(game.money), self)
        self.label_stats.setStyleSheet("font: 20pt Comic Sans MS; color: grey")

        # a widget with play buttons
        self.button_widget = ButtonWidget()

        # LAYOUT (vertical)
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.addWidget(self.label)
        self.vertical_layout.addWidget(self.label_win_loose)
        self.vertical_layout.addWidget(self.label_stats)
        self.vertical_layout.addWidget(self.button_widget)
        self.setLayout(self.vertical_layout)

        # connect signals
        signals.bet_placed.connect(self.update_labels)

    def update_labels(self):
        if game.result:
            self.label_win_loose.setText('Game color: {} - You win!'.format(game.color))
        else:
            self.label_win_loose.setText('Game color: {} - You loose'.format(game.color))
        self.label_stats.setText('Money: {}.  --- Stats (won/lost): {}/{}'.format(game.money, game.won, game.lost))