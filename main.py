import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication , QMainWindow , QLabel
from PyQt5.QtGui import QIcon , QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Main Window Config
        self.setWindowTitle("Music Player")
        self.setGeometry(300, 300, 800, 600)
        self.setWindowIcon(QIcon("icon.png")) #------------NOTE----- modfiy the icon picture


        #Label -1 Config
        label = QLabel("Hello World" , self)
        label.setFont(QFont("Arial", 20))
        label.setGeometry(0 , 0 , 500 , 100)
        label.setStyleSheet("background-color: rgb(255, 255, 255);  color: blue;")



def main ():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()