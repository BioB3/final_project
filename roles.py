import datetime

class request:
    def __init__(self, table) -> None:
        self.__table = table

    @property
    def get_tab(self):
        return self.__table

    def create_r(self, project_id, person_table, from_role, to_be, user_id = ""):
        if to_be != "evaluate":
            if from_role == "faculty":
                people = person_table.filter(lambda x: x["type"] == from_role or x["type"] == "advisor")
            elif from_role == "student":
                people = person_table.filter(lambda x: x["type"] == from_role)
            people_lst = people.select(["ID", "fist", "last"])
            print("\n List of people available:")
            for info in people_lst:
                print(info)
            recruit_id_lst = []
            while True:
                recruit_id = input("ID of the person (leave blank to submit): ")
                if recruit_id == "":
                    break
                if recruit_id not in [i["ID"] for i in people_lst]:
                    print("Invalid ID, please try again.")
                else:
                    recruit_id_lst.append(recruit_id)
            print()
            for _id in recruit_id_lst:
                temp_dict = {}
                temp_dict["ProjectID"] = project_id
                temp_dict[f"to_be_{to_be}"] = _id
                temp_dict['Response'] = ""
                temp_dict['Response_date'] = ""
                self.__table.insert(temp_dict)
                f_name = person_table.filter(lambda x: x["ID"] == _id).table[0]
                print(f"Sent request to {f_name['fist']} {f_name['last']}")
        elif to_be == "evaluate":
            people = person_table.filter(lambda x: x["type"] == "faculty" or x["type"] == "advisor"\
                and x["ID"] != user_id)
            people_lst = people.select(["ID", "fist", "last"])
            print("\n List of people available:")
            for info in people_lst:
                print(info)
            recruit_id_lst = []
            num_eval = input("Enter the number of evaluaters (min:3): ")
            while not num_eval.isdigit():
                num_eval = input("Please Enter a Valid Number: ")
            while int(num_eval) < 3 or int(num_eval) > len(people_lst):
                num_eval = input("Please Enter a Valid Number: ")
                if not num_eval.isdigit():
                    num_eval = 0
            for _ in range(0,3):
                recruit_id = input("ID of the person to be evaluater: ")
                while recruit_id not in [i["ID"] for i in people_lst] or recruit_id in recruit_id_lst:
                    recruit_id = input("Invalid or Duplicate ID, please try again: ")
                recruit_id_lst.append(recruit_id)
            print()
            for _id in recruit_id_lst:
                temp_dict = {}
                temp_dict["ProjectID"] = project_id
                temp_dict[f"to_evaluate"] = _id
                temp_dict['Response'] = ""
                temp_dict['Response_date'] = ""
                temp_dict['Comment'] = ""
                self.__table.insert(temp_dict)
                f_name = person_table.filter(lambda x: x["ID"] == _id).table[0]
                print(f"Sent request to {f_name['fist']} {f_name['last']}")

    def view_request(self, person_id, to_be, project_table):
        count = 0
        temp_tap = self.__table.filter(lambda x: x[f"to_be_{to_be}"] == person_id and\
            x["Response"] == "")
        for _ in temp_tap.select(["ProjectID"]):
            count += 1
            print(f"{count})")
            for n, m in _.items():
                print(f"|   {n} : {m}")
                temp_detail = project_table.get_tab.filter(lambda x: x["ProjectID"] == m).select(\
                    ["Title", "Detail"])[0]
                print(f"|   Title : {temp_detail['Title']}")
                print(f"|   Detail : {temp_detail['Detail']}")


    def view_status(self, project_id):
        if self.__table.filter(lambda x: x["ProjectID"] == project_id).table == []:
            print("There are no request recorded.")
        else:
            for _ in self.__table.filter(lambda x: x["ProjectID"] == project_id).table:
                print(_)

    def respond(self, project_id, person_id, to_be, proj, login_table = None,\
        person_table = None,):
        if login_table == None:
            response = "n"
        else:
            response = input("Enter your response (y/n) :")
            while response.lower() not in ["y", "n"]:
                response = input("Invalid Input. Please enter 'y' or 'n':")
        for _req in self.__table.table:
            if _req["ProjectID"] == project_id and _req[f"to_be_{to_be}"] == person_id:
                _req["Response_date"] = datetime.datetime.now().strftime("%d-%m-%Y")
                if response.lower() == "y":
                    _req["Response"] = "Accepted"
                    login_table.update("ID", person_id, "role", to_be)
                    person_table.update("ID", person_id, "type", to_be)
                    proj.p_update(project_id, to_be.capitalize(), person_id)
                    for _other_req in self.__table.table:
                        if to_be.lower() == "member" and _other_req["ProjectID"] != project_id\
                            and _other_req[f"to_be_{to_be}"] == person_id:
                            self.respond(_other_req["ProjectID"], person_id, to_be, proj)
                        if to_be.lower() == "member" and not proj.check_m_and_a(\
                            project_id, "member") and _other_req["Response"] == "":
                            self.respond(project_id, _other_req[f"to_be_{to_be}"], to_be, proj)
                        if to_be.lower() == "advisor":
                            proj.p_update(project_id, "Status", "in progress")
                            if _other_req["ProjectID"] == project_id\
                                and _other_req[f"to_be_{to_be}"] != person_id:
                                self.respond(project_id, _other_req[f"to_be_{to_be}"], to_be, proj)
                elif response.lower() == "n":
                    if to_be.lower() == "member" or to_be.lower() == "advisor":
                        _req["Response"] = "Rejected"

    def eval(self, project_id, user_id, project_table):
        project_table.show_status(project_id)
        for _req in self.__table.table:
            if _req["ProjectID"] == project_id and _req[f"to_evaluate"] == user_id:
                _req["Response_date"] = datetime.datetime.now().strftime("%d-%m-%Y")
                p_or_f = input("Passed or Failed: ").lower()
                while p_or_f not in ["passed", "failed"]:
                    p_or_f = input("Passed or Failed: ").lower()
                _req["Response"] = p_or_f
                _req["Comment"] = input("Enter Comment: ")
class project:
    def __init__(self, table) -> None:
        self.__table = table

    @property
    def get_tab(self):
        return self.__table

    def create_p(self, lead_id, login_table, person_table):
        temp_dict = {}
        temp_dict["ProjectID"] = str(len(self.__table.table) + 1)
        title = input("Enter Project's Title: ")
        temp_dict["Title"] = title
        temp_dict["Lead"] = lead_id
        temp_dict["Member1"] = ""
        temp_dict["Member2"] = ""
        temp_dict["Advisor"] = ""
        temp_dict["Status"] = "finding supervisor"
        temp_dict["Detail"] = ""
        login_table.update("ID", lead_id, "role", "lead")
        person_table.update("ID", lead_id, "type", "lead")
        self.__table.insert(temp_dict)

    def get_id(self, _id):
        return self.__table.filter(lambda x: x["Lead"] == _id or x["Member1"] == _id or\
            x["Member2"] == _id).table[0]["ProjectID"]

    def check_m_and_a(self, project_id, m_or_a):
        cw_dict = self.__table.filter(lambda x: x["ProjectID"] == project_id).table[0]
        if m_or_a == "member":
            if cw_dict["Member1"] != "" and cw_dict["Member2"] != "":
                return False
        elif m_or_a == "advisor":
            if cw_dict["Advisor"] != "":
                return False
        return True

    def p_update(self, project_id, key, value):
        cw_dict = self.__table.filter(lambda x: x["ProjectID"] == project_id).table[0]
        if key.lower() == "member" and cw_dict["Member1"] == "":
            key = "Member1"
        elif key.lower() == "member" and cw_dict["Member1"] != "":
            key = "Member2"
        self.__table.update("ProjectID", project_id, key, value)

    def show_status(self, project_id):
        temp_pj = self.__table.filter(lambda x: x["ProjectID"] == project_id).table[0]
        for _ in temp_pj:
            print(f"{_} : {temp_pj[_]}")

class User:
    def __init__(self, id, role, database) -> None:
        self.__id = id
        self.__role = role
        self.__database = database
        self.__project_table = project(self.__database.search("project"))
        self.__member_req = request(self.__database.search("member_pending_request"))
        self.__advisor_req = request(self.__database.search("advisor_pending_request"))
        self.__login_table = self.__database.search("login")
        self.__person_table = self.__database.search("persons")
        self.__evaluate_req = request(self.__database.search("evaluate_request"))

    def update_role(self):
        self.__role = self.__login_table.filter(lambda x: x["ID"] == self.__id).table[0]["role"]

    def menu(self):
        print(f"Welcome!" +
              f"{self.__person_table.filter(lambda x: x['ID'] == self.__id).table[0]['fist']}" +
              f" {self.__person_table.filter(lambda x: x['ID'] == self.__id).table[0]['last']}")
        self.update_role()
        print(f"Your role is {self.__role}. Please choose one of the following choice:")
        if self.__role == "student":
            print("• Inbox\n• Create a Project")
        elif self.__role == "lead":
            print("• Project Status\n• Invite Members\n• Invite Supervisor\n\
• View Invitations\n• Edit Project\n• Submit Project")
        elif self.__role == "member":
            print("• Project Status\n• Edit Project")
        elif self.__role == "faculty" or self.__role == "advisor":
            print("• Inbox\n• View Projects")
            if self.__role == "advisor":
                print("• Start Evaluation\n• View Evaluation\n• Approve Project")
        elif self.__role == "admin":
            print("• View Tables\n• Update Tables")
        print("• Exit")
        m_choice = input().lower()
        while m_choice != "exit":
            if m_choice == "Congrat! You broke my program.":
                break
            print()
            m_choice = self.navigate(m_choice.lower())
            print("*"*50)
        if m_choice == "exit":
            return
        print()
        self.menu()


    def navigate(self, choice):
        if choice == "inbox" and self.__role in ["student", "faculty", "advisor"]:
                self.inbox()
        elif choice == "create a project" and self.__role == "student":
            self.__project_table.create_p(self.__id, self.__login_table, self.__person_table)
        elif choice == "project status" and self.__role in ["member", "lead"]:
            self.__project_table.show_status(self.__project_table.get_id(self.__id))
        elif choice == "edit project" and self.__role in ["member", "lead"]:
            if self.__role == "member":
                changes = input("Enter Detail (leave blank to cancel) : ")
                if changes != "":
                    self.__project_table.p_update(self.__project_table.get_id(self.__id),\
                        "Detail", changes)
            elif self.__role == "lead":
                t_or_d = ""
                while t_or_d not in ["title", "detail"]:
                    t_or_d = input("Edit Title or Detail: ").lower()
                changes = input(f"Enter {t_or_d.capitalize()} (leave blank to cancel): ")
                if changes != "":
                    if t_or_d == "title":
                        self.__project_table.p_update(self.__project_table.get_id(self.__id),\
                            "Title", changes)
                    elif t_or_d == "detail":
                        self.__project_table.p_update(self.__project_table.get_id(self.__id),\
                            "Detail", changes)
        elif choice == "invite members" and self.__role == "lead":
            if self.__project_table.check_m_and_a(self.__project_table.get_id(self.__id), "member"):
                self.__member_req.create_r(self.__project_table.get_id(self.__id),\
                    self.__person_table, "student", "member")
            else:
                print("Your Project already have the maximum amount of member.")
        elif choice == "invite supervisor" and self.__role == "lead":
            if self.__project_table.check_m_and_a(self.__project_table.get_id(self.__id),\
                "advisor"):
                self.__advisor_req.create_r(self.__project_table.get_id(self.__id),\
                    self.__person_table, "faculty", "advisor")
            else:
                print("Your Project already have a supervisor.")
        elif choice == "view invitations" and self.__role == "lead":
            type_invite = input("Enter the type of Invitation (Member/Advisor): ").lower()
            while type_invite not in ["member", "advisor"]:
                type_invite = input("Please Enter a Valid Option: ").lower()
            if type_invite == "member":
                self.__member_req.view_status(self.__project_table.get_id(self.__id))
            elif type_invite == "advisor":
                self.__advisor_req.view_status(self.__project_table.get_id(self.__id))
        elif choice == "submit project" and self.__role == "lead":
            if not self.__project_table.check_m_and_a(self.__project_table.get_id(self.__id),\
                "advisor"):
                self.__project_table.p_update(self.__project_table.get_id(self.__id),\
                    "Status", "waiting for evaluation")
                print("report sent.")
            else:
                print("Your Project doesn't have a Supervisor.")
        elif choice == "view projects" and self.__role in ["faculty", "advisor"]:
            project_count = len(self.__project_table.get_tab.table)
            project_id_lst = []
            for num in range(1, project_count + 1):
                project_id_lst.append(num)
            print(f"Available Projects:\n{project_id_lst}")
            temp_pro_id = input("Enter Project id: ")
            while temp_pro_id not in [i["ProjectID"] for i in self.__project_table.get_tab.table]:
                temp_pro_id = input("Please Enter a Valid Project ID: ")
            self.__project_table.show_status(temp_pro_id)
        elif choice == "start evaluation" and self.__role == "advisor":
            filtered__project_table = self.__project_table.get_tab.filter(
                lambda x: x["Advisor"] == self.__id and  x["Status"] == "waiting for evaluation")
            if filtered__project_table.table == []:
                print("No projects available for evaluating.")
            else:
                print("List of Project(s) avaliable to evaluate:")
                for pro in filtered__project_table.table:
                    print(pro)
                to_eval_pro = input("Enter Project ID: ")
                while to_eval_pro not in [i["ProjectID"] for i in filtered__project_table.table]:
                    to_eval_pro = input("Please Enter a Valid Project ID: ")
                self.__evaluate_req.create_r(to_eval_pro, self.__person_table, "", "evaluate",\
                    self.__id)
        elif choice == "view evaluation" and self.__role == "advisor":
            pass
        elif choice == "approve project" and self.__role == "advisor":
            pass
        elif choice == "view tables" and self.__role == "admin":
            temp_table_name = input("Enter Table Name: ")
            while self.__database.search(temp_table_name) == None:
                temp_table_name = input("Please Enter a Valid Table Name: ")
            print(self.__database.search(temp_table_name))
        elif choice == "update tables" and self.__role == "admin":
            temp_table_name = input("Enter Table Name: ")
            while self.__database.search(temp_table_name) == None:
                temp_table_name = input("Please Enter a Valid Table Name: ")
            to_edit_table = self.__database.search(temp_table_name)
            ref_key = input("Enter the Reference Key: ")
            while ref_key not in [n for n in to_edit_table.table[0].keys()]:
                ref_key = input("Please Enter a Valid Reference Key: ")
            ref_value = input("Enter the Reference Value: ")
            while ref_value not in [i[f"{ref_key}"] for i in to_edit_table.table]:
                ref_value = input("Please Enter a Valid Reference Value: ")
            to_edit_key = input("Enter the Key of data you want to edit: ")
            while to_edit_key not in [n for n in to_edit_table.table[0].keys()]:
                to_edit_key = input("Please Enter a Valid Key: ")
            to_edit_value = input("Enter Value: ")
            to_edit_table.update(ref_key, ref_value, to_edit_key, to_edit_value)

        else:
            return input("Invalid Choice. Please Select a Valid Choice: ")
        return "Congrat! You broke my program."

    def inbox(self):
        if self.__role == "student":
            filtered_req = self.__member_req.get_tab.filter(lambda x: x["to_be_member"] ==\
                self.__id and x["Response"] == "").table
            if filtered_req != []:
                print("Request for you to become member:")
                self.__member_req.view_request(self.__id, "member", self.__project_table)
            else:
                print("There're no requests.")
                return
            t_choice = input("Please choose one of the following choice:\n• Respond\n• Menu\n")\
                .lower()
            while t_choice != "menu":
                if t_choice == "respond":
                    temp_pro_id = input("Enter ID of project you want to respond: ")
                    pro_td_check = [i["ProjectID"] for i in filtered_req]
                    while temp_pro_id not in pro_td_check:
                        temp_pro_id = input("Please Enter a Valid ID: ")
                    self.__member_req.respond(temp_pro_id, self.__id, "member",\
                        self.__project_table, self.__login_table, self.__person_table,)
                    break
                else:
                    print("Invalid Choice.")
                    t_choice = input("Please select a valid choice: ")
        elif self.__role == "faculty" or self.__role == "advisor":
            f_choice = input("Please choose the type of request:\n• To be Advisor\n\
• To Evaluate\n• Menu\n").lower()
            while f_choice != "menu":
                if f_choice == "to be advisor":
                    filtered_req = self.__advisor_req.get_tab.filter(lambda x: \
                        x["to_be_advisor"] == self.__id and x["Response"] == "").table
                    if filtered_req != []:
                        print("Request for you to become advisor:")
                        self.__advisor_req.view_request(self.__id, "advisor", self.__project_table)
                        t_choice = input("Please choose one of the following choice:\
                            \n• Respond\n• Menu\n").lower()
                        while t_choice != "menu":
                            if t_choice == "respond":
                                temp_pro_id = input("Enter ID of project you want to respond: ")
                                pro_td_check = [i["ProjectID"] for i in filtered_req]
                                while temp_pro_id not in pro_td_check:
                                    temp_pro_id = input("Please Enter a Valid ID: ")
                                self.__advisor_req.respond(temp_pro_id, self.__id, "advisor",\
                                    self.__project_table, self.__login_table, self.__person_table)
                                break
                            else:
                                print("Invalid Choice.")
                                t_choice = input("Please select a valid choice: ")
                            break
                    else:
                        print("There're no requests.")
                        break
                elif f_choice == "to evaluate":
                    filtered__eva_req = self.__evaluate_req.get_tab.filter\
                        (lambda x: x["to_evaluate"] == self.__id and x["Response"] != "").table
                    if filtered__eva_req == []:
                        print("There're no request.")
                        f_choice = "menu"
                    else:
                        print("Project to Evaluate:")
                        for req in filtered__eva_req.select(["ProjectID"]):
                            print(f"• {req}")
                        eva_pro_id = input("Enter Project ID:")
                        while eva_pro_id not in [i["ProjectID"] for i in filtered__eva_req]:
                            eva_pro_id = input("Please Enter a Valid Project ID:")
                        self.__evaluate_req.eval(eva_pro_id, self.__id, self.__project_table)
                else:
                    print("Invalid Choice.")
                    f_choice = input("Please select a valid choice: ")
