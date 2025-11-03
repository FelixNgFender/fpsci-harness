import platform
import vlc
import tkinter as tk


class Player(tk.Label):
    def __init__(self, frame: tk.LabelFrame):
        super().__init__()
        self.master = frame
        # Create a basic vlc instance
        self.instance = vlc.Instance()
        self.media = None
        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

    def open_file(self, file_name: str):
        """Open a media file in a MediaPlayer"""
        self.media = self.instance.media_new(file_name)
        self.mediaplayer.set_media(self.media)

        # The media player has to be 'connected' to the Frame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the Frame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux":  # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.master.winfo_id()))
        elif platform.system() == "Windows":  # for Windows
            self.mediaplayer.set_hwnd(int(self.master.winfo_id()))
        elif platform.system() == "Darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.master.winfo_id()))

        self.media.parse()
        self.mediaplayer.play()
