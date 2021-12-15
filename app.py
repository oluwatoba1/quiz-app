import json
import random
import getpass

from tkinter import *

from home import Home
from modules import Module
from questions import Question
from quiz import Quiz


if __name__ == "__main__":

    window = Tk(className="QUIZZER")
    window.grid_columnconfigure(0, weight=1)
    window.configure(background="#FAFAFA")
    home = Home(window)

    module_section = Module(window).show_section
    question_section = Question(window).show_section
    quiz_section = Quiz(window).show_quiz_categories

    home.launch(module_section, question_section, quiz_section)
N
