import random
import json

from tkinter import *
from utilities import *

from home import Home


class Quiz(Home):

    session_questions = []
    answers = []
    page = 1
    btn_next = None
    btn_submit = None

    def show_quiz_categories(self, module, question):
        self.initialize(rebuild=True)
        with open("assets/modules.json", "r+") as m:
            modules = json.load(m)
            options = []
            for module in modules:
                options.append(
                    {
                        "text": module["name"],
                        "command": lambda module_code=module["code"]: self.play(
                            module_code=module_code
                        ),
                    }
                )
            options.append(
                {
                    "text": "Back",
                    "command": lambda: self.launch(
                        module, question, self.show_quiz_categories, rebuild=True
                    ),
                }
            )

            self.show_options(options, header="Select Test Module")

    def play(self, module_code):
        # print("\n==========QUIZ START==========")
        # score = 0
        # with open("assets/questions.json", "r+") as q:
        #     j = json.load(f)
        #     for i in range(10):
        #         no_of_questions = len(j)
        #         ch = random.randint(0, no_of_questions - 1)
        #         print(f'\nQ{i+1} {j[ch]["question"]}\n')
        #         for option in j[ch]["options"]:
        #             print(option)
        #         answer = input("\nEnter your answer: ")
        #         if j[ch]["answer"][0] == answer[0].upper():
        #             print("\nYou are correct")
        #             score += 1
        #         else:
        #             print("\nYou are incorrect"
        #         del j[ch]
        #     print(f"\nFINAL SCORE: {score}/10")
        for i in range(5):
            self.answers.append([])
        print(self.answers)
        self.initialize(rebuild=True, window_size="500x400")
        with open("assets/questions.json", "r+") as q:
            questions = json.load(q)
            module_questions = list(
                filter(lambda question: question["module"] == module_code, questions)
            )
            self.session_questions = random.sample(module_questions, 5)
            print("####questions####")
            print(self.session_questions)

            self.display_current_question()

    def show_question(self, page=None):
        if page is None:
            page = self.page
        Label(
            text=f"Question {str(page)}", foreground="black", font=("Arial", 16)
        ).pack()
        question_group = Frame(master=self.get_window(), pady=20, padx=10, bg="#FAFAFA")
        Label(
            master=question_group,
            text=self.session_questions[page - 1]["question"],
            bg="#FAFAFA",
            wraplength=500,
            justify=LEFT,
        ).pack()
        question_group.pack(fill=X)
        generate_quiz_options(
            self.get_window(),
            self.session_questions[page - 1]["question_type"],
            self.session_questions[page - 1]["choices"],
            self.on_click,
        )

    def display_current_question(self):
        self.show_question()

        navigation_group = Frame(
            master=self.get_window(), pady=20, padx=10, bg="#FAFAFA"
        )

        # Next button
        self.btn_next = Button(
            master=navigation_group,
            text="Next",
            command=lambda: self.navigate("next"),
        )

        # Submit button
        self.btn_submit = Button(
            master=navigation_group,
            text="Submit",
            command=self.submit,
        )

        self.btn_next.grid(row=0, column=1, sticky="w")
        navigation_group.pack(fill=X)

    def navigate(self, action):
        if action == "next":
            self.page = self.page + 1
        else:
            self.page = None
        self.initialize(rebuild=True)
        self.display_current_question()

        if self.page == 5:
            self.btn_next.grid_remove()
            self.btn_submit.grid(row=0, column=1, sticky="e")

    def on_click(self, choice, checkbox=None):
        if checkbox:
            if choice in self.answers[self.page - 1]:
                self.answers[self.page - 1].remove(choice)
                print(self.answers)
                return None
            self.answers[self.page - 1].append(choice)
        else:
            self.answers[self.page - 1] = [choice]
        print(self.answers)

    def submit(self):
        self.initialize(True)
        canvas = Canvas(self.get_window(), bg="#FAFAFA", height=500, width=500)
        canvas.configure(scrollregion=(0, 0, 550, 550))
        canvas_frame = Frame(canvas, bg="#FAFAFA")
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw", tags="frame")

        scrollbar = Scrollbar(
            self.get_window(), orient="vertical", command=canvas.yview
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side=BOTTOM, anchor=NW, fill="both", expand=True)

        index = 1
        for question in self.session_questions:
            Label(
                master=canvas_frame,
                text=f"Question {str(index)}",
                foreground="black",
                font=("Arial", 16),
            ).pack()

            question_group = Frame(master=canvas_frame, pady=20, padx=10, bg="#FAFAFA")
            Label(
                master=question_group,
                text=self.session_questions[index - 1]["question"],
                bg="#FAFAFA",
                wraplength=500,
                justify=LEFT,
            ).pack()

            Label(
                master=question_group,
                text=f"Your answer was {self.answers[index - 1][0]}",
                bg="#FAFAFA",
                wraplength=500,
                justify=LEFT,
            ).pack()
            question_group.pack(fill=X)
            index += 1
        canvas.configure(scrollregion=(0, 0, 550, 550))
