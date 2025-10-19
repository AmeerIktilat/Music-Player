class BackgroundManager:
    def apply_background(self, widget, index):
        bg_index = (index % 17) + 1
        bg_path = f"resourses/Images/Backgrounds/{bg_index}.jpeg"
        widget.backgroundFrame.setStyleSheet(f"""
            QFrame#backgroundFrame {{
                background-image: url("{bg_path}");
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
            }}
        """)