import random

from tkinter import *

def generate_quiz_options(window, question_type, choices, command):
    choice_group = Frame(master=window, pady=20, padx=10, bg="#FAFAFA")
    random.shuffle(choices)
    index = 0
    for choice in choices:
        if question_type == 'MCQ':
            Checkbutton(choice_group, text=choice, bg="#FAFAFA", highlightthickness=0, command=lambda choice=choice: command(choice, True)).grid(row=index, column=0, sticky="w")
        else:
            Radiobutton(choice_group, text=choice, value=choice, bg="#FAFAFA", highlightthickness=0, command=lambda choice=choice: command(choice)).grid(row=index, column=0, sticky="w")
        
        index += 1
    choice_group.pack(fill=X)