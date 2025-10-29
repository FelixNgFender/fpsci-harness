import os
import tkinter as tk
import tkinter.font as font
import harness.constants as constants


def popup_test_round_start_banner() -> None:
    """Display a banner announcing the start of the test round."""
    root = tk.Tk()
    root.title("Test Round")
    root.configure(bg="#FFFFFF")
    root.geometry("550x320")
    root.resizable(False, False)

    # Fonts
    title_font = font.Font(family="Helvetica", size=24, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=14)
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    # Title
    tk.Label(
        root,
        text="This is a test round",
        font=title_font,
        fg="#0071C5",
        bg="#FFFFFF",
    ).pack(pady=(60, 10))

    # Subtitle
    tk.Label(
        root,
        text="Feel free to try 😊",
        font=subtitle_font,
        fg="#333333",
        bg="#FFFFFF",
    ).pack(pady=(0, 20))

    # Instruction
    tk.Label(
        root,
        text="Press the button below to start",
        font=("Helvetica", 11, "italic"),
        fg="#E65100",
        bg="#FFFFFF",
    ).pack(pady=(0, 30))

    # Button
    tk.Button(
        root,
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
        command=root.destroy,
    ).pack()

    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()


def popup_test_round_end_banner() -> None:
    """Display a banner announcing the end of the test round."""
    root = tk.Tk()
    root.title("Test Round Ended")
    root.configure(bg="#FFFFFF")
    root.geometry("550x320")
    root.resizable(False, False)

    title_font = font.Font(family="Helvetica", size=24, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=14)
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    tk.Label(
        root,
        text="Test round ended!",
        font=title_font,
        fg="#0071C5",
        bg="#FFFFFF",
    ).pack(pady=(60, 10))

    tk.Label(
        root,
        text="Let's play more 😊  Take a break if you need",
        font=subtitle_font,
        fg="#333333",
        bg="#FFFFFF",
    ).pack(pady=(0, 20))

    tk.Label(
        root,
        text="Press the button below to continue",
        font=("Helvetica", 11, "italic"),
        fg="#E65100",
        bg="#FFFFFF",
    ).pack(pady=(0, 30))

    tk.Button(
        root,
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
        command=root.destroy,
    ).pack()

    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()


def popup_next_round_banner() -> None:
    """Display a banner prompting to go back for another round."""
    root = tk.Tk()
    root.title("Next Round")
    root.configure(bg="#FFFFFF")
    root.geometry("550x300")
    root.resizable(False, False)

    title_font = font.Font(family="Helvetica", size=22, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=14)
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    tk.Label(
        root,
        text="Please go back to the game\nfor another round",
        font=title_font,
        fg="#000000",
        bg="#FFFFFF",
        justify="center",
    ).pack(pady=(70, 40))

    tk.Button(
        root,
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
        command=root.destroy,
    ).pack()

    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()
