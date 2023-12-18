# import database module
from database import Database, CsvReader, Table
import csv
import sys


class Person:
    def __init__(self):
        self.person_data = []  # ID, First, Last, Type

    def add_person(self, person_id, first_name, last_name, person_type):
        person_entry = {"ID": person_id, "First": first_name, "Last": last_name, "Type": person_type}
        self.person_data.append(person_entry)


class Login:
    def __init__(self):
        self.login_data = []  # ID, Username, Password, Role

    def add_login(self, person_id, username, password, role):
        login_entry = {"ID": person_id, "Username": username, "Password": password, "Role": role}
        self.login_data.append(login_entry)


class AdvisorPendingRequest:
    def __init__(self, project_id, advisor_id, status='Pending', response=None, response_data=None):
        self.project_id = project_id
        self.advisor_id = advisor_id
        self.response = response
        self.status = status
        self.response_data = response_data


class MemberPendingRequest:
    def __init__(self, project_id, to_be_member, response=None, response_data=None):
        self.project_id = project_id
        self.to_be_member = to_be_member
        self.response = response
        self.response_data = response_data

        self.first_name = None
        self.last_name = None
        self.member_id = to_be_member
        self.status = 'Pending'


# project_manage.py

class DatabaseManager:
    def __init__(self):
        # Initialize the database and tables
        self.database = Database('project_database')
        self.initialize_tables()

    def initialize_tables(self):
        # Create tables for admin, lead, member, student, faculty, project, etc.
        # Define table structures (columns) as needed
        self.database.create_table('admin', ['ID', 'username', 'password'])
        self.database.create_table('lead', ['ID', 'username', 'password', 'projects'])
        self.database.create_table('member', ['ID', 'username', 'password', 'project_details'])
        # ... (similarly for other roles and entities)

    def update_all_tables(self, table_name, data):
        # Update data in the specified table
        self.database.update_table(table_name, data)


class User:
    def __init__(self, user_id, username, password):
        self.ID = user_id
        self.username = username
        self.password = password


class Admin(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'admin'

    def manage_database(self, database_manager, table_name, data):
        # Admin can update all tables in the database
        return database_manager.update_all_tables(table_name, data)


class Student(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'student'
        self.invitation_messages = []
        self.project_details = None

    def accept_invitation(self, member_id):
        # Read the existing member_request.csv file
        with open('Member_request.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Find the row corresponding to the member_id
        for row in rows:
            if row['ID'] == member_id and row['status'] == 'Pending':
                # Update the status to 'Accepted'
                row['status'] = 'Accepted'
                print(f"Invitation accepted for member {member_id}.")
                break

        # Write the updated data back to the member_request.csv file
        with open('Member_request.csv', mode='w', newline='') as file:
            fieldnames = ['ID', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def deny_invitation(self, member_id):
        # Read the existing member_request.csv file
        with open('Member_request.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Find the row corresponding to the member_id
        for row in rows:
            if row['ID'] == member_id and row['status'] == 'Pending':
                # Update the status to 'Denied'
                row['status'] = 'Denied'
                print(f"Invitation denied for member {member_id}.")
                break

        # Write the updated data back to the member_request.csv file
        with open('Member_request.csv', mode='w', newline='') as file:
            fieldnames = ['ID', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def modify_project_details(self, project_id, modifying_member, new_details):
        # Read the existing project CSV file
        with open("Project.csv", mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Find the row corresponding to the project_id
        for row in rows:
            if row['ProjectID'] == project_id:
                # Update project details
                row['Details'] = new_details
                row['Status'] = f"Details modified by {modifying_member}"
                print(f"Project details modified for project {project_id} by {modifying_member}.")
                break

        # Write the updated data back to the project.csv file
        with open("Project.csv", mode='w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


class Lead(Student):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'lead'
        self.projects = []

    def create_project(self, ProjectID, Title, Lead, Member1, Member2, Advisor, Status):
        # Logic for creating a new project
        with open("Project.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            project_data = [ProjectID, Title, Lead, Member1, Member2, Advisor, Status]
            writer.writerow(project_data)

    def find_member(self, member_name):
        with open('Project.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                project_id = row['ProjectID']
                title = row['Title']
                lead = row['Lead']
                member1 = row['Member1']
                member2 = row['Member2']
                advisor = row['Advisor']
                status = row['Status']

                # Check if the member is in 'Member1' or 'Member2' columns
                if member_name in [member1, member2]:
                    print(f"Member {member_name} found in project {project_id}: {title}")
                    # You can also print or return other information as needed
                    return project_id, title, lead, member_name, advisor, status

        print(f"Member {member_name} not found in any projects.")
        return None

    def send_invitation_to_member(self, project_id, member_to_invite):
        # Create a MemberPendingRequest instance for the invitation
        invitation_request = MemberPendingRequest(project_id, member_to_invite)

        # Write the invitation request to the member_request.csv file
        with open('Member_request.csv', mode='a', newline='') as file:
            fieldnames = ['project_id', 'to_be_member', 'response', 'response_data', 'first_name', 'last_name',
                          'member_id', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header if the file is newly created
            if file.tell() == 0:
                writer.writeheader()

            # Write the invitation request data
            writer.writerow(vars(invitation_request))

    def add_member_to_project(self, project_id, new_member):
        # Read the existing CSV file
        with open('Project.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = list(csv_reader)

        # Find the project in the CSV file
        for row in rows:
            if row['ProjectID'] == project_id:
                # Update the 'Member1' or 'Member2' column with the new member
                if not row['Member1']:
                    row['Member1'] = new_member
                elif not row['Member2']:
                    row['Member2'] = new_member
                else:
                    # Handle the case where both 'Member1' and 'Member2' are already occupied
                    print(f"Project {project_id} already has two members.")

        # Write the updated data back to the CSV file
        with open('Project.csv', mode='w', newline='') as csv_file:
            fieldnames = csv_reader.fieldnames
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header
            csv_writer.writeheader()

            # Write the updated rows
            csv_writer.writerows(rows)

    def send_request_to_advisors(self, project_id, advisor_name):
        # Create an AdvisorPendingRequest instance for the request
        request_to_advisor = AdvisorPendingRequest(project_id, advisor_name)

        # Write the request to the advisor_request.csv file
        with open('Advisor_request.csv', mode='a', newline='') as file:
            fieldnames = ['project_id', 'advisor_id', 'status', 'response', 'response_data']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header if the file is newly created
            if file.tell() == 0:
                writer.writeheader()

            # Write the request data
            writer.writerow(vars(request_to_advisor))

    def submit_final_report(self, project_id, reporting_member):
        # Read the existing CSV file
        with open('Project.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = list(csv_reader)

        # Find the project in the CSV file
        for row in rows:
            if row['ProjectID'] == project_id:
                # Update the 'Status' column with the final report information
                row['Status'] = f"Final Report Submitted by {reporting_member}"

                print(f"Final report submitted for project {project_id} by {reporting_member}.")

        # Write the updated data back to the CSV file
        with open('Project.csv', mode='w', newline='') as csv_file:
            fieldnames = csv_reader.fieldnames
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header
            csv_writer.writeheader()

            # Write the updated rows
            csv_writer.writerows(rows)


class Member(Student):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'member'

    def modify(self, project_id, modifying_member, new_details):
        self.modify_project_details(project_id, modifying_member, new_details)


class Faculty(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'faculty'

    def see_project_requests(self):
        # Read the advisor_request.csv file
        with open("Advisor_request.csv", mode='r') as file:
            reader = csv.DictReader(file)

            # Display project requests
            print("Project Requests:")
            for row in reader:
                print(f"Project ID: {row['ID']}, Status: {row['status']}")

    def deny_advisor_request(self, project_id, denying_advisor):
        # Read the existing advisor_request.csv file
        with open("Advisor_request.csv", mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Find the row corresponding to the project_id
        for row in rows:
            if row['ID'] == project_id and row['status'] == 'Pending':
                # Update the status to 'Denied'
                row['status'] = 'Denied by Advisor: ' + denying_advisor
                print(f"Advisor request denied for project {project_id} by {denying_advisor}.")
                break

        # Write the updated data back to the advisor_request.csv file
        with open("Advisor_request.csv", mode='w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def see_all_projects(self):
        # Read the Project.csv file
        with open("Project.csv", mode='r') as file:
            reader = csv.DictReader(file)

            # Display project
            print("Project: ")
            for row in reader:
                print(f"Project ID: {row['ProjectID']}, Title: {row['Title']}, Lead: {row['Lead']}, "
                      f"Member1: {row['Member1']}, Member2: {row['Member2']}, Advisor: {row['Advisor']}, "
                      f"Status: {row['status']}")

    def evaluate_project(self, project_id, evaluator, score, feedback):
        # Read the existing Project.csv file
        with open('Project.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Find the row corresponding to the project_id
        for row in rows:
            if row['ProjectID'] == project_id:
                # Update the status, evaluator, score, and feedback
                row['Status'] = f"Evaluated by {evaluator}"
                row['Evaluator'] = evaluator
                row['Score'] = score
                row['Feedback'] = feedback
                print(f"Project {project_id} evaluated by {evaluator}.")
                break

        # Write the updated data back to the Project.csv file
        with open("Project.csv", mode='w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


class AdvisingFaculty(Faculty):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'advising_faculty'

    def approve_project(self, project_id, approver):
        # Read the existing Project.csv file
        with open('Project.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Find the row corresponding to the project_id
        for row in rows:
            if row['ProjectID'] == project_id:
                # Update the status and approver
                row['Status'] = f"Approved by {approver}"
                row['Approver'] = approver
                print(f"Project {project_id} approved by {approver}.")
                break

        # Write the updated data back to the Project.csv file
        with open('Project.csv', mode='w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def see_all_projects_detail(self):
        self.see_all_projects()

    def accept_advisor_request(self, project_id, accepting_advisor):
        # Read the existing advisor_request.csv file
        with open("Advisor_request.csv", mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Find the row corresponding to the project_id
        for row in rows:
            if row['ID'] == project_id and row['status'] == 'Pending':
                # Update the status to 'Accepted by Advisor: [accepting_advisor]'
                row['status'] = f'Accepted by Advisor: {accepting_advisor}'
                print(f"Advisor request accepted for project {project_id} by {accepting_advisor}.")
                break

        # Write the updated data back to the advisor_request.csv file
        with open("Advisor_request.csv", mode='w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def deny_advisor_request(self, project_id, denying_advisor):
        # Read the existing advisor_request.csv file
        with open('Advisor_request.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Find the row corresponding to the project_id
        for row in rows:
            if row['ID'] == project_id and row['status'] == 'Pending':
                # Update the status to 'Denied by Advisor: [denying_advisor]'
                row['status'] = f'Denied by Advisor: {denying_advisor}'
                print(f"Advisor request denied for project {project_id} by {denying_advisor}.")
                break

        # Write the updated data back to the advisor_request.csv file
        with open('Advisor_request.csv', mode='w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


# define a function called initializing

def initializing():
    """
        Create all the corresponding tables for those csv files
        see the guide on how many tables are needed
        add all these tables to the database.
    """

    # database = Database('my_database')  # Instantiate the database

    persons_data = CsvReader(file_paths=['persons.csv']).read_csv()
    login_data = CsvReader(file_paths=['login.csv']).read_csv()

    # Create the 'persons' table
    persons_table = Table(table_name='persons', columns=['ID', 'first', 'last', 'type'])
    for person_entry in persons_data:
        persons_table.insert(person_entry)

    # Create the 'login' table
    login_table = Table(table_name='login', columns=['ID', 'username', 'password', 'role'])

    for login_entry in login_data:
        login_table.insert(login_entry)

    return persons_table, login_table


def login(username, password, login_file='login.csv', max_password_attempts=3):
    # Read the login.csv file
    with open(login_file, mode='r') as file:
        reader = csv.DictReader(file)

        password_attempts = 0

        # Check each row for a matching username and password
        for row in reader:
            if row['username'] == username:
                # Username is correct, check password
                while password_attempts < max_password_attempts:
                    if row['password'] == password:
                        return row['role']
                    else:
                        password_attempts += 1
                        print(f"-----------------------------------------")
                        print(f"Incorrect password. {max_password_attempts - password_attempts} attempts remaining.")
                        print(f"-----------------------------------------")
                        password = input("Enter your password: ")

                # Max password attempts reached
                print("Max password attempts reached. Please try again later.")
                return None

        # Username not found
        print("Incorrect username. Please try again.")
        return None


# define a function called exit
def exit_program():
    """
        Exit the Program.
    """
    sys.exit()


# make calls to the initializing and login functions defined above

persons_table, login_table = initializing()
max_username_attempts = 3
max_password_attempts = 3
real_role = []
user_id = []
username = []
password = []
project_id = []

for _ in range(max_username_attempts):
    username_input = input("Enter your username: ")
    password_input = input("Enter your password: ")

    username.append(username_input)
    password.append(password_input)

    role = login(username_input, password_input, max_password_attempts=max_password_attempts)
    roles = role.lower()

    if roles:
        print(f"Login successful! You are a {roles}.")
        real_role = str(roles)
        break
    else:
        print("Login failed. Please try again.")
        print(f"-----------------------------------------")
else:
    print("Max username attempts reached. Please try again later.")

with open("login.csv", mode='r') as file:
    reader = csv.DictReader(file)
    rowww = list(reader)

    for roww in rowww:
        if username[-1] == roww['username']:
            user_id.append(roww['ID'])

with open("Project.csv", mode='r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

    for row in rows:
        if user_id[-1] == (row['Member1'] or row['Member2']):
            project_id.append(row['ProjectID'])

while True:

    if real_role == 'admin':
        # see and do admin related activities
        print("Admin can manage_database")
        choose = input("Manage or Exit ? [Y/N]: ").upper()
        while choose == 'y':
            admin = Admin(user_id, username[-1], password[-1])
            table_name = input("Table name to update? : ")
            new_data = input("Data to edit? : ")
            manage = admin.manage_database(DatabaseManager, table_name, new_data)
            print("Your database has been updated.")
            choose = input("Manage or Exit ? [Y/N]: ").upper()

        print("Exit the program.")
        exit_program()

    elif real_role == 'student':
        print("Student can Accept, Deny the invitation and Modify your project.")

        choose2 = input("Accept[A] or Deny[D] or Modify[M] or Exit[E]: ").upper()
        student = Student(user_id, username[0], password[0])

        while True:
            if choose2 == 'A':
                accept = student.accept_invitation(user_id)
                choose2 = input("Accept[A] or Deny[D] or Modify[M] or Exit[E]: ").upper()
            elif choose2 == 'D':
                deny = student.deny_invitation(user_id)
                choose2 = input("Accept[A] or Deny[D] or Modify[M] or Exit[E]: ").upper()
            elif choose2 == 'M':
                new_data2 = input('Detail to modify? : ')
                modify = student.modify_project_details(project_id[-1], user_id[-1], new_data2)
                print("Your database has been updated.")
                choose2 = input("Accept[A] or Deny[D] or Modify[M] or Exit[E]: ").upper()
            else:
                print("Exit the program.")
                exit_program()

        # see and do student related activities

    elif real_role == 'member':
        # see and do member related activities
        member = Member(user_id[-1], username[-1], password[-1])
        print("Member can Modify the project details.")
        choose3 = input('Modify[M] or Exit[E]? : ').upper()
        while choose3 == 'M':
            new_data3 = input('Detail to modify? : ')
            modify2 = member.modify(project_id[-1], user_id[-1], new_data3)
            print("Your database has been updated.")
            choose3 = input('Modify[M] or Exit[E]? : ').upper()

        print("Exit the program.")
        exit_program()

    elif real_role == 'lead':
        # see and do lead related activities
        lead = Lead(user_id[-1], username[-1], password[-1])
        print('lead can Create Project, Find member, Send invite to member, '
              'Send request to advisor, Add member, Submit project')
        choose4 = input('Create Project[C], Find member[F], Send invite to member[I], '
                        'Send request to advisor[R], Add member[A], Submit project[S]? : ').upper()
        while True:
            if choose4 == 'C':
                # ProjectID, Title, Lead, Member1, Member2, Advisor, Status
                print("Create Project : ")
                projectID = input("ProjectID : ")
                title = input("Title : ")
                lead2 = input("Lead : ")
                member1 = input("Member1 : ")
                member2 = input("Member2 : ")
                advisor = input("Advisor : ")
                status = input("Status : ")
                create = lead.create_project(projectID, title, lead2, member1, member2, advisor, status)
                choose4 = input('Create Project[C], Find member[F], Send invite to member[I], '
                                'Send request to advisor[R], Add member[A], Submit project[S]? : ').upper()
            elif choose4 == 'F':
                member_name = input("Enter the name : ")
                find = lead.find_member(member_name)
                choose4 = input('Create Project[C], Find member[F], Send invite to member[I], '
                                'Send request to advisor[R], Add member[A], Submit project[S]? : ').upper()
            elif choose4 == 'I':
                print("Send invite to member : ")
                mem = input("Enter member name : ")
                invite = lead.send_invitation_to_member(project_id[-1], mem)
                print("Member has been invited.")
                choose4 = input('Create Project[C], Find member[F], Send invite to member[I], '
                                'Send request to advisor[R], Add member[A], Submit project[S]? : ').upper()

    elif real_role == 'faculty':
        # see and do faculty related activities
        pass
    elif real_role == 'advisor':
        # see and do advisor related activities
        pass

# pr = Project()
# show = pr.load_projects_from_csv()
# once everything is done, make a call to the exit function
exit_program()
