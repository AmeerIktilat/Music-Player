from PyQt5 import QtWidgets
import os
from PyQt5.QtCore import QPropertyAnimation, QRect

class MenuPanel:
    def __init__(self, parent, playlist_manager, track_manager):
        self.parent = parent
        self.playlist_manager = playlist_manager
        self.track_manager = track_manager

        self.menuPanel = QtWidgets.QFrame(parent)
        self.menuPanel.setGeometry(0, 0, 120, parent.height())
        self.menuPanel.setStyleSheet("background-color: #3c2c5e;")
        self.menuPanel.hide()

        self.menuLayout = QtWidgets.QVBoxLayout(self.menuPanel)
        self.menuLayout.setContentsMargins(10, 10, 10, 10)
        self.menuLayout.setSpacing(10)

        self.favoriteLabel = QtWidgets.QLabel("★ Playlist's ")
        self.favoriteLabel.setStyleSheet("color: gold; font-size: 14px; font-weight: bold;")
        self.menuLayout.addWidget(self.favoriteLabel)

        self.createPlaylistButton = QtWidgets.QPushButton("Create Playlist")
        self.createPlaylistButton.setStyleSheet("""
            QPushButton {
                background-color: #a86cc1;
                color: white;
                border-radius: 8px;
                font-size: 12px;
            }
        """)
        self.createPlaylistButton.clicked.connect(self.create_playlist)
        self.menuLayout.addWidget(self.createPlaylistButton)

        self.playlistContainer = QtWidgets.QVBoxLayout()
        self.menuLayout.addLayout(self.playlistContainer)

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


        self.playlistButtons = []

    def toggle_menu(self):
        if self.menuPanel.isVisible():
            # Slide out to the left
            self.animation = QPropertyAnimation(self.menuPanel, b"geometry")
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(0, 0, 120, self.parent.height()))
            self.animation.setEndValue(QRect(-120, 0, 120, self.parent.height()))
            self.animation.finished.connect(self.menuPanel.hide)
            self.animation.start()
        else:
            # Show and slide in from the left
            self.menuPanel.setGeometry(-120, 0, 120, self.parent.height())
            self.menuPanel.show()
            self.menuPanel.raise_()
            self.animation = QPropertyAnimation(self.menuPanel, b"geometry")
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(-120, 0, 120, self.parent.height()))
            self.animation.setEndValue(QRect(0, 0, 120, self.parent.height()))
            self.animation.start()

        self.close_playlist()

    def create_playlist(self):
        name, ok = QtWidgets.QInputDialog.getText(self.parent, "New Playlist", "Enter playlist name:")
        if ok and name:
            self.playlist_manager.create_playlist(name)
            self.add_playlist_to_menu(name)

    def add_playlist_to_menu(self, name):
        button = QtWidgets.QPushButton(name)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4b2e6f;
                color: white;
                border-radius: 6px;
                font-size: 12px;
            }
        """)
        button.clicked.connect(lambda _, n=name: self.open_playlist(n))
        self.playlistContainer.addWidget(button)
        self.playlistButtons.append(button)

    def close_playlist(self):
        if hasattr(self, "playlistPanel"):
            self.animation = QPropertyAnimation(self.playlistPanel, b"geometry")
            self.animation.setDuration(300)
            self.animation.setStartValue(QRect(120, 0, 280, self.parent.height()))
            self.animation.setEndValue(QRect(-280, 0, 280, self.parent.height()))
            self.animation.finished.connect(self.playlistPanel.hide)
            self.animation.start()

    from PyQt5 import QtWidgets
    from PyQt5.QtCore import QPropertyAnimation, QRect

    def open_playlist(self, name):
        self.close_playlist()
        # Remove previous panel if it exists
        if hasattr(self, "playlistPanel"):
            self.playlistPanel.deleteLater()

        # Create the playlist panel off-screen
        self.playlistPanel = QtWidgets.QFrame(self.parent)
        self.playlistPanel.setGeometry(-280, 0, 280, self.parent.height())#---------
        self.playlistPanel.setStyleSheet("background-color: #2e1f4b;")
        self.playlistPanel.show()

        # Animate sliding in from the left
        self.animation = QPropertyAnimation(self.playlistPanel, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(-280, 0, 280, self.parent.height()))
        self.animation.setEndValue(QRect(120, 0, 280, self.parent.height()))
        self.animation.start()

        # Add playlist title
        title = QtWidgets.QLabel(f"{name} Songs", self.playlistPanel)
        title.setGeometry(10, 10, 260, 30)
        title.setStyleSheet("color: white; font-size: 14px;")

        # Add song buttons
        songs = self.playlist_manager.get_tracks(name)
        self.playlistSongButtons = []
        for i, song in enumerate(songs):
            btn = QtWidgets.QPushButton(os.path.basename(song), self.playlistPanel)
            btn.setGeometry(10, 50 + i * 35, 260, 30)
            btn.setStyleSheet("background-color: #a86cc1; color: white; border-radius: 6px;")
            btn.clicked.connect(lambda _, s=song: self.play_song_from_playlist(s))
            btn.show()
            self.playlistSongButtons.append(btn)