import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize, Qt, QTimer, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QLabel, QListWidget, QPushButton

from track_manager import TrackManager
from background_manager import BackgroundManager
from menu_panel import MenuPanel
from add_song_dialog import AddSongDialog


class MusicPlayerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("resourses/MusicPlayerWindow.ui", self)
        self.setWindowTitle("Music Player")
        self.setWindowIcon(QIcon("resourses/Images/Icons/Music-Player-Icon2.jpeg"))

        self.songTitle.setStyleSheet("""
            QLabel {
                background-color: #4b2e6f;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
            }
        """)



        self.player = QMediaPlayer()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_progress)

        self.track_manager = TrackManager(self.player)
        self.background_manager = BackgroundManager()

        self.backgroundFrame = QtWidgets.QFrame(self)
        self.backgroundFrame.setObjectName("backgroundFrame")
        self.backgroundFrame.setGeometry(0, 0, self.width(), self.height())
        self.backgroundFrame.lower()

        self.song_list_widget = QListWidget(self)
        self.song_list_widget.setGeometry(20, 100, 200, 400)
        self.song_list_widget.itemClicked.connect(self.play_selected_song)
        self.song_list_widget.setVisible(False)#debugging----------------------

        self.refresh_tracks_and_covers()
        self.track_manager.set_tracks(self.tracks)
        self.menu_panel = MenuPanel(self)
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

        self.pauseButton.setIcon(QIcon("resourses/Images/Icons/pause_button_icon.png"))
        self.pauseButton.setIconSize(QSize(40, 40))
        self.pauseButton.setText("")

        self.timeStart.setText("0:00")
        self.timeEnd.setText("0:00")

        self.add_button = QPushButton("+", self)
        self.add_button.setFixedSize(40, 40)
        self.add_button.move(self.width() - 60, self.height() - 60)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #a86cc1;
                color: white;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c58ee0;
            }
        """)
        self.add_button.clicked.connect(self.open_add_song_dialog)

    def refresh_tracks_and_covers(self):
        self.tracks = [
            os.path.join("resourses/Music", f)
            for f in os.listdir("resourses/Music")
            if f.lower().endswith(".mp3")
        ]
        self.covers = [
            os.path.join("resourses/Images/Covers", f)
            for f in os.listdir("resourses/Images/Covers")
            if f.lower().endswith((".jpg", ".png", ".jpeg", ".webp"))
        ]
        self.load_songs()

    def load_songs(self):
        self.song_list_widget.clear()
        for track_path in self.tracks:
            song_name = os.path.splitext(os.path.basename(track_path))[0]
            self.song_list_widget.addItem(song_name)

    def play_selected_song(self, item):
        song_name = item.text()
        music_path = os.path.join("resourses/Music", f"{song_name}.mp3")
        if os.path.exists(music_path):
            url = QUrl.fromLocalFile(os.path.abspath(music_path))
            self.player.setMedia(QMediaContent(url))
            self.player.play()
            self.songTitle.setText(song_name)
            self.pauseButton.setIcon(QIcon("resourses/Images/Icons/pause_button_icon.png"))
            self.timer.start()

            cover_path = next((c for c in self.covers if os.path.basename(c).startswith(song_name)), "resourses/Images/Covers/ztrack.png")
            pixmap = QPixmap(cover_path).scaled(self.albumCover.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.albumCover.setPixmap(pixmap)

    def open_add_song_dialog(self):
        dialog = AddSongDialog(self)
        if dialog.exec_():
            self.refresh_tracks_and_covers()
            self.track_manager.set_tracks(self.tracks)

    def resizeEvent(self, event):
        self.backgroundFrame.setGeometry(0, 0, self.width(), self.height())
        self.add_button.move(self.width() - 60, self.height() - 60)
        super().resizeEvent(event)

    def load_track(self, index):
        if 0 <= index < len(self.tracks):
            track_path = self.tracks[index]
            track_name = os.path.basename(track_path).replace(".mp3", "")
            display_name = track_name.replace("_", " ").title()

            url = QUrl.fromLocalFile(os.path.abspath(track_path))
            self.player.setMedia(QMediaContent(url))
            self.player.play()
            self.pauseButton.setIcon(QIcon("resourses/Images/Icons/pause_button_icon.png"))
            self.timer.start()

            self.songTitle.setText(display_name)
            self.background_manager.apply_background(self, index)

            cover_path = self.covers[index] if index < len(self.covers) else "resourses/Images/Covers/ztrack.png"
            pixmap = QPixmap(cover_path).scaled(self.albumCover.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.albumCover.setPixmap(pixmap)

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