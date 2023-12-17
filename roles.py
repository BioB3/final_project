import database, os, datetime

class request:
    def __init__(self, table) -> None:
        self.__table = table

    @property
    def get_tab(self):
        return self.__table

    def create_r(self, project_ID, person_table, from_role, to_be):
        if from_role == "faculty":
            people = person_table.filter(lambda x: x["type"] == from_role or x["type"] == "advisor")
        elif from_role == "student":
            people = person_table.filter(lambda x: x["type"] == from_role)
        people_lst = people.select(["ID", "fist", "last"])
        print("\n List of people available:")
        for info in people_lst:
            print(info)
        recruit_ID_lst = []
        while True:
            recruit_ID = input("ID of the person (leave blank to submit): ")
            if recruit_ID == "":
                break
            if recruit_ID not in [i["ID"] for i in people_lst]:
                print("Invalid ID, please try again.")
            else:
                recruit_ID_lst.append(recruit_ID)
        print()
        for _ID in recruit_ID_lst:
            temp_dict = {}
            temp_dict["ProjectID"] = project_ID
            temp_dict[f"to_be_{to_be}"] = _ID
            temp_dict['Response'] = ""
            temp_dict['Response_date'] = ""
            self.__table.insert(temp_dict)
            f_name = person_table.filter(lambda x: x["ID"] == _ID).table[0]
            print(f"Sent request to {f_name['fist']} {f_name['last']}")
            
    def view_request(self, person_ID, to_be, project_table):
        count = 0
        temp_tap = self.__table.filter(lambda x: x[f"to_be_{to_be}"] == person_ID and x["Response"] == "")
        for _ in temp_tap.select(["ProjectID"]):
            count += 1
            print(f"{count})")
            for n, m in _.items():
                print(f"|   {n} : {m}")
                temp_detail = project_table.get_tab.filter(lambda x: x["ProjectID"] == m).select(["Title", "Detail"])[0]
                print(f"|   Title : {temp_detail['Title']}")
                print(f"|   Detail : {temp_detail['Detail']}")
                
        
    def view_status(self, project_ID):
        for _ in self.__table.filter(lambda x: x["ProjectID"] == project_ID).table:
            print(_)
    
    def respond(self, project_ID, person_ID, to_be, login_table = None,\
        person_table = None, proj = None):
        if login_table == None:
            response = "n"
        else:
            response = input("Enter your response (y/n) :")
        for _req in self.__table.table:
            if _req["ProjectID"] == project_ID and _req[f"to_be_{to_be}"] == person_ID:
                _req["Response_date"] = datetime.datetime.now().strftime("%d-%m-%Y")
                if response.lower() == "y":
                    _req["Response"] = "Accepted"
                    login_table.update("ID", person_ID, "role", to_be)
                    person_table.update("ID", person_ID, "type", to_be)
                    proj.update(project_ID, to_be.capitalize(), person_ID)
                    for _other_req in self.__table.table:
                        if to_be.lower() == "member" and _other_req["ProjectID"] != project_ID\
                            and _other_req[f"to_be_{to_be}"] == person_ID:
                            self.respond(_other_req["ProjectID"], person_ID, to_be)
                        if to_be.lower() == "member" and not proj.check_member(project_ID)\
                            and _other_req["Response"] == "":
                            self.respond(project_ID, _other_req[f"to_be_{to_be}"], to_be)
                        if to_be.lower() == "advisor":
                            proj.update(project_ID, "Status", "in progress")
                            if _other_req["ProjectID"] == project_ID\
                                and _other_req[f"to_be_{to_be}"] != person_ID:
                                self.respond(project_ID, _other_req[f"to_be_{to_be}"], to_be)
                elif response.lower() == "n":
                    if to_be.lower() == "member" or to_be.lower() == "advisor":
                        _req["Response"] = "Rejected"

class project:
    def __init__(self, table) -> None:
        self.__table = table
    
    @property
    def get_tab(self):
        return self.__table
    
    def create_p(self, lead_ID, login_table, person_table):
        temp_dict = {}
        temp_dict["ProjectID"] = str(len(self.__table.table) + 1)
        title = input("Enter Project's Title: ")
        temp_dict["Title"] = title
        temp_dict["Lead"] = lead_ID
        temp_dict["Member1"] = ""
        temp_dict["Member2"] = ""
        temp_dict["Advisor"] = ""
        temp_dict["Status"] = "finding supervisor"
        temp_dict["Detail"] = ""
        login_table.update("ID", lead_ID, "role", "lead")
        person_table.update("ID", lead_ID, "type", "lead")
        self.__table.insert(temp_dict)
        
    def get_id(self, _ID):
        return self.__table.filter(lambda x: x["Lead"] == _ID or x["Member1"] == _ID or\
            x["Member2"] == _ID).table[0]["ProjectID"]
        
    def check_member(self, project_ID):
        cw_dict = self.__table.filter(lambda x: x["ProjectID"] == project_ID).table[0]
        if cw_dict["Member1"] != "" and cw_dict["Member2"] != "":
            return False
        else:
            return True
    
    def update(self, project_ID, key, value):
        cw_dict = self.__table.filter(lambda x: x["ProjectID"] == project_ID).table[0]
        if key.lower() == "member" and cw_dict["Member1"] == "":
            key = "Member1"
        elif key.lower() == "member" and cw_dict["Member1"] != "":
            key = "Member2"
        self.__table.update("ProjectID", project_ID, key, value)
    
    def show_status(self, project_ID):
        temp_pj = self.__table.filter(lambda x: x["ProjectID"] == project_ID).table[0]
        for _ in temp_pj:
            print(f"{_} : {temp_pj[_]}")

class User:
    def __init__(self, ID, role, database) -> None:
        self.__ID = ID
        self.__role = role
        self.__database = database
        self.__project_table = project(self.__database.search("project"))
        self.__member_req = request(self.__database.search("member_pending_request"))
        self.__advisor_req = request(self.__database.search("advisor_pending_request"))
        self.__login_table = self.__database.search("login")
        self.__person_table = self.__database.search("persons")
    
    def update_role(self):
        self.__role = self.__login_table.filter(lambda x: x["ID"] == self.__ID).table[0]["role"]
    
    def menu(self):
        print(f"Welcome! {self.__person_table.filter(lambda x: x['ID'] == self.__ID).table[0]['fist']}" +
              f" {self.__person_table.filter(lambda x: x['ID'] == self.__ID).table[0]['last']}")
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
            print("• Inbox\nView Projects")
            if self.__role == "advisor":
                print("• View Evaluation\n• Approve Project")
        elif self.__role == "admin":
            print("• View Tables\n• Update Tables")
        print("• Exit")
        m_choice = input().lower()
        while m_choice != "exit":
            if m_choice == "Congrat! You broke my program.":
                break
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
            self.__project_table.create_p(self.__ID, self.__login_table, self.__person_table)
        elif choice == "project status" and self.__role in ["member", "lead"]:
            self.__project_table.show_status(self.__project_table.get_id(self.__ID))
        elif choice == "edit project" and self.__role in ["member", "lead"]:
            if self.__role == "member":
                changes = input("Enter Detail (leave blank to cancel) : ")
                if changes != "":
                    self.__project_table.update(self.__project_table.get_id(self.__ID),"Detail", changes)
            elif self.__role == "lead":
                t_or_d = ""
                while t_or_d not in ["title", "detail"]:
                    t_or_d = input("Edit Title or Detail: ").lower()
                changes = input(f"Enter {t_or_d.capitalize()} (leave blank to cancel): ")
                if changes != "":
                    if t_or_d == "title":
                        self.__project_table.update(self.__project_table.get_id(self.__ID),"Title", changes)
                    elif t_or_d == "detail":
                        self.__project_table.update(self.__project_table.get_id(self.__ID),"Detail", changes)
        elif choice == "invite members" and self.__role == "lead":
            if self.__project_table.check_member(self.__project_table.get_id(self.__ID)):
                self.__member_req.create_r(self.__project_table.get_id(self.__ID),\
                    self.__person_table, "student", "member")
        elif choice == "invite supervisor" and self.__role == "lead":
            pass
        elif choice == "view invitations" and self.__role == "lead":
            pass
        elif choice == "submit project" and self.__role == "lead":
            pass
        elif choice == "view projects" and self.__role in ["faculty", "advisor"]:
            pass
        elif choice == "view evaluation" and self.__role == "advisor":
            pass
        elif choice == "approve project" and self.__role == "advisor":
            pass
        elif choice == "view tables" and self.__role == "admin":
            temp_table_name = input("Enter Table Name: ")
            print(self.__database.search(temp_table_name))
        elif choice == "update tables" and self.__role == "admin":
            pass
        else:
            return input("Invalid Choice. Please Select a Valid Choice: ")
        return "Congrat! You broke my program."

    def inbox(self):
        if self.__role == "student":
            if self.__member_req.get_tab.filter(lambda x: x["to_be_member"] == self.__ID).table != []:
                print("Request for you to become member:")
                self.__member_req.view_request(self.__ID, "member", self.__project_table)
            else:
                print("There're no requests.")
                return
            t_choice = input("Please choose one of the following choice:\n• Respond\n• Menu\n").lower()
            while t_choice != "menu":
                if t_choice == "respond":
                    temp_Pro_ID = input("Enter ID of project you want to respond: ")
                    self.__member_req.respond(temp_Pro_ID, self.__ID, "member", self.__login_table,\
                        self.__person_table, self.__project_table)
                    break
                else:
                    print("Invalid Choice.")
                    t_choice = input("Please select a valid choice: ")
        elif self.__role == "faculty" or self.__role == "advisor":
            f_choice = input("Please choose the type of request:\n• To be Advisor\n• To Evaluate\n• Menu\n").lower()
            while f_choice != "menu":
                if f_choice == "to be advisor":
                    if self.__advisor_req.get_tab.filter(lambda x: x["to_be_advisor"] == self.__ID).table != []:
                        print("Request for you to become advisor:")
                        self.__advisor_req.view_request(self.__ID, "advisor", self.__project_table)
                        t_choice = input("Please choose one of the following choice:\n• Respond\n• Menu").lower()
                        while t_choice != "menu":
                            if t_choice == "respond":
                                temp_Pro_ID = input("Enter ID of project you want to respond: ")
                                self.__advisor_req.respond(temp_Pro_ID, self.__ID, "advisor", self.__login_table,\
                                    self.__person_table, self.__person_table)
                                break
                            else:
                                print("Invalid Choice.")
                                t_choice = input("Please select a valid choice: ")
                            break
                    else:
                        print("There're no requests.")
                        break
                elif f_choice == "to evaluate":
                    break
                else:
                    print("Invalid Choice.")
                    t_choice = input("Please select a valid choice: ")
