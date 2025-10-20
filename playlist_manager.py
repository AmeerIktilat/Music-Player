class PlaylistManager:
    def __init__(self):
        self.playlists = {}

    def create_playlist(self, name):
        if name not in self.playlists:
            self.playlists[name] = []

    def add_track(self, playlist_name, track_path):
        if playlist_name in self.playlists and track_path not in self.playlists[playlist_name]:
            self.playlists[playlist_name].append(track_path)

    def get_tracks(self, playlist_name):
        return self.playlists.get(playlist_name, [])

    def rename_playlist(self, old_name, new_name):
        if old_name in self.playlists and new_name not in self.playlists:
            self.playlists[new_name] = self.playlists.pop(old_name)

    def delete_playlist(self, name):
        if name in self.playlists:
            del self.playlists[name]