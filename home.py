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
            {"text": "Module", "command": module},
            {"text": "Questions", "command": lambda: question(module, quiz)},
            {"text": "Take Quiz", "command": lambda: quiz(module, question)},
            {"text": "Generate Report", "command": lambda: quiz(module, question, isReport=True)},
            {"text": "Exit", "command": None},
        ]
        self.show_options(options)

    def show_options(self, options, header="WELCOME TO QUIZ MASTER"):
        """
        Shows list of options for user to select
        """

        frame = Frame(self._window, relief="sunken", bg="white")

        self.canvas = Canvas(frame, bg="#FAFAFA", height=500, width=500)
        scrollheight = (len(options) + 1) * 50
        self.canvas.configure(scrollregion=(0, 0, scrollheight, scrollheight))
        canvas_frame = Frame(self.canvas, bg="#FAFAFA")
        self.canvas.create_window(
            (0, 0), window=canvas_frame, anchor="nw", tags="frame"
        )

        scrollbar = Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side=BOTTOM, anchor=NW, fill="both", expand=True)

        frame.pack(anchor=W, fill="both", expand=True, padx=0, pady=10)

        for option in options:
            Button(
                canvas_frame,
                text=option["text"],
                width=55,
                height=2,
                bg="#333",
                fg="#FFF",
                command=option["command"] or self._window.destroy,
                wraplength=400,
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
