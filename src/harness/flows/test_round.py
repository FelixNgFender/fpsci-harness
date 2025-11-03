import tkinter as tk
from tkinter import font


def popup_test_round_start_banner() -> None:
    """Display a banner announcing the start of the test round."""
    master = tk.Tk()
    master.title("Test Round")
    master.configure(bg="#FFFFFF")
    master.attributes("-fullscreen", True)
    master.resizable(False, False)

    # Fonts
    title_font = font.Font(family="Helvetica", size=24, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=14)
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    # Title
    tk.Label(
        master,
        text="This is a test round",
        font=title_font,
        fg="#0071C5",
        bg="#FFFFFF",
    ).pack(pady=(60, 10))

    # Subtitle
    tk.Label(
        master,
        text="Feel free to try 😊",
        font=subtitle_font,
        fg="#333333",
        bg="#FFFFFF",
    ).pack(pady=(0, 20))

    # Instruction
    tk.Label(
        master,
        text="Press the button below to start",
        font=("Helvetica", 11, "italic"),
        fg="#E65100",
        bg="#FFFFFF",
    ).pack(pady=(0, 30))

    # Button
    tk.Button(
        master,
        text="Start",
        font=button_font,
        bg="#0078D7",
        fg="#FFFFFF",
        activebackground="#005A9E",
        activeforeground="#FFFFFF",
        width=14,
        height=2,
        relief="flat",
        borderwidth=0,
        command=master.destroy,
    ).pack()

    master.protocol("WM_DELETE_WINDOW", lambda: None)
    master.mainloop()


def popup_test_round_end_banner() -> None:
    """Display a banner announcing the end of the test round."""
    master = tk.Tk()
    master.title("Test Round Ended")
    master.configure(bg="#FFFFFF")
    master.attributes("-fullscreen", True)
    master.resizable(False, False)

    title_font = font.Font(family="Helvetica", size=24, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=14)
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    tk.Label(
        master,
        text="Test round ended!",
        font=title_font,
        fg="#0071C5",
        bg="#FFFFFF",
    ).pack(pady=(60, 10))

    tk.Label(
        master,
        text="Let's play more 😊  Take a break if you need",
        font=subtitle_font,
        fg="#333333",
        bg="#FFFFFF",
    ).pack(pady=(0, 20))

    tk.Label(
        master,
        text="Press the button below to continue",
        font=("Helvetica", 11, "italic"),
        fg="#E65100",
        bg="#FFFFFF",
    ).pack(pady=(0, 30))

    tk.Button(
        master,
        text="Continue",
        font=button_font,
        bg="#0078D7",
        fg="#FFFFFF",
        activebackground="#005A9E",
        activeforeground="#FFFFFF",
        width=14,
        height=2,
        relief="flat",
        borderwidth=0,
        command=master.destroy,
    ).pack()

    master.protocol("WM_DELETE_WINDOW", lambda: None)
    master.mainloop()
