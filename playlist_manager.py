class PlaylistManager:
    def __init__(self):
        self.playlists = {}

    def create_playlist(self, name):
        if name not in self.playlists:
            self.playlists[name] = []

    def add_track(self, playlist_name, track_path):
        if playlist_name in self.playlists:
            self.playlists[playlist_name].append(track_path)

    def get_tracks(self, playlist_name):
        return self.playlists.get(playlist_name, [])