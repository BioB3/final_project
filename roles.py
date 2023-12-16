import database, os, datetime

class request:
    def __init__(self, table) -> None:
        self.__table = table

    @property
    def get_tab(self):
        return self.__table

    def __str__(self) -> str:
        return str(self.__table)

    def create_r(self, project_ID, person_table, from_role, to_be):
        people = person_table.filter(lambda x: x["type"] == from_role).select(["ID", "fist", "last"])
        print("\n List of people available:")
        for info in people:
            print(info)
        recruit_ID_lst = []
        while True:
            recruit_ID = input("ID of the person (leave blank to submit): ")
            if recruit_ID == "":
                break
            if recruit_ID not in [i["ID"] for i in people]:
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
            f_name = person.filter(lambda x: x["ID"] == _ID).table[0]
            print(f"Sent request to {f_name['fist']} {f_name['last']}")
            
    def view_request(self, person_ID, to_be):
        count = 0
        temp_tap = self.__table.filter(lambda x: x[f"to_be_{to_be}"] == person_ID and x["Response"] == "")
        for _ in temp_tap.select(["ProjectID", f'to_be_{to_be}']):
            count += 1
            print(f"{count})")
            for n, m in _.items():
                print(f"|   {n} : {m}")
        
    def view_status(self, project_ID):
        for _ in self.__table.filter(lambda x: x["ProjectID"] == project_ID).table:
            print(_)
    
    def respond(self, project_ID, person_ID, to_be, login_table = None, person_table = None, proj = None):
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
                    if to_be.lower() == "member":
                        for _other_req in self.__table.table:
                            if _other_req["ProjectID"] != project_ID and _other_req[f"to_be_{to_be}"] == person_ID:
                                self.respond(project_ID, person_ID, to_be)
                elif response.lower() == "n":
                    _req["Response"] = "Rejected"

class project:
    def __init__(self, table) -> None:
        self.__table = table
    
    @property
    def get_tab(self):
        return self.__table
    
    def __str__(self) -> str:
        return str(self.__table)
    
    def create_p(self, title, lead_ID, login_table, person_table):
        temp_dict = {}
        temp_dict["ProjectID"] = str(len(self.__table.table) + 1)
        temp_dict["Title"] = title
        temp_dict["Lead"] = lead_ID
        temp_dict["Member1"] = ""
        temp_dict["Member2"] = ""
        temp_dict["Advisor"] = ""
        temp_dict["status"] = "finding supervisor"
        temp_dict["Detail"] = ""
        login_table.update("ID", lead_ID, "role", "lead")
        person_table.update("ID", lead_ID, "type", "lead")
        self.__table.insert(temp_dict)
        
    def get_id(self, lead_ID):
        return self.__table.filter(lambda x: x["Lead"] == lead_ID).table[0]["ProjectID"]
    
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

if __name__ == "__main__":
    my_DB = database.DB()
    for files in os.listdir(os.getcwd()):
        if files.endswith('.csv'):
            file_name = os.path.splitext(files)[0]
            content = database.CSV_reader(file_name).get_lst
            temp_table = database.Table(file_name, content)
            my_DB.insert(temp_table)
    login = my_DB.search("login")
    person = my_DB.search("persons")
    _project = my_DB.search("project")
    member_pending_request = my_DB.search("member_pending_request")
    advisor_pending_request = my_DB.search("advisor_pending_request")
    a_p = project(_project)
    a_p.create_p("abc", 1228464, login, person)
    a_p.update(a_p.get_id(1228464), "Detail", "fqfdqcdqw")
    a_p.show_status(a_p.get_id(1228464))
    a_r = request(member_pending_request)
    a_r.create_r(a_p.get_id(1228464), person, "student", "member")
    a_r.view_request("5086282", "member")
    a_r.view_status(a_p.get_id(1228464))
    a_r.respond("1", "5086282", "member", login, person, a_p)
    a_r.view_request("5086282", "member")
    a_r.view_status(a_p.get_id(1228464))
    print(login)
    print(person)
    a_p.show_status(a_p.get_id(1228464))