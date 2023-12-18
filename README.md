# Final project for 2023's 219114/115 Programming I
## File list
  - database.py
  - project_manage.py
  - roles.py
  - advisor_pending_request.csv
  - evaluate_request.csv
  - login.csv
  - member_pending_request.csv
  - persons.csv
  - project.csv

# Classes in roles.py
## Class Request
This class contains all function related to requests.
The class recieve a request table and store it as its attribute
### Function
  - get_tab: basic getter for the table attribute
  - create r: add request to the table based on the arguments taken
  - view_request: view request that contain the ID recieved
  - view_status: view status of request releated to the project with the projectID recieved
  - respond: reply to a request
  - eval: use specificly for eval request(not done)

## Class Project
This class contains all function related to projects.
The class recieve a request table and store it as its attribute
### Function
  - get_tab: basic getter for the table attribute
  - create_p : add project to table based on the arguments given
  - get_id: return the project_id of a project with lead_id recieved
  - check_m_and_a: check whether there're free slot for member or supervisor
  - p_update: update value in the project
  - show_status: print the status of the project

## Class User
This class contain the menu and run function based on the role
This class recieve id, role, and database to generate its attribute.
### Function
  - update_role: update self.__row
  - menu: show the menu use navigate() to run function
  - navigate: run functions based on self.__row and input recieced
  - inbow: show request sent to user
  - 
# How to run?
  - run the **project_manage.py** file.

# Roles
This program does not seperate each role into its own class
|Role|Action|Method|Class|Completion percentage|
|----|------|------|----|-----|
|Admin|View table in the database|menu|User|100%|
|Admin|Update table in the database|update tables|menu|User|100%|
|Student|View requests|Inbox|
|__str__|print table|None|

# Bugs
If user input break line when the program read input, the program will loop to eternity.