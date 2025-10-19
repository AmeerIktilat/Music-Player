from PyQt5 import QtWidgets
from music_player_window import MusicPlayerWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MusicPlayerWindow()
    window.show()
    app.exec_()