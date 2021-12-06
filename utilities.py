import random

from tkinter import *


def generate_quiz_options(
    parent, question_type, choices, command=None, disabled=False, answers=None
):
    choice_group = Frame(master=parent, pady=20, padx=10, bg="#FAFAFA")
    random.shuffle(choices)
    index = 0
    for choice in choices:
        chkValue = BooleanVar()
        chkValue.set(False)
        if question_type == "MCQ":
            if not disabled:
                Checkbutton(
                    choice_group,
                    text=choice,
                    var=chkValue,
                    bg="#FAFAFA",
                    highlightthickness=0,
                    command=lambda choice=choice: command(choice, True),
                ).grid(row=index, column=0, sticky="w")
            else:
                checkbutton = Checkbutton(
                    choice_group,
                    text=choice,
                    var=chkValue,
                    bg="#FAFAFA",
                    highlightthickness=0,
                )

                if choice in answers:
                    print("yes checky")
                    checkbutton.select()

                checkbutton.configure(state=DISABLED)
                checkbutton.grid(row=index, column=0, sticky="w")
        else:
            v = StringVar()
            if not disabled:
                Radiobutton(
                    choice_group,
                    text=choice,
                    value=choice,
                    variable=v,
                    bg="#FAFAFA",
                    highlightthickness=0,
                    command=lambda choice=choice: command(choice),
                ).grid(row=index, column=0, sticky="w")
            else:
                if choice in answers:
                    print("yes radio")
                    # radiobutton.select()
                    v.set(choice)

                radiobutton = Radiobutton(
                    choice_group,
                    text=choice,
                    value=choice,
                    variable=v,
                    bg="#FAFAFA",
                    highlightthickness=0,
                    state=DISABLED,
                ).grid(row=index, column=0, sticky="w")

        index += 1
    choice_group.pack(fill=X)
