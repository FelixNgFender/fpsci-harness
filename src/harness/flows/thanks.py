import tkinter as tk
from tkinter import font


def popup_thank_you_banner() -> None:
    """Display a clean thank-you banner after completing all rounds."""
    root = tk.Tk()
    root.title("Thank You")
    root.configure(bg="#FFFFFF")
    root.attributes("-fullscreen", True)
    root.resizable(False, False)

    # Fonts
    title_font = font.Font(family="Helvetica", size=22, weight="bold")
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    # Main message
    container = tk.Frame(root, bg="#FFFFFF")
    container.pack(expand=True)

    tk.Label(
        container,
        text="You’ve completed all rounds!\n\nThank you for participating!",
        font=title_font,
        fg="#000000",
        bg="#FFFFFF",
        justify="center",
    ).pack(pady=(70, 40))

    # Close button
    tk.Button(
        container,
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
        command=root.destroy,
    ).pack()

    # Prevent accidental close
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()
