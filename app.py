import json
import random
import getpass

from tkinter import *

from home import Home
from modules import Module
from questions import Question
from quiz import Quiz

user = []


def addModule():
    code = input("Enter module code (unique): \n")
    name = input("Enter module name: \n")

    module = Module(code, name)
    module.save()


def quizQuestions():
    if len(user) == 0:
        print("You must first login before adding questions.")
    elif len(user) == 2:
        if user[1] == "ADMIN":
            print("\n==========ADD QUESTIONS==========\n")
            ques = input("Enter the question that you want to add:\n")
            opt = []
            print("Enter the 4 options with character initials (A, B, C, D)")
            for _ in range(4):
                opt.append(input())
            ans = input("Enter the answer:\n")
            with open("assets/questions.json", "r+") as f:
                questions = json.load(f)
                dic = {"question": ques, "options": opt, "answer": ans}
                questions.append(dic)
                f.seek(0)
                json.dump(questions, f)
                f.truncate()
                print("Question successfully added.")
        else:
            print(
                "You don't have access to adding questions. Only admins are allowed to add questions."
            )


def createAccount():
    print("\n==========CREATE ACCOUNT==========")
    username = input("Enter your USERNAME: ")
    password = getpass.getpass(prompt="Enter your PASSWORD: ")
    with open("assets/user_accounts.json", "r+") as user_accounts:
        users = json.load(user_accounts)
        if username in users.keys():
            print(
                "An account of this Username already exists.\nPlease enter the login panel."
            )
        else:
            users[username] = [password, "PLAYER"]
            user_accounts.seek(0)
            json.dump(users, user_accounts)
            user_accounts.truncate()
            print("Account created successfully!")


def loginAccount():
    print("\n==========LOGIN PANEL==========")
    username = input("USERNAME: ")
    password = getpass.getpass(prompt="PASSWORD: ")
    with open("assets/user_accounts.json", "r") as user_accounts:
        users = json.load(user_accounts)
    if username not in users.keys():
        print("An account of that name doesn't exist.\nPlease create an account first.")
    elif username in users.keys():
        if users[username][0] != password:
            print(
                "Your password is incorrect.\nPlease enter the correct password and try again."
            )
        elif users[username][0] == password:
            print("You have successfully logged in.\n")
            user.append(username)
            user.append(users[username][1])


def logout():
    global user
    if len(user) == 0:
        print("You are already logged out.")
    else:
        user = []
        print("You have been logged out successfully.")


def rules():
    print(
        """\n==========RULES==========
1. Each round consists of 10 random questions. To answer, you must press A/B/C/D (case-insensitive).
Your final score will be given at the end.
2. Each question consists of 1 point. There's no negative point for wrong answers.
3. You can create an account from ACCOUNT CREATION panel.
4. You can login using the LOGIN PANEL. Currently, the program can only login and not do anything more.
	"""
    )


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
