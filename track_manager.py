import os
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl

class TrackManager:
    def __init__(self, player):
        self.player = player
        self.tracks = []
        self.current_index = 0

    def set_tracks(self, tracks):
        self.tracks = tracks

    def load_track(self, index):
        if 0 <= index < len(self.tracks):
            path = self.tracks[index]
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath(path))))
            self.player.play()
            self.current_index = index
            return path

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.tracks)
        return self.current_index

    def previous_track(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        return self.current_index

    def get_track_name(self, path):
        return os.path.basename(path).replace(".mp3", "").replace("_", " ").title()