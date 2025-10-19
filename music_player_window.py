import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from track_manager import TrackManager
from playlist_manager import PlaylistManager
from background_manager import BackgroundManager
from menu_panel import MenuPanel

class MusicPlayerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("resourses/MusicPlayerWindow.ui", self)

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
            "resourses/Music/track1.mp3",
            "resourses/Music/track2.mp3",
            "resourses/Music/track3.mp3"
        ]
        self.track_manager.set_tracks(self.tracks)
        self.load_track(0)

        self.menuButton.clicked.connect(self.menu_panel.toggle_menu)
        self.pauseButton.clicked.connect(self.toggle_pause)
        self.nextButton.clicked.connect(self.skip_next)
        self.prevButton.clicked.connect(self.skip_previous)
        self.progressBar.sliderMoved.connect(self.seek_position)

        self.timeStart.setText("0:00")
        self.timeEnd.setText("0:00")
        self.pauseButton.setText("⏸")
        self.setObjectName("musicPlayerWindow")

    def resizeEvent(self, event):
        self.backgroundFrame.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    from PyQt5 import QtGui
    import os
    def load_track(self, index):
        if 0 <= index < len(self.tracks):
            track_path = self.tracks[index]
            track_name = os.path.basename(track_path).replace(".mp3", "")
            display_name = track_name.replace("_", " ").title()

            # 🎧 Load and play the track
            url = QUrl.fromLocalFile(os.path.abspath(track_path))
            self.player.setMedia(QMediaContent(url))
            self.player.play()
            self.pauseButton.setText("⏸")
            self.timer.start()

            # 🏷️ Update song title
            self.songTitle.setText(display_name)

            # 🌄 Update background
            self.background_manager.apply_background(self, index)

            # 🖼️ Load album cover into QLabel named 'albumCover'
            cover_path = f"resources/Images/Covers/{track_name}.jpeg"
            if os.path.exists(cover_path):
                pixmap = QtGui.QPixmap(cover_path)
                self.albumCover.setPixmap(pixmap)
            else:
                self.albumCover.clear()

    def toggle_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.pauseButton.setText("▶")
        else:
            self.player.play()
            self.pauseButton.setText("⏸")

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

    def format_time(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02}"