import json
from tkinter import *

from home import Home


class Question(Home):
    """
    Fields:
        =>Module
        =>Question
        =>Question Type
        =>Options
        =>Answer
        =>Score
    Functionalities:
        =>Create Question
        =>Update Question
        =>Delete Question
    """

    form_group = None
    module_selected = None
    lbl_module = None
    option_module = None
    lbl_question = None
    txt_question = None
    lbl_type = None
    option_type = None
    lbl_options = None
    ent_option1 = None
    ent_option2 = None
    ent_option3 = None
    ent_option4 = None
    lbl_answer = None
    ent_answer1 = None
    ent_answer2 = None
    ent_answer3 = None
    ent_answer4 = None
    tf_answer_selected = None
    option_answer = None
    lbl_score = None
    ent_score = None
    lbl_notify = None
    scrollbar = None
    canvas = None

    MODULE_OPTIONS = {}
    MODULE_KEYS = {}
    TYPE_OPTIONS = {
        "Multiple-Choice Question": "MCQ",
        "True-False Question": "TF",
        "Best Match Question": "BM",
    }
    MODULE_DEFAULT = "Select a module"
    TYPE_DEFAULT = "Select a question type"
    ANSWER_DEFAULT = "Select the correct answer"
    mc = None
    module = None
    qz = None

    def show_section(self, mc, qz):
        self.initialize(rebuild=True)
        self.mc = mc
        self.qz = qz
        options = [
            {"text": "Create Question", "command": self.add_or_update_question},
            {"text": "Update Question", "command": self.show_modules},
            {
                "text": "Remove Question",
                "command": lambda: self.show_modules(delete=True),
            },
            {
                "text": "Back",
                "command": lambda: self.launch(
                    self.mc, self.show_section, self.qz, rebuild=True
                ),
            },
        ]

        self.show_options(options, header="QUESTION")

    def show_answer_options(self, selection):

        self.ent_answer1.grid(row=7, column=1, sticky="e")

        if selection != "True-False Question":
            self.lbl_options.grid(row=3, column=0, sticky="w")
            self.ent_option1.grid(row=3, column=1, sticky="e")
            self.ent_option2.grid(row=4, column=1, sticky="e")
            self.ent_option3.grid(row=5, column=1, sticky="e")
            self.ent_option4.grid(row=6, column=1, pady=(0, 10), sticky="e")
        else:
            self.lbl_options.grid_remove()
            self.ent_option1.grid_remove()
            self.ent_option2.grid_remove()
            self.ent_option3.grid_remove()
            self.ent_option4.grid_remove()

        if selection == "Multiple-Choice Question":
            self.ent_answer2.grid(row=8, column=1, sticky="e")
            self.ent_answer3.grid(row=9, column=1, sticky="e")
            self.ent_answer4.grid(row=10, column=1, pady=(0, 10), sticky="e")
            self.option_answer.grid_remove()
        elif selection == "True-False Question":
            self.ent_answer1.grid_remove()
            self.ent_answer2.grid_remove()
            self.ent_answer3.grid_remove()
            self.ent_answer4.grid_remove()
            self.option_answer.grid(row=7, column=1, pady=(0, 10), sticky="e")

        else:
            self.ent_answer2.grid_remove()
            self.ent_answer3.grid_remove()
            self.ent_answer4.grid_remove()
            self.option_answer.grid_remove()

        self.canvas.configure(scrollregion=(0, 0, 550, 550))

    def add_or_update_question(self, question=None):
        save_command = self.save
        self.initialize(rebuild=True)
        with open("assets/modules.json", "r+") as m:
            modules = json.load(m)
            index = 0
            text = "Create Question"
            back_command = lambda: self.show_section(self.mc, self.qz)
            if question:
                text = "Update Question"
                back_command = lambda: self.show_related_questions(module=self.module)

            for module in modules:
                self.MODULE_OPTIONS[module["name"]] = module["code"]
                index += 1

            frame = Frame(self.get_window(), bg="#FAFAFA")

            self.canvas = Canvas(frame, bg="#FAFAFA", height=500, width=500)
            self.canvas.configure(scrollregion=(0, 0, 550, 550))
            canvas_frame = Frame(self.canvas, bg="#FAFAFA")
            self.canvas.create_window(
                (0, 0), window=canvas_frame, anchor="nw", tags="frame"
            )

            scrollbar = Scrollbar(frame, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            self.canvas.pack(side=BOTTOM, anchor=NW, fill="both", expand=True)
            frame.pack(anchor=W, fill="x")

            # self.canvas.create_line(0, 0, 500, 1000)
            # self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            Label(
                master=canvas_frame, text=text, foreground="black", font=("Arial", 16)
            ).pack()
            self.form_group = Frame(canvas_frame, pady=10, padx=10, bg="#FAFAFA")
            form_action = Frame(canvas_frame, pady=10, padx=10, bg="#FAFAFA")
            form_notify = Frame(canvas_frame, pady=10, padx=10, bg="#FAFAFA")

            # Module
            self.module_selected = StringVar(self.form_group)
            self.module_selected.set(self.MODULE_DEFAULT)
            self.lbl_module = Label(master=self.form_group, text="Module: ", width=20)
            self.option_module = OptionMenu(
                self.form_group, self.module_selected, *self.MODULE_OPTIONS.keys()
            )
            self.option_module.configure(width=35)

            # Question
            self.lbl_question = Label(
                master=self.form_group, text="Question: ", width=20
            )
            self.txt_question = Text(master=self.form_group, width=40, height=3)

            # Question Type
            self.type_selected = StringVar(self.form_group)
            self.type_selected.set(self.TYPE_DEFAULT)
            self.lbl_type = Label(
                master=self.form_group, text="Question Type: ", width=20
            )
            self.option_type = OptionMenu(
                self.form_group,
                self.type_selected,
                *self.TYPE_OPTIONS.keys(),
                command=lambda selection: self.show_answer_options(selection),
            )

            self.option_type.configure(width=35)

            # Options
            self.lbl_options = Label(master=self.form_group, text="Options: ", width=20)
            self.ent_option1 = Entry(master=self.form_group, width=40)
            self.ent_option2 = Entry(master=self.form_group, width=40)
            self.ent_option3 = Entry(master=self.form_group, width=40)
            self.ent_option4 = Entry(master=self.form_group, width=40)

            # Correct answer
            self.lbl_answer = Label(master=self.form_group, text="Answer: ", width=20)
            self.ent_answer1 = Entry(master=self.form_group, width=40)
            self.ent_answer2 = Entry(master=self.form_group, width=40)
            self.ent_answer3 = Entry(master=self.form_group, width=40)
            self.ent_answer4 = Entry(master=self.form_group, width=40)

            # True/False options
            self.tf_answer_selected = StringVar(self.form_group)
            self.tf_answer_selected.set(self.ANSWER_DEFAULT)
            self.option_answer = OptionMenu(
                self.form_group, self.tf_answer_selected, *["True", "False"]
            )

            self.option_answer.configure(width=35)

            # Question score
            self.lbl_score = Label(master=self.form_group, text="Score: ", width=20)
            self.ent_score = Entry(master=self.form_group, width=40)

            # Answer explanation
            self.lbl_explanation = Label(
                master=self.form_group, text="Answer Explanation: ", width=20
            )
            self.ent_explanation = Entry(master=self.form_group, width=40)

            if question:
                save_command = lambda: self.save(question["id"])

                for key in self.MODULE_OPTIONS.keys():
                    if self.MODULE_OPTIONS[key] == question["module"]:
                        self.module_selected.set(key)
                        break

                self.txt_question.insert("1.0", question["question"])

                for key in self.TYPE_OPTIONS.keys():
                    if self.TYPE_OPTIONS[key] == question["question_type"]:
                        self.type_selected.set(key)
                        self.show_answer_options(key)
                        break

                if question["question_type"] != "TF":
                    self.ent_option1.insert(0, question["choices"][0])
                    self.ent_option2.insert(0, question["choices"][1])
                    self.ent_option3.insert(0, question["choices"][2])
                    self.ent_option4.insert(0, question["choices"][3])
                    answers = []
                    index = 0
                    limit = 4
                    question_length = len(question["answers"])

                    while index < limit:
                        if index < question_length:
                            answers.append(question["answers"][index])
                        else:
                            answers.append("")
                        index += 1

                    self.ent_answer1.insert(0, answers[0])
                    self.ent_answer2.insert(0, answers[1])
                    self.ent_answer3.insert(0, answers[2])
                    self.ent_answer4.insert(0, answers[3])
                else:
                    self.tf_answer_selected.set(question["answers"][0])

                self.ent_score.insert(0, question["score"])
                self.ent_explanation.insert(0, question["explanation"])

            # notifier
            self.lbl_notify = Label(
                master=form_notify,
                text="",
                foreground="black",
                bg="#FAFAFA",
                font=("Arial", 12),
            )

            # Save button
            btn_save = Button(
                master=form_action,
                text="Save",
                command=save_command,
            )

            # Back button
            btn_back = Button(
                master=form_action,
                text="Go back",
                command=back_command,
            )

            self.lbl_module.grid(row=0, column=0, sticky="w")
            self.option_module.grid(row=0, column=1, pady=10, sticky="e")

            self.lbl_question.grid(row=1, column=0, sticky="w")
            self.txt_question.grid(row=1, column=1, pady=10, sticky="e")

            self.lbl_type.grid(row=2, column=0, sticky="w")
            self.option_type.grid(row=2, column=1, pady=10, sticky="e")

            self.lbl_answer.grid(row=7, column=0, sticky="w")
            self.ent_answer1.grid(row=7, column=1, sticky="e")

            self.lbl_score.grid(row=11, column=0, sticky="w")
            self.ent_score.grid(row=11, column=1, pady=10, sticky="e")

            self.lbl_explanation.grid(row=12, column=0, sticky="w")
            self.ent_explanation.grid(row=12, column=1, pady=10, sticky="e")

            btn_back.grid(row=0, column=0, sticky="w")
            btn_save.grid(row=0, column=1, pady=10, sticky="e")

            self.form_group.pack(fill=BOTH)
            form_action.pack(fill=BOTH)
            form_notify.pack(fill=BOTH)
            self.lbl_notify.pack()

            self.canvas.configure(scrollregion=(0, 0, 550, 550))

    def validate_and_save(self, save_data, question_type, questions, q, index):
        message = "Question created successfully!"
        string_fields = ["module", "question", "question_type", "score", "explanation"]
        list_fields = ["choices", "answers"]

        for key in save_data:
            if (key in string_fields and not save_data[key]) or save_data[key] in [
                self.MODULE_DEFAULT,
                self.TYPE_DEFAULT,
            ]:
                self.notify(self.lbl_notify, f'{key.replace("_", " ")} is empty', 5000)
                break
            elif (
                key in list_fields
                and key == "choices"
                and len(save_data[key]) < 4
                and question_type != "TF"
            ):
                self.notify(self.lbl_notify, "You must have four choices", 5000)
                break
            elif key in list_fields and len(save_data[key]) < 1:
                if question_type != "TF":
                    self.notify(
                        self.lbl_notify, "You must have at least one answer", 5000
                    )
                break
            elif key in list_fields and self.ANSWER_DEFAULT in save_data[key]:
                self.notify(self.lbl_notify, "Select an answer", 5000)
                break

        else:
            if index is None:
                questions.append(save_data)
                q.seek(0)
                json.dump(questions, q)
                q.truncate()
                self.module_selected.set(self.MODULE_DEFAULT)
                self.txt_question.delete("1.0", "end")
                self.type_selected.set(self.TYPE_DEFAULT)
                self.tf_answer_selected.set(self.ANSWER_DEFAULT)
                self.ent_option1.delete(0, "end")
                self.ent_option2.delete(0, "end")
                self.ent_option3.delete(0, "end")
                self.ent_option4.delete(0, "end")
                self.ent_answer1.delete(0, "end")
                self.ent_answer2.delete(0, "end")
                self.ent_answer3.delete(0, "end")
                self.ent_answer4.delete(0, "end")
                self.ent_score.delete(0, "end")
                self.ent_explanation.delete(0, "end")
            else:
                message = "Question updated successfully!"
                questions[index] = save_data
                q.seek(0)
                json.dump(questions, q)
                q.truncate()

            self.notify(self.lbl_notify, message)

    def save(self, index=None):
        with open("assets/questions.json", "r+") as q:
            questions = json.load(q) or []
            module = self.MODULE_OPTIONS[self.module_selected.get()] or ""
            question = self.txt_question.get("1.0", END)
            question_type = ""
            if self.type_selected.get() in self.TYPE_OPTIONS:
                question_type = self.TYPE_OPTIONS[self.type_selected.get()]
            choices = []
            answers = []

            if question_type == "TF":
                choices = ["True", "False"]
                answers = [self.tf_answer_selected.get()]
            else:
                choices = [
                    self.ent_option1.get(),
                    self.ent_option2.get(),
                    self.ent_option3.get(),
                    self.ent_option4.get(),
                ]
                answers = [
                    self.ent_answer1.get(),
                    self.ent_answer2.get(),
                    self.ent_answer3.get(),
                    self.ent_answer4.get(),
                ]
                choices = [choice for choice in choices if choice.strip()]
                answers = [answer for answer in answers if answer.strip()]

            question_score = self.ent_score.get()
            answer_explanation = self.ent_explanation.get()

            save_data = {
                "module": module,
                "question": question.strip(),
                "question_type": question_type,
                "choices": choices,
                "answers": answers,
                "score": question_score,
                "explanation": answer_explanation,
            }

            self.validate_and_save(save_data, question_type, questions, q, index)

    def show_modules(self, delete=False):
        with open("assets/modules.json", "r+") as m:
            modules = json.load(m)
            self.list_items(
                modules,
                m,
                "Select module to view available questions",
                self.show_related_questions,
                lambda: self.show_section(self.mc, self.qz),
                delete=delete,
            )

    def show_related_questions(
        self, modules=None, file=None, index=None, module=None, delete=False
    ):
        self.module = module
        with open("assets/questions.json", "r+") as q:
            questions = json.load(q)
            index = 0
            filtered_questions = []

            for question in questions:
                if question["module"] == self.module["code"]:
                    question["id"] = index
                    filtered_questions.append(question)
                index += 1

            options = []

            self.initialize(rebuild=True)

            for question in filtered_questions:
                command = lambda question=question: self.add_or_update_question(
                    question
                )
                if delete:
                    command = lambda question=question: self.confirmation_page(
                        questions, question, q
                    )
                options.append({"text": question["question"], "command": command})
            options.append(
                {
                    "text": "Back",
                    "command": self.show_modules,
                }
            )

            self.show_options(options, header="Questions")

    def confirmation_page(self, questions, question, file):
        window = Tk(className="Confirmation")
        window.configure(background="#FAFAFA")

        Label(
            master=window,
            text=f'Are you sure you want to delete: {question["question"]}',
            foreground="black",
            font=("Arial", 14),
        ).pack()

        form_action = Frame(master=window, pady=20, bg="#FAFAFA")

        btn_yes = Button(
            master=form_action,
            text="Yes",
            command=lambda: self.delete(window, questions, question, file),
        )

        btn_no = Button(master=form_action, text="No", command=window.destroy)

        form_action.pack()

        btn_no.grid(row=0, column=0, sticky="w")
        btn_yes.grid(row=0, column=1, sticky="e")

        window.mainloop()

    def delete(self, window, questions, question, file):

        del questions[question["id"]]
        file.seek(0)
        json.dump(questions, file)
        file.truncate()
        form_notify = Frame(master=window, pady=10, bg="#FAFAFA")

        # notifier
        lbl_notify = Label(
            master=form_notify,
            text="Question removed",
            foreground="black",
            bg="#FAFAFA",
            font=("Arial", 16),
        )

        form_notify.pack()
        lbl_notify.pack()

        window.after(2000, window.destroy)
        self.show_section(self.mc, self.qz)
