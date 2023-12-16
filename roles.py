import database, os, datetime

class request:
    def __init__(self,table) -> None:
        self.__table = table

    @property
    def table(self):
        return self.__table

    def __str__(self) -> str:
        return str(self.__table)

    def create(self, project_ID, data_table, from_role, to_be):
        people = data_table.filter(lambda x: x['role'] == from_role).select(['ID', 'first', 'last'])
        print("\n List of people available:")
        for info in people:
            print(info)
        recruit_ID_lst = []
        while True:
            recruit_ID = input("ID of the person (blank to submit): ")
            if recruit_ID == "":
                break
            if recruit_ID not in [i["ID"] for i in people]:
                print("Invalid ID, please try again.")
            else:
                recruit_ID_lst.append(recruit_ID)
        for _ID in recruit_ID_lst:
            temp_dict = {}
            temp_dict["ProjectID"] = project_ID
            temp_dict[f"to_be_{to_be}"] = _ID
            temp_dict['Response'] = None
            temp_dict['Response_date'] = None
            self._table.insert(temp_dict)
            
        def view_request(self, person_ID, to_be):
            for _ in self._table.filter(lambda x: x[f"to_be_{to_be}"] == person_ID and x['response'] == None).table:
                print(_)
        
        def view_status(self, project_ID):
            for _ in self._table.filter(lambda x: x[f"ProjectID"] == project_ID).table:
                print(_)