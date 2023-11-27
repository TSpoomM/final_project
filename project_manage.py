# import the database module
from database import Database, persons_table
import csv
import sys


class ProjectEvaluation:
    def __init__(self):
        self.evaluations = []

    def add_evaluation(self, project_id, eva_id, comments, rate):
        eva = {
            "project_id": project_id,
            "evaluator_id": eva_id,
            "comments": comments,
            "rating": rate
        }
        self.evaluations.append(eva)

    def get_evaluations_for_project(self, project_id):
        return [data for data in self.evaluations if data["project_id"] == project_id]


class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        data = []
        with open(self.file_path) as f:
            rows = csv.DictReader(f)
            for r in rows:
                data.append(dict(r))
        return data


class CSVTable:
    def __init__(self, file_path):
        self.file_path = file_path
        self.entries = []
        self.load_entries()
        self.evaluations = ProjectEvaluation()

    def load_entries(self):
        csv_reader = CSVReader(self.file_path)
        self.entries = csv_reader.read_csv()

    def insert_entry(self, entry):
        self.entries.append(entry)

    def update_entry(self, key, old_value, new_value):
        for i in self.entries:
            if i.get(key) == old_value:
                i[key] = new_value

    def save_to_csv(self):
        with open(self.file_path, mode='w', newline='') as f:
            fieldnames = self.entries[0].keys() if self.entries else []
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(self.entries)

    def evaluate(self, project_id, eva_id, comments, rate):
        self.evaluations.add_evaluation(project_id, eva_id, comments, rate)

    def get_project_eva(self, project_id):
        return self.evaluations.get_evaluations_for_project(project_id)


class CSVDatabase:
    def __init__(self, database_name):
        self.database_name = database_name
        self.tables = {}

    def create_table(self, table_name, file_path):
        table = CSVTable(file_path)
        self.tables[table_name] = table


# define a function called initializing
def initializing():
    # create an object to read all csv files that will serve as a persistent state for this program
    my_database = Database('my_database')

    """
    create all the corresponding tables for those csv files
    see the guide on how many tables are needed
    add all these tables to the database
    """

    # Read the 'persons.csv' file and add a 'persons' table to the database
    csv_file_path_persons = 'persons.csv'
    table_name_persons = 'persons'
    with open(csv_file_path_persons) as f_persons:
        rows_persons = csv.DictReader(f_persons)
        columns_persons = rows_persons.fieldnames

        # Add the 'persons' table to the database
        my_database.add_table(table_name_persons, columns_persons)

        # Get the 'persons' table from the database
        persons_table = my_database.tables[table_name_persons]

        # Insert data into the 'persons' table
        for row_persons in rows_persons:
            entry_persons = [row_persons[column] for column in columns_persons]
            persons_table.insert(entry_persons)

    # Read the 'login.csv' file and add a 'login' table to the database
    csv_file_path_login = 'login.csv'
    table_name_login = 'login'
    with open(csv_file_path_login) as f_login:
        rows_login = csv.DictReader(f_login)
        columns_login = rows_login.fieldnames

        # Add the 'login' table to the database
        my_database.add_table(table_name_login, columns_login)

        # Get the 'login' table from the database
        login_table = my_database.tables[table_name_login]

        # Insert data into the 'login' table
        for row_login in rows_login:
            entry_login = [row_login[column] for column in columns_login]
            login_table.insert(entry_login)

    return my_database


# define a function called login
def login(database):
    """
    add code that performs a login task
    ask a user for a username and password
    returns [ID, role] if valid
    """

    # Check the username
    global name, password

    username_flag = True
    password_flag = True
    count = 1

    while username_flag:

        name = input("Enter your username: ")

        for entry in database.tables['login'].data:

            if entry['username'] == name:
                username_flag = False
                break

        if username_flag:
            print(f"--------------------------------------")
            print("Incorrect name.")
            print(f"--------------------------------------")

    while password_flag:

        password = input("Enter your password: ")

        if count >= 3:
            print("BYE BYE")
            exit()

        for entry in database.tables['login'].data:
            if password == entry['password']:
                password = False
                return [entry['ID'], entry['role']]

        count += 1
        print(f"--------------------------------------")
        print(f"Invalid password \nPlease try again {4 - count}")
        print(f"--------------------------------------")


# define a function called exit
def exit_program():
    """
    write out all the tables that have been modified to the corresponding csv files
    By now, you know how to read in a csv file and transform it into a list of dictionaries.
    For this project, you also need to know how to do the reverse, i.e.,
    writing out to a csv file given a list of dictionaries.
    See the link below for a tutorial on how to do this:
    https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python
    """

    sys.exit()


# make calls to the initializing and login functions defined above
my_db = initializing()
val = login(my_db)

""" 
based on the return value for login, activate the code 
that performs activities according to the role defined for that person_id 
"""
if val and val[1] == 'admin':
    # see and do admin related activities
    print("Admin activities")
    persons_table.show_data()
    print("Admin can update all the tables there")

elif val and val[1] == 'student':
    # see and do student related activities
    print("student activities")
    print("1. See an invitational message from the lead \n"
          "2. Accept or deny the invitation \n"
          "3. See and modify his project details")

elif val and val[1] == 'member':
    # see and do member related activities
    print("member activities")
    print("See and modify his project details")

elif val and val[1] == 'lead':
    # see and do lead related activities
    print("lead activities")
    print("Create a project \n"
          "Find members \n"
          "Send invitational messages to potential members \n"
          "Add members to the project and form a group \n"
          "See and modify his own project details \n"
          "Send request messages to potential advisors \n"
          "Submit the final project report \n")

elif val and val[1] == 'faculty':
    # see and do faculty related activities
    print("faculty activities")
    print("See request to be a supervisor \n"
          "Send response denying to serve as an advisor \n"
          "See details of all the project \n"
          "Evaluate projects (this is the missing step that you will explain in"
          " your proposal; see details in the tasks below)")

elif val and val[1] == 'advisor':
    # see and do advisor related activities
    print("advisor activities")
    print("See request to be a supervisor \n"
          "Send accept response (for projects eventually serving as an advisor) \n"
          "Send deny response (for projects not eventually serving as an advisor) \n"
          "See details of all the project \n"
          "Evaluate projects (this is the missing step that you will explain in your "
          "proposal; see details in the tasks below)Approve the project")
else:
    print("Invalid role. Please check your user data.")

# once everything is done, make a call to the exit function
exit_program()
