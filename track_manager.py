class TrackManager:
    def __init__(self, player):
        self.player = player
        self.tracks = []
        self.current_index = 0

    def set_tracks(self, tracks):
        self.tracks = tracks

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.tracks)
        return self.current_index

    def previous_track(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        return self.current_index