import tkinter as tk
from tkinter import font

from harness import video


def popup_start_banner(
    window_title: str,
    title: str,
    description: str,
    tutorial_path: str | None = None,
) -> None:
    """Display a banner announcing the start of the Fitts' Law game."""
    master = tk.Tk()
    master.title(window_title)
    master.configure(bg="#FFFFFF")
    master.attributes("-fullscreen", True)
    master.attributes("-topmost", True)
    master.resizable(False, False)

    # Custom fonts
    title_font = font.Font(family="Helvetica", size=22, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=12)

    # Title label
    tk.Label(
        master,
        text=title,
        font=title_font,
        bg="#FFFFFF",
        fg="#003366",
    ).pack(pady=(50, 10))

    # Subtitle text
    tk.Label(
        master,
        text=description,
        font=subtitle_font,
        bg="#FFFFFF",
        fg="#333333",
        justify="center",
    ).pack(pady=(0, 40))

    if tutorial_path is not None:
        video_frame = tk.LabelFrame(master, bg="black", width=1280, height=720)
        video_frame.pack(pady=(10, 20))
        video_frame.pack_propagate(False)  # keep fixed size

        player = video.Player(video_frame)
        player.open_file(tutorial_path)

        def on_quit() -> None:
            master.destroy()
            player.mediaplayer.stop()
    else:

        def on_quit() -> None:
            master.destroy()

    # Start button
    start_button = tk.Button(
        master,
        text="Start",
        font=("Helvetica", 14, "bold"),
        bg="#0078D7",
        fg="#FFFFFF",
        activebackground="#005A9E",
        activeforeground="#FFFFFF",
        relief="raised",
        width=12,
        height=2,
        command=on_quit,
        borderwidth=0,
    )
    start_button.pack()

    # Disable closing via the X button
    master.protocol("WM_DELETE_WINDOW", lambda: None)
    master.mainloop()
