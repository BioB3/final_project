# Final project for 2023's 219114/115 Programming I
## File list
  - .gitignore
  - database.py
  - project_manage.py
  - roles.py
  - advisor_pending_request.csv
  - evaluate_request.csv
  - login.csv
  - member_pending_request.csv
  - persons.csv
  - project.csv
  - Proposal.md
  - TODO.md
  - README.md

# Classes in database.py
## Class CSV_reader
This class find the csv file with the given name in current working directory,
and read it as dictionarys then store them as a list.
This class's needed argument is file name.
### Function
  - get_lst: return the list stored

## Class DB
This class acts like a database by being a list that store Table objects
This class need no argument
### Fuctiom
  - insert: add a Table to the list
  - search: find a Table in the the list with the name taken

## Class Table
This class acts like a table to store data by being a list of dictionarys with name.
This class's needed argument are table name and the list of dictionarys and the table name.
### Function
  - table_name: return the table name
  - table: return the list of dictionarys
  - join: connect with the Table taken using the common key taken to return a new Table
  - filter: return a filtered Table with the conditions taken
  - _if_float: check whether the argument taken can be convert into float
  - aggregate: use the function taken on the values of the key taken, then return the result
  - select: return a new Table that retained the keys taken
  - __str__: print the list of dictionarys in the formatted form
  - insert: add the taken dictionary to the list
  - update: edit the value associated with the key taken in the chosen dictionary by recieving the reference key and value

# Classes in roles.py
## Class Request
This class contains most function related to request tables.
The class's needed argument is a Table(request Table)
### Function
  - get_tab: return the Table stored
  - create r: add request to the Table based on the arguments taken
  - view_request: view request in the Table that contain the ID recieved
  - view_status: view status of request releated to the project with the projectID recieved in the Table
  - respond: reply to a request in the Table and make changes to other table based on the arguments taken
  - eval: reply to a evaluation request in the Table(Not Done)

## Class Project
This class contains most function related to project tables.
The class's needed argument is a Table(project Table)
### Function
  - get_tab: return the Table stored
  - create_p : add project to Table based on the arguments given and edit role and type in person and login table
  - get_id: return the project_id of a project in the Table with lead_id taken
  - check_m_and_a: check whether there're free slot for member or supervisor in a project with id taken
  - p_update: update value associated with the key taken in the selected project
  - show_status: print the status of the project with the id taken

## Class User
This class contain the main menu.
This class recieve input and call function based on the input recieved and role of the user.
This class's needed arguments are id, role, and DB
### Function
  - update_role: update the role stored to match with login and person table
  - menu: show the main menu which will recieve inputs and run navigate(input)
  - navigate: run functions based on the user's role and input recived
  - inbow: show the request that contain the user's ID(the output varies based on user's role)

# How to run?
  - download the files needed
  - run the project_manage.py file.
  - enter the value that the program asked for
*The input in menu have to be the same as the choices but is not case-sensitive*

# Actions
|Role|Action|Input recieved|Releated Method(Class)|Completion percentage|
|----|------|------|----|-----|
|Admin|View table in the database|view tables|search(Class DB)|100%|
|Admin|Update table in the database|update tables|search(Class DB), table(Table), update(Table)|100%|
|Student|View requests to be member|inbox|inbox(User)|100%|
|Student|respond to requests to be member|inbox -> respond|inbox(User)|100%|
|Student|Create project and become lead|create a project|create_p(Project)|100%|
|Member|View Project Status|project status|show_status(Project)|100%|
|Member|Edit Project Detail|edit project|p_update(Project)|100%|
|Lead|View Project Status|project status|show_status(Project)|100%|
|Lead|Edit Project Title and Detail|edit project|p_update(Project)|100%|
|Lead|request members|invite members|check_m_and_a(Project), create_r(Request)|100%|
|Lead|request supervisor|invite supervisor|check_m_and_a(Project), create_r(Request)|100%|
|Lead|View requests sent|view invitations|get_id(Project), view_status(Request)|100%|
|Lead|Submit final report to get project evaluated|submit project|check_m_and_a(Project), get_id(Project), p_update(Project)|100%|
|Faculty, Advisor|View Requests to be advisor|inbox -> to be advisor|inbox(User)|100%|
|Faculty, Advisor|View Requests to evaluate project|inbox -> to evaluate|inbox(User)|50%|
|Faculty, Advisor|respond to reqests to be advisor|inbox -> to be advisor -> respond|inbox(User)|100%|
|Faculty, Advisor|respond to evaluation request|inbox -> to evaluate -> respond|inbox(User)|50%|
|Faculty, Advisor|View a project's status|view projects|get_tab(Project), table(Table), show_status(Project)|100%|
|Advisor|Start Evaluating project|start evaluation|filter(Table), table(Table), create_r(Project)|40%|
|Advisor|View Status of evaluation requests sent|view evaluation|Not implemented|0%|
|Advisor|Approve projects|approve project|Not implemented|0%|


# Missing features and outstanding bugs
  - If user input break line when the program read input, the program will loop to eternity.
  - Creating project doesn't automatically rejects request to be member
  - All function that is not finished or not done will lead to either error or eternal loop.
  - *View request to evaluate project* does not correctly print the requests
  - *View requests to evaluate project* suppose to lead to responding the request by selecting one of the request then update the evaluate_request with the inputted response and comment
  - *View Status of evaluation requests sent* is planned to show all of the requests to be evaluater that the advisor(user) sent
  - *Approve projects* is planned to show all projects the advisor(user) is supervising that have the status "waiting for approval" then the advisor(user) choose one of them to approve which will set the project status to "finished"
