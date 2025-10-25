from PyQt5 import QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QRect, QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap
import os

from PyQt5.QtMultimedia import QMediaContent


class MenuPanel:
    def __init__(self, parent):
        self.parent = parent

        self.menuPanel = QtWidgets.QFrame(parent)
        self.menuPanel.setGeometry(0, 0, 120, parent.height())
        self.menuPanel.setStyleSheet("background-color: #3c2c5e;")
        self.menuPanel.hide()

        self.menuLayout = QtWidgets.QVBoxLayout(self.menuPanel)
        self.menuLayout.setContentsMargins(10, 10, 10, 10)
        self.menuLayout.setSpacing(10)

        self.titleLabel = QtWidgets.QLabel("♪ Songs")
        self.titleLabel.setStyleSheet("color: gold; font-size: 14px; font-weight: bold;")
        self.menuLayout.addWidget(self.titleLabel)

        self.songContainer = QtWidgets.QVBoxLayout()
        self.menuLayout.addLayout(self.songContainer)

        self.menuLayout.addStretch()

        self.backButton = QtWidgets.QPushButton("← Back")
        self.backButton.setStyleSheet("""
            QPushButton {
                background-color: #5a3d85;
                color: white;
                border-radius: 8px;
                font-size: 12px;
            }
        """)
        self.backButton.clicked.connect(self.toggle_menu)
        self.menuLayout.addWidget(self.backButton)

        self.songButtons = []

    def toggle_menu(self):
        if self.menuPanel.isVisible():
            self.animation = QPropertyAnimation(self.menuPanel, b"geometry")
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(0, 0, 120, self.parent.height()))
            self.animation.setEndValue(QRect(-120, 0, 120, self.parent.height()))
            self.animation.finished.connect(self.menuPanel.hide)
            self.animation.start()
        else:
            self.menuPanel.setGeometry(-120, 0, 120, self.parent.height())
            self.menuPanel.show()
            self.menuPanel.raise_()
            self.animation = QPropertyAnimation(self.menuPanel, b"geometry")
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(-120, 0, 120, self.parent.height()))
            self.animation.setEndValue(QRect(0, 0, 120, self.parent.height()))
            self.animation.start()
            self.load_songs()

    def load_songs(self):
        for btn in self.songButtons:
            btn.deleteLater()
        self.songButtons.clear()

        music_dir = "resourses/Music"
        supported_formats = ('.mp3', '.wav', '.ogg')

        try:
            songs = [f for f in os.listdir(music_dir) if f.endswith(supported_formats)]
        except FileNotFoundError:
            songs = []

        for name in songs:
            display_name = os.path.splitext(name)[0]
            button = QtWidgets.QPushButton(display_name)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4b2e6f;
                    color: white;
                    border-radius: 6px;
                    font-size: 12px;
                }
            """)
            button.clicked.connect(lambda _, n=name: self.play_song(n))
            self.songContainer.addWidget(button)
            self.songButtons.append(button)

    def play_song(self, song_name):
        music_path = os.path.join("resourses/Music", song_name)
        if os.path.exists(music_path):
            url = QUrl.fromLocalFile(os.path.abspath(music_path))
            self.parent.player.setMedia(QMediaContent(url))
            self.parent.player.play()
            self.parent.songTitle.setText(os.path.splitext(song_name)[0])
            self.parent.pauseButton.setIcon(QIcon("resourses/Images/Icons/pause_button_icon.png"))
            self.parent.timer.start()

            cover_path = next(
                (c for c in self.parent.covers if os.path.basename(c).startswith(os.path.splitext(song_name)[0])),
                "resourses/Images/Covers/ztrack.png"
            )
            pixmap = QPixmap(cover_path).scaled(
                self.parent.albumCover.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.parent.albumCover.setPixmap(pixmap)

            try:
                index = self.parent.tracks.index(music_path)
                self.parent.background_manager.apply_background(self.parent, index)
            except ValueError:
                print(f"Track not found in list: {music_path}")