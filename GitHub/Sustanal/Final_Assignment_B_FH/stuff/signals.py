from PyQt5 import QtCore


class Signals(QtCore.QObject):
    """
    This class is a container for all signals. The typical format is like this:
    action_taken = QtCore.pyqtSignal(TYPE, IF ANY)
    """
    bet_placed = QtCore.pyqtSignal()


signals = Signals()  # create single instance