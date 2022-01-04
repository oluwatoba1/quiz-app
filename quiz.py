import random
import json
from datetime import datetime

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
    module_code = None
    lbl_notify = None

    def show_quiz_categories(self, module, question, isReport=False):
        self.module_model = module
        self.question_model = question
        self.initialize(rebuild=True)
    
        with open("assets/modules.json", "r+") as m:
            modules = json.load(m)
            options = []
            for module in modules:
                command = lambda module_code=module["code"]: self.play(
                            module_code=module_code
                        )
                if isReport:
                    command = lambda module_code=module["code"]: self.show_report(module_code)

                options.append(
                    {
                        "text": module["name"],
                        "command": command,
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
        self.module_code = module_code
        for _ in range(5):
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
        self.update_questions()
        self.save_result()

        frame = Frame(self.get_window(), bg="#FAFAFA")

        canvas = Canvas(
            frame, bg="#FAFAFA", height=600, width=600, scrollregion=(0, 0, 1000, 1000)
        )
        canvas_frame = Frame(canvas, bg="#FAFAFA")
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw", tags="result")

        scrollbar = Scrollbar(frame, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side=BOTTOM, anchor=NW, fill="y", expand=True)

        Label(
            canvas_frame,
            text="Result",
            foreground="black",
            font=("Arial", 20),
        ).pack()
        Label(
            canvas_frame,
            text=self.display_result_reaction(),
            bg="#FAFAFA",
            foreground="black",
            font=("Arial", 16),
        ).pack()
        Label(
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
                text=f"{question['question']} ({question['score']} points)",
                bg="#FAFAFA",
                wraplength=500,
                justify=LEFT,
            ).pack()

            # question_type = question["question_type"]
            # choices = question["choices"]
            answers = self.answers[index - 1]

            # options and user choice(s)
            # generate_quiz_options(
            #     question_group,
            #     question_type,
            #     choices,
            #     command=None,
            #     disabled=True,
            #     answers=answers,
            # )

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
        Button(
            master=canvas_frame,
            text="Back",
            command=lambda: self.launch(
                self.module, self.question, self.show_quiz_categories, rebuild=True
            ),
        ).pack()

        frame.pack()

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

    def update_questions(self):
        with open("assets/questions.json", "r+") as q:
            try:
                questions = json.load(q)
            except:
                questions = []
            
            for sq in self.session_questions:
                for question in questions:
                    if question["id"] == sq["id"]:
                        question["answered_count"] += 1
                        break

            q.seek(0)
            json.dump(questions, q)
            q.truncate()
    
    def save_result(self):
        # module code
        # total score
        # date
        with open("assets/results.json", "r+") as r:
            try:
                results = json.load(r)
            except:
                results = []

            save_data = {
                "module": self.module_code,
                "total_score": int(round(self.score/self.total_score * 100)),
                "date": datetime.now().strftime("%d-%m-%Y")
            }

            results.append(save_data)

            r.seek(0)
            json.dump(results, r)
            r.truncate()


        return None

    def show_report(self, module_code):
        self.initialize(rebuild=True, window_size="700x550")
        with open("assets/results.json") as r, open("assets/questions.json") as q:
            try:
                results = json.load(r)
                questions = json.load(q)
            except:
                self.launch(
                    self.module, self.question, self.show_quiz_categories, rebuild=True
                )
            
            total_quizzes = len(list(filter(lambda result: result["module"] == module_code, results)))
            scores_list = [result["total_score"] for result in results]
            total_score = 0
            average_score = 0
            count = 0
            for score in scores_list:
                total_score += score
                count += 1
            average_score = int(round(total_score / count))

            max_score = max(scores_list)
            min_score = min(scores_list)


            module_questions = list(filter(lambda question: question["module"] == module_code, questions))
            module_questions.sort(key=lambda q: q.get("answered_count"), reverse=True)
            frequent_questions = [question["question"] for question in module_questions[:2]]

            Label(self.get_window(), text='Quizzer Report', font=('Helvetica', 20, 'bold')).pack()

            frame1 = Frame(self.get_window(), pady=20, padx=10, bg="#FAFAFA")
            frame2 = Frame(self.get_window(), pady=20, padx=10, bg="#FAFAFA")
            frame3 = Frame(self.get_window(), pady=20, padx=10, bg="#FAFAFA")
            frame_action = Frame(self.get_window(), pady=20, padx=10, bg="#FAFAFA")
            frame_notify = Frame(self.get_window(), pady=20, padx=10, bg="#FAFAFA")

            # No report available
            if len(frequent_questions) < 2:
                Label(frame1, text="No report available for this module!", font=("Arial", 16, "bold"), bg="#FAFAFA").grid(row=0, column=0, sticky="w")
                frame1.pack(fill=X)
                return

            # Number of quizzes taken
            Label(frame1, text="Number of quizzes taken: ", font=("Arial", 16, "bold"), bg="#FAFAFA").grid(row=0, column=0, sticky="w")
            Label(frame1, text=total_quizzes, font=("Arial", 16), bg="#FAFAFA").grid(row=0, column=1, sticky="e")

            # Scores
            Label(frame2, text="Average Score: ", font=("Arial", 16, "bold"), bg="#FAFAFA").grid(row=0, column=0, sticky="w")
            Label(frame2, text=average_score, font=("Arial", 16), bg="#FAFAFA").grid(row=0, column=1, sticky="e")

            Label(frame2, text="Highest Score: ", font=("Arial", 16, "bold"), bg="#FAFAFA").grid(row=1, column=0, sticky="w")
            Label(frame2, text=max_score, font=("Arial", 16), bg="#FAFAFA").grid(row=1, column=1, sticky="e")

            Label(frame2, text="Lowest Score: ", font=("Arial", 16, "bold"), bg="#FAFAFA").grid(row=2, column=0, sticky="w")
            Label(frame2, text=min_score, font=("Arial", 16), bg="#FAFAFA").grid(row=2, column=1, sticky="e")

            # Most frequent questions
            Label(frame3, text="Most Frequent Questions: ", font=("Arial", 16, "bold"), bg="#FAFAFA").grid(row=0, column=0, sticky="w")
            Label(frame3, text=f"1. {frequent_questions[0]}", font=("Arial", 16), bg="#FAFAFA", wraplength=680, justify=LEFT).grid(row=1, column=0, sticky="w")
            Label(frame3, text=f"2. {frequent_questions[1]}", font=("Arial", 16), bg="#FAFAFA", wraplength=680, justify=LEFT).grid(row=2, column=0, sticky="w")

            data = dict(total_quizzes=total_quizzes, average_score=average_score, max_score=max_score, min_score=min_score, frequent_questions=frequent_questions)

            # Back button
            back_btn = Button(
                master=frame_action,
                text="Back to Modules",
                command=lambda: self.show_quiz_categories(
                    self.module, self.question, isReport=True
                ),
            )

            # Export button
            export_btn = Button(
                master=frame_action,
                text="Export",
                command=lambda: self.export_report(**data),
            )

            # notifier
            self.lbl_notify = Label(
                master=frame_notify,
                text="",
                foreground="black",
                bg="#FAFAFA",
                font=("Arial", 12),
            )

            frame1.pack(fill=X)
            frame2.pack(fill=X)
            frame3.pack(fill=X)
            back_btn.grid(row=0, column=0, sticky="w")
            export_btn.grid(row=0, column=1, sticky="e")
            frame_action.pack(fill=X)
            frame_notify.pack(fill=X)
            self.lbl_notify.pack()

    def export_report(self, **kwargs):
        with open("assets/report.txt", "w+") as report:
            report.write(f"Number of quizzes taken: {kwargs['total_quizzes']} \n")
            report.write("\n")
            report.write(f"Average score: {kwargs['average_score']} \n")
            report.write(f"Highest score: {kwargs['max_score']} \n")
            report.write(f"Lowest score: {kwargs['min_score']} \n")
            report.write("\n")
            report.write("Top 2 most frequent questions: \n")
            report.write(f"{kwargs['frequent_questions'][0]} \n")
            report.write(f"{kwargs['frequent_questions'][1]} \n")
        self.notify(self.lbl_notify, "Exported successfully!")
            