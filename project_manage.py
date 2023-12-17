import database, csv, os

# define a funcion called initializing

def initializing():
    global DB
    DB = database.DB()
    for files in os.listdir(os.getcwd()):
        if files.endswith('.csv'):
            file_name = os.path.splitext(files)[0]
            print(file_name)
            content = database.CSV_reader(file_name).get_lst
            temp_table = database.Table(file_name, content)
            DB.insert(temp_table)
    
    # test code
    # print(DB.search('login'))

# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed

    # add all these tables to the database


# define a funcion called login

def login():
    username = input('Enter username: ')
    password = input('Enter password: ')
    output = DB.search('login').filter(lambda x: x['username'] == username 
            and x['password'] == password).select(['ID', 'role'])
    if output != []:
        return [output[0]["ID"], output[0]["role"]]
    else:
        return None
# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None

# define a function called exit
def exit():
    for _ in DB.database:
        if _.table != []:
            filename = _.table_name + ".csv"
            myFile = open(filename, "w", newline="")
            writer = csv.writer(myFile)
            writer.writerow(Head for Head in _.table[0])
            for dictionary in _.table:
                writer.writerow(dictionary.values())
            myFile.close()
            with open(filename) as myFile:
                lines = myFile.readlines()
                last_line = lines[len(lines)-1]
                lines[len(lines)-1] = last_line.rstrip()
            with open(filename, 'w') as myFile:    
                myFile.writelines(lines)

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

initializing()
val = login()

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # see and do admin related activities
# elif val[1] = 'student':
    # see and do student related activities
# elif val[1] = 'member':
    # see and do member related activities
# elif val[1] = 'lead':
    # see and do lead related activities
# elif val[1] = 'faculty':
    # see and do faculty related activities
# elif val[1] = 'advisor':
    # see and do advisor related activities

# once everyhthing is done, make a call to the exit function
exit()
