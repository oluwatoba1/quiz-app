import json
from tkinter import *

from home import Home
from questions import Question
from quiz import Quiz


class Module(Home):
    """
    Fields:
        =>Code
        =>Name
    Functionalities:
        =>Create Module
        =>Update Module
        =>Delete Module
    """

    def show_section(self):
        """
        Shows actions users can perform in the module page
        """
        qc = Question(self.get_window()).show_section
        qz = Quiz(self.get_window()).show_quiz_categories
        self.initialize(rebuild=True)
        options = [
            {"text": "Add Module", "command": self.add_module},
            {"text": "Edit Module", "command": self.edit_module},
            {"text": "Delete Module", "command": self.delete_module},
            {
                "text": "Back",
                "command": lambda: self.launch(self.show_section, qc, qz, rebuild=True),
            },
        ]

        self.show_options(options, header="MODULE")

    def find_module(self, modules, code):
        exist = False
        for module in modules:
            if module["code"] == code:
                exist = True
                break

        return exist

    def add_module(self, **kwargs):
        """
        Shows the module form for creation or update
        """
        modules = None
        file = None
        index = None
        module = None
        self.initialize(rebuild=True)
        Label(text="Add Module", foreground="black", font=("Arial", 16)).pack()
        form_group = Frame(master=self.get_window(), pady=20, padx=10, bg="#FAFAFA")
        form_action = Frame(master=self.get_window(), pady=20, padx=10, bg="#FAFAFA")
        form_notify = Frame(master=self.get_window(), pady=10, padx=10, bg="#FAFAFA")
        # Module code
        lbl_code = Label(master=form_group, text="Module code: ", width=15)
        ent_code = Entry(master=form_group, width=40)

        # Module name
        lbl_name = Label(master=form_group, text="Module name: ", width=15)
        ent_name = Entry(master=form_group, width=40)

        # notifier
        lbl_notify = Label(
            master=form_notify,
            text="",
            foreground="black",
            bg="#FAFAFA",
            font=("Arial", 12),
        )

        save = lambda: self.save(ent_code, ent_name, lbl_notify)

        if len(kwargs) > 0:
            modules = kwargs["modules"]
            file = kwargs["file"]
            index = kwargs["index"]
            module = kwargs["module"]
            ent_code.insert(0, module["code"])
            ent_name.insert(0, module["name"])
            save = lambda: self.update_module(
                modules, dict(name=ent_name, code=ent_code), index, file, lbl_notify
            )

        # Save button
        btn_save = Button(
            master=form_action,
            text="Save",
            command=save,
        )

        # Back button
        btn_back = Button(
            master=form_action,
            text="Go back",
            command=self.show_section,
        )

        lbl_code.grid(row=0, column=0, sticky="w")
        ent_code.grid(row=0, column=1, pady=20, sticky="e")
        lbl_name.grid(row=1, column=0, sticky="w")
        ent_name.grid(row=1, column=1, pady=20, sticky="e")
        btn_back.grid(row=0, column=0, sticky="w")
        btn_save.grid(row=0, column=1, sticky="e")

        form_group.pack(fill=X)
        form_action.pack(fill=X)
        form_notify.pack(fill=X)
        lbl_notify.pack()

    def save(self, code, name, notify_label):
        """
        Save module functionality
        """
        with open("assets/modules.json", "r+") as m:
            try:
                modules = json.load(m)
            except:
                modules = []

            exist = self.find_module(modules, code.get())

            if not exist:
                module = {"code": code.get(), "name": name.get()}
                modules.append(module)
                m.seek(0)
                json.dump(modules, m)
                m.truncate()
                code.delete(0, "end")
                name.delete(0, "end")
                self.notify(notify_label, "Module added successfully!")
            else:
                message = f"Module with code: {code.get()} already exists!"
                self.notify(notify_label, message)

    def update_module(self, modules, module, choice, file, notify_label):
        """
        Update module functionality
        """
        name = module["name"]
        code = module["code"]
        modules[choice - 1]["name"] = name.get()
        modules[choice - 1]["code"] = code.get()
        file.seek(0)
        json.dump(modules, file)
        file.truncate()
        self.notify(notify_label, "Module updated successfully!")

    def edit_module(self):
        """
        Shows modules for update
        """
        with open("assets/modules.json", "r+") as m:
            modules = json.load(m)
            self.list_items(
                modules,
                m,
                "Select module for update",
                self.add_module,
                self.show_section,
            )

    def delete_module(self):
        with open("assets/modules.json", "r+") as m:
            modules = json.load(m)

            self.list_items(
                modules,
                m,
                "Select module for deletion",
                self.confirmation_page,
                self.show_section,
            )

    def confirmation_page(self, modules, file, index, module, delete=False):
        """
        Popup to confirm deletion of module
        """
        window = Tk(className="Confirmation")
        window.configure(background="#FAFAFA")

        Label(
            master=window,
            text=f'Are you sure you want to delete: {module["name"]}',
            foreground="black",
            font=("Arial", 14),
        ).pack()

        form_action = Frame(master=window, pady=20, bg="#FAFAFA")

        btn_yes = Button(
            master=form_action,
            text="Yes",
            command=lambda: self.delete(window, modules, file, index),
        )

        btn_no = Button(master=form_action, text="No", command=window.destroy)

        form_action.pack()

        btn_no.grid(row=0, column=0, sticky="w")
        btn_yes.grid(row=0, column=1, sticky="e")

        window.mainloop()

    def delete(self, window, modules, file, choice):
        """
        Delete functionality
        """
        with open("assets/questions.json", "r+") as q:
            form_notify = Frame(master=window, pady=10, bg="#FAFAFA")
            # notifier
            lbl_notify = Label(
                master=form_notify,
                foreground="black",
                bg="#FAFAFA",
                font=("Arial", 14),
            )
            try:
                questions = json.load(q)
            except:
                questions = []
            module = modules[choice - 1]
            module_questions = list(
                filter(lambda question: question["module"] == module["code"], questions)
            )
            if len(module_questions) > 0:
                print("has questions")
                lbl_notify.config(text="Deletion failed, module has questions")
            else:
                del modules[choice - 1]
                file.seek(0)
                json.dump(modules, file)
                file.truncate()

                # notifier
                # lbl_notify = Label(
                #     master=form_notify,
                #     text="Module deleted",
                #     foreground="black",
                #     bg="#FAFAFA",
                #     font=("Arial", 16),
                # )
                lbl_notify.config(text="Module deleted")

            form_notify.pack()
            lbl_notify.pack()

            window.after(3000, window.destroy)
            self.show_section()
