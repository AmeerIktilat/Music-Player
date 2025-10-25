
import sys
from PyQt5 import QtWidgets
from music_player_window import MusicPlayerWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MusicPlayerWindow()
    window.show()
    sys.exit(app.exec_())