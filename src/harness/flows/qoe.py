import pathlib
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import font

from PIL import Image, ImageTk

from harness import constants


def popup_qoe_questionnaire(answer_path: str | pathlib.Path) -> None:  # noqa: C901, PLR0915
    def disable_event() -> None:
        pass

    def store_ans() -> None:
        with pathlib.Path(answer_path).open(mode="a") as log:
            log.write(f"QoE: {entry1.get()} : {btn1.get()},\n")

    def force_answer1() -> None:
        mb.showinfo("Reminder", "Please answer Q1 with a number between 1.0 and 5.0")

    def force_answer2() -> None:
        mb.showinfo("Reminder", "Please answer Q2")

    def check_ans1() -> bool:
        num = entry1.get().strip()
        try:
            val = float(num)
        except ValueError:
            return False
        return 1.0 <= val <= 5.0  # noqa: PLR2004

    def check_ans2() -> bool:
        val = btn1.get()
        return val in (1, 2)

    def check_both() -> None:
        if not check_ans1():
            force_answer1()
            return
        if not check_ans2():
            force_answer2()
            return
        store_ans()
        master.destroy()

    # --- Window setup ---
    master = tk.Tk()
    master.title("In-game Survey")
    master.configure(bg="#FFFFFF")
    master.attributes("-fullscreen", True)
    master.resizable(False, False)
    master.attributes("-topmost", True)
    master.protocol("WM_DELETE_WINDOW", disable_event)

    # --- Fonts ---
    title_font = font.Font(family="Helvetica", size=22, weight="bold")
    question_font = font.Font(family="Helvetica", size=14)
    button_font = font.Font(family="Helvetica", size=16, weight="bold")

    # --- Layout ---
    tk.Label(
        master,
        text="In-game Survey",
        font=title_font,
        fg="#000000",
        bg="#FFFFFF",
        justify="center",
    ).pack(pady=(30, 10))

    # Q1
    tk.Label(
        master,
        text="Q1: Rate the quality of the previous round (1.0 - 5.0)",
        font=question_font,
        fg="#000000",
        bg="#FFFFFF",
        wraplength=700,
        justify="left",
    ).pack(pady=(20, 5))

    entry_frame = tk.Frame(master, bg="#FFFFFF")
    entry_frame.pack(pady=(0, 15))
    tk.Label(
        entry_frame,
        text="Enter here:",
        font=("Helvetica", 12),
        bg="#FFFFFF",
    ).pack(side="left", padx=(0, 10))
    entry1 = tk.Entry(entry_frame, width=10, font=("Helvetica", 12))
    entry1.pack(side="left")

    img = Image.open(constants.QOE_CHART)
    img = img.resize((300, 200))
    img_tk = ImageTk.PhotoImage(img)
    tk.Label(master, image=img_tk, bg="#FFFFFF").pack(pady=(10, 10))

    # Q2
    tk.Label(
        master,
        text="Q2: Is the experience acceptable?",
        font=question_font,
        fg="#000000",
        bg="#FFFFFF",
    ).pack(pady=(20, 10))

    btn1 = tk.IntVar(value=0)
    radio_frame = tk.Frame(master, bg="#FFFFFF")
    radio_frame.pack(pady=(0, 20))

    tk.Radiobutton(
        radio_frame,
        text="Yes",
        variable=btn1,
        value=1,
        font=question_font,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
    ).pack(side="left", padx=20)

    tk.Radiobutton(
        radio_frame,
        text="No",
        variable=btn1,
        value=2,
        font=question_font,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
    ).pack(side="left", padx=20)

    # Done Button
    tk.Button(
        master,
        text="Submit",
        font=button_font,
        bg="#0078D7",
        fg="#FFFFFF",
        activebackground="#005A9E",
        activeforeground="#FFFFFF",
        width=16,
        height=2,
        relief="flat",
        borderwidth=0,
        command=check_both,
    ).pack(pady=(20, 40))

    master.mainloop()
