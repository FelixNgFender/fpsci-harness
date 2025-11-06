import tkinter as tk
from tkinter import font


def popup_thank_you_banner() -> None:
    """Display a clean thank-you banner after completing all rounds."""
    master = tk.Tk()
    master.title("Thank You")
    master.configure(bg="#FFFFFF")
    master.attributes("-fullscreen", True)
    master.resizable(False, False)

    # Fonts
    title_font = font.Font(family="Helvetica", size=22, weight="bold")
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    # Main message
    tk.Label(
        master,
        text="You've completed all rounds!\n\nThank you for participating!",
        font=title_font,
        fg="#000000",
        bg="#FFFFFF",
        justify="center",
    ).pack(pady=(70, 40))

    # Close button
    tk.Button(
        master,
        text="Finish",
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

    # Prevent accidental close
    master.protocol("WM_DELETE_WINDOW", lambda: None)
    master.mainloop()
