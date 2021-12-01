import json
import random
import getpass

from tkinter import *

class Home:
    """
        Home/Launch window
    """
    def __init__(self, window):
        self._window = window
        self.label = None
        self.module_class = None
        self.question_class = None

    def get_window(self):
        return self._window

    def all_children(self):
        _list = self._window.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())

        return _list

    def rebuild(self):
        """
            clear window and create new content
        """
        widget_list = self.all_children()
        for item in widget_list:
            item.pack_forget()
        # self._window = Tk(className="QUIZZER")

    def initialize(self, rebuild=False, window_size="550x500"):
        if rebuild:
            self.rebuild()

        self._window.geometry(window_size)

    def launch(self, module, question, quiz, rebuild=False):
        """
            first method of the application- the launcher method
        """
        self.initialize(rebuild)
        options = [
            {"text": "Take Quiz", "command": lambda: quiz(module, question)},
            {"text": "Module", "command": module},
            {"text": "Questions", "command": lambda: question(module, quiz)},
            {"text": "Exit", "command": None},
        ]
        self.show_options(options)

    def show_options(self, options, header="WELCOME TO QUIZ MASTER"):
        """
            Shows list of options for user to select
        """
        welcome = Label(text=header, foreground="black", font=("Arial", 16)).pack()

        frame = Frame(self._window, relief="sunken", bg="white")
        frame.pack(fill="both", expand=True, padx=0, pady=10)

        for option in options:
            Button(
                frame,
                text=option["text"],
                width=55,
                height=2,
                bg="#333",
                fg="#FFF",
                command=option["command"] or self._window.destroy,
            ).pack()

        self._window.mainloop()

    def list_items(self, modules, file, header, command, back, delete=False):
        self.initialize(rebuild=True)
        index = 0
        options = []
        for module in modules:
            index += 1
            options.append(
                {
                    "text": module["name"],
                    "command": lambda index=index, module=module: command(
                        modules=modules,
                        file=file,
                        index=index,
                        module=module,
                        delete=delete,
                    ),
                }
            )

        options.append({"text": "Back", "command": back})

        self.show_options(options, header=header)

    def clear_notify(self):
        self.label.config(text="")

    def notify(self, label, message="Failed", delay=3000):
        """
        notification method
        """
        self.label = label
        self.label.config(text=message)
        self._window.after(delay, self.clear_notify)
