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
    score = 0
    total_score = 0
    module = None
    question = None

    def show_quiz_categories(self, module, question):
        self.module_model = module
        self.question_model = question
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
        self.initialize(True, "600x600")
        score = self.compute_score()

        frame = Frame(self.get_window(), bg="#FAFAFA")

        canvas = Canvas(
            frame, bg="#FAFAFA", height=600, width=600, scrollregion=(0, 0, 1200, 1200)
        )
        # canvas.configure()
        canvas_frame = Frame(canvas, bg="#FAFAFA")
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw", tags="result")

        scrollbar = Scrollbar(frame, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side=BOTTOM, anchor=NW, fill="y", expand=True)

        header = Label(
            canvas_frame,
            text="Result",
            foreground="black",
            font=("Arial", 20),
        ).pack()
        header = Label(
            canvas_frame,
            text=self.display_result_reaction(),
            bg="#FAFAFA",
            foreground="black",
            font=("Arial", 16),
        ).pack()
        result = Label(
            canvas_frame,
            text=f"Your score is: {score}",
            bg="#FAFAFA",
            foreground="black",
            font=("Arial", 16),
        ).pack()

        index = 1
        for question in self.session_questions:
            # Question no#
            Label(
                master=canvas_frame,
                text=f"Question {str(index)}",
                foreground="black",
                font=("Arial", 16),
            ).pack()

            question_group = Frame(master=canvas_frame, pady=20, padx=10, bg="#FAFAFA")
            # The question itself
            Label(
                master=question_group,
                text=question["question"],
                bg="#FAFAFA",
                wraplength=500,
                justify=LEFT,
            ).pack()

            question_type = question["question_type"]
            choices = question["choices"]
            answers = self.answers[index - 1]

            # options and user choice(s)
            generate_quiz_options(
                question_group,
                question_type,
                choices,
                command=None,
                disabled=True,
                answers=answers,
            )

            # Answer explanation
            explanation = self.get_explanation(question, answers)
            Label(
                master=question_group,
                text=explanation,
                bg="#FAFAFA",
                wraplength=500,
                justify=LEFT,
            ).pack()
            question_group.pack(fill=X)
            index += 1

        # Back button
        btn_back = Button(
            master=canvas_frame,
            text="Back to Home",
            command=lambda: self.launch(
                self.module, self.question, self.show_quiz_categories, rebuild=True
            ),
        ).pack()

        canvas.configure(scrollregion=(0, 0, 1200, 1200))

    def mark_questions(self):
        index = 0
        for question in self.session_questions:
            if (sorted(question["answers"]) == sorted(self.answers[index])) and (
                len(question["answers"]) == len(self.answers[index])
            ):
                self.score += int(question["score"])
            self.total_score += int(question["score"])
            index += 1

    def compute_score(self):
        self.mark_questions()

        return f"{str(self.score)}/{str(self.total_score)}"

    def display_result_reaction(self):
        comment = ""
        result_percentage = self.score / self.total_score * 100
        if result_percentage >= 90:
            comment = "Awesome!!!!"
        elif result_percentage >= 80:
            comment = "Great!!!"
        elif result_percentage >= 70:
            comment = "Nice!!"
        elif result_percentage >= 50:
            comment = "Not bad!"
        else:
            comment = "Eish :("

        return comment

    def get_explanation(self, question, answer):
        suffix = ""
        prefix = "Your answer was "
        is_correct_str = " which is INCORRECT"
        if len(answer) == 1:
            suffix = answer[0]

        else:
            prefix = "Your answers were "
            for i in range(len(answer)):
                if i == len(answer) - 1:
                    suffix += f" and {answer[i]}"
                    continue
                elif i == 0:
                    suffix += f" {answer[i]}"
                    continue
                suffix += f", {answer[i]}"

        if (sorted(question["answers"]) == sorted(answer)) and (
            len(question["answers"]) == len(answer)
        ):
            is_correct_str = " which is CORRECT"
            question["explanation"] = ""

        explanation = prefix + suffix + is_correct_str + ". " + question["explanation"]
        return explanation
