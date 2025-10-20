import os
import random




class BackgroundManager:
    @staticmethod
    def find_cover_image(track_name):
        base_path = "resourses/Images/Backgrounds/"
        for ext in [".jpeg", ".jpg"]:
            path = os.path.join(base_path, str(track_name) + ext)
            if os.path.exists(path):
                return path
        return None


    def apply_background(self, widget, index):
        item_count = len(os.listdir("resourses/Images/Backgrounds"))
        bg_path = self.find_cover_image(random.randint(1, item_count))
        widget.backgroundFrame.setStyleSheet(f"""
            QFrame#backgroundFrame {{
                background-image: url("{bg_path}");
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
            }}
        """)

