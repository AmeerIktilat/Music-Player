import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap


from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from track_manager import TrackManager
from playlist_manager import PlaylistManager
from background_manager import BackgroundManager
from menu_panel import MenuPanel

class MusicPlayerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("resourses/MusicPlayerWindow.ui", self)
        self.setWindowTitle("Music Player")
        self.setWindowIcon(QIcon("resourses/Images/Icons/Music-Player-Icon2.jpeg"))


        self.player = QMediaPlayer()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_progress)

        self.track_manager = TrackManager(self.player)
        self.playlist_manager = PlaylistManager()
        self.background_manager = BackgroundManager()
        self.menu_panel = MenuPanel(self, self.playlist_manager, self.track_manager)

        # 🎨 Background frame (must be created before load_track)
        self.backgroundFrame = QtWidgets.QFrame(self)
        self.backgroundFrame.setObjectName("backgroundFrame")
        self.backgroundFrame.setGeometry(0, 0, self.width(), self.height())
        self.backgroundFrame.lower()  # Push behind all other widgets

        self.tracks = [
            os.path.join("resourses/Music", f)
            for f in os.listdir("resourses/Music")
            if f.lower().endswith(".mp3")

        ]

        self.covers = [
            os.path.join("resourses/Images/Covers", f)
            for f in os.listdir("resourses/Images/Covers")
            if f.lower().endswith(".jpg") or f.lower().endswith(".png") or f.lower().endswith(".jpeg") or f.lower().endswith(".webp")
        ]
        self.track_manager.set_tracks(self.tracks)
        self.load_track(0)

        self.menuButton.clicked.connect(self.menu_panel.toggle_menu)
        self.pauseButton.clicked.connect(self.toggle_pause)
        self.nextButton.clicked.connect(self.skip_next)
        self.prevButton.clicked.connect(self.skip_previous)
        self.progressBar.sliderMoved.connect(self.seek_position)


        self.nextButton.setIcon(QIcon("resourses/Images/Icons/next_button_icon.png"))
        self.nextButton.setIconSize(QSize(40, 40))
        self.nextButton.setText("")

        self.prevButton.setIcon(QIcon("resourses/Images/Icons/back_button_icon.png"))
        self.prevButton.setIconSize(QSize(40, 40))
        self.prevButton.setText("")

        self.timeStart.setText("0:00")
        self.timeEnd.setText("0:00")
        self.pauseButton.setIcon(QIcon("resourses/Images/Icons/pause_button_icon.png"))
        self.pauseButton.setIconSize(QSize(40, 40))
        self.pauseButton.setText("")
        self.setObjectName("musicPlayerWindow")

    def resizeEvent(self, event):
        self.backgroundFrame.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def load_track(self, index):
        if 0 <= index < len(self.tracks):
            track_path = self.tracks[index]
            track_name = os.path.basename(track_path).replace(".mp3", "")
            display_name = track_name.replace("_", " ").title()

            # 🎧 Load and play the track
            url = QUrl.fromLocalFile(os.path.abspath(track_path))
            self.player.setMedia(QMediaContent(url))
            self.player.play()
            self.pauseButton.setIcon(QIcon("resourses/Images/Icons/pause_button_icon.png"))
            self.timer.start()

            # 🏷️ Update song title
            self.songTitle.setText(display_name)

            # 🌄 Update background
            self.background_manager.apply_background(self, index)

            if index >= len(self.covers):
                pixmap = QPixmap("resourses/Images/Covers/ztrack.png")
            else:
                pixmap = QPixmap(self.covers[index])


            pixmap = pixmap.scaled(self.albumCover.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.imageLabel = QLabel(self)
            self.imageLabel.setPixmap(pixmap)
            self.imageLabel.setGeometry(100, 50, 200, 200)

    def toggle_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.pauseButton.setIcon(QIcon("resourses/Images/Icons/play_button_icon.png"))
        else:
            self.player.play()
            self.pauseButton.setIcon(QIcon("resourses/Images/Icons/pause_button_icon.png"))

    def skip_next(self):
        index = self.track_manager.next_track()
        self.load_track(index)

    def skip_previous(self):
        index = self.track_manager.previous_track()
        self.load_track(index)

    def seek_position(self, position):
        duration = self.player.duration()
        if duration > 0:
            self.player.setPosition(int((position / 100) * duration))

    def update_progress(self):
        duration = self.player.duration()
        position = self.player.position()
        if duration > 0:
            self.progressBar.setValue(int((position / duration) * 100))
            self.timeStart.setText(self.format_time(position))
            self.timeEnd.setText(self.format_time(duration))

    @staticmethod
    def format_time(ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02}"