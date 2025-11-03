import tkinter as tk
from tkinter import font


def popup_next_round_banner() -> None:
    """Display a banner prompting to go back for another round."""
    root = tk.Tk()
    root.title("Next Round")
    root.configure(bg="#FFFFFF")
    root.attributes("-fullscreen", True)
    root.resizable(False, False)
    title_font = font.Font(family="Helvetica", size=22, weight="bold")
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    container = tk.Frame(root, bg="#FFFFFF")
    container.pack(expand=True)

    tk.Label(
        container,
        text="Please go back to the game\nfor another round",
        font=title_font,
        fg="#000000",
        bg="#FFFFFF",
        justify="center",
    ).pack(pady=(70, 40))

    tk.Button(
        container,
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
