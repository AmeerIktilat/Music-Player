import os
import shutil
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QMessageBox
)

class AddSongDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Song")
        self.setFixedSize(400, 300)

        self.song_name_input = QLineEdit(self)
        self.song_name_input.setPlaceholderText("Enter song name")

        self.mp3_path = ""
        self.cover_path = ""

        self.mp3_button = QPushButton("Choose MP3 File", self)
        self.mp3_button.clicked.connect(self.select_mp3)

        self.cover_button = QPushButton("Choose Cover Image (optional)", self)
        self.cover_button.clicked.connect(self.select_cover)

        self.submit_button = QPushButton("Add Song", self)
        self.submit_button.clicked.connect(self.add_song)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Song Name:"))
        layout.addWidget(self.song_name_input)
        layout.addWidget(self.mp3_button)
        layout.addWidget(self.cover_button)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        self.parent_window = parent  # Save reference to main window

    def select_mp3(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select MP3", "", "MP3 Files (*.mp3)")
        if file:
            self.mp3_path = file

    def select_cover(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Cover", "", "Images (*.png *.jpg *.jpeg)")
        if file:
            self.cover_path = file

    def add_song(self):
        song_name = self.song_name_input.text().strip()
        if not song_name or not self.mp3_path:
            QMessageBox.warning(self, "Missing Info", "Please enter a song name and select an MP3 file.")
            return

        music_dir = "resourses/Music"
        cover_dir = "resourses/Images/Covers"
        mp3_target = os.path.join(music_dir, f"{song_name}.mp3")

        # Check for duplicates
        if os.path.exists(mp3_target):
            QMessageBox.warning(self, "Duplicate", "A song with this name already exists.")
            return

        try:
            shutil.copy(self.mp3_path, mp3_target)
            if self.cover_path:
                ext = os.path.splitext(self.cover_path)[1]
                cover_target = os.path.join(cover_dir, f"{song_name}{ext}")
                shutil.copy(self.cover_path, cover_target)
            QMessageBox.information(self, "Success", f"Song '{song_name}' added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add song: {e}")

        try:
            shutil.copy(self.mp3_path, mp3_target)
            if self.cover_path:
                ext = os.path.splitext(self.cover_path)[1]
                shutil.copy(self.cover_path, os.path.join(cover_dir, f"{song_name}{ext}"))

            QMessageBox.information(self, "Success", f"Song '{song_name}' added successfully!")
            self.parent_window.load_songs()  # Refresh playlist
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add song: {e}")
