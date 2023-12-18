# Project TODO List

## Admin
- [ ] Create tables for admin, lead, member, student, faculty, project, etc.
- [ ] Define table structures (columns) as needed.
- [ ] Implement a method to manage the database (Admin class).
- [ ] Allow the admin to update all tables in the database.

## Student
- [ ] See an invitational message from the lead.
- [ ] Accept or deny the invitation.
- [ ] See and modify his project details.
- [ ] Implement `accept_invitation` method in the Student class.
- [ ] Implement `deny_invitation` method in the Student class.
- [ ] Implement `modify_project_details` method in the Student class.

## Lead Student
- [ ] Create a project.
- [ ] Find members.
- [ ] Send invitational messages to potential members.
- [ ] Add members to the project and form a group.
- [ ] See and modify his own project details.
- [ ] Send request messages to potential advisors.
- [ ] Submit the final project report.
- [ ] Implement `create_project` method in the Lead class.
- [ ] Implement `find_member` method in the Lead class.
- [ ] Implement `send_invitation_to_member` method in the Lead class.
- [ ] Implement `add_member_to_project` method in the Lead class.
- [ ] Implement `send_request_to_advisors` method in the Lead class.
- [ ] Implement `submit_final_report` method in the Lead class.

## Member Student
- [ ] See and modify his project details.
- [ ] Implement `modify` method in the Member class.

## Normal Faculty (Not an Advisor)
- [ ] See requests to be a supervisor.
- [ ] Send a response denying serving as an advisor.
- [ ] See details of all projects.
- [ ] Evaluate projects.
- [ ] Implement `see_project_requests` method in the Faculty class.
- [ ] Implement `deny_advisor_request` method in the Faculty class.
- [ ] Implement `see_all_projects` method in the Faculty class.
- [ ] Implement `evaluate_project` method in the Faculty class.

## Advising Faculty
- [ ] See requests to be a supervisor.
- [ ] Send accept response (for projects eventually serving as an advisor).
- [ ] Send deny response (for projects not eventually serving as an advisor).
- [ ] See details of all projects.
- [ ] Evaluate projects.
- [ ] Approve the project.
- [ ] Implement `see_project_requests` method in the AdvisingFaculty class.
- [ ] Implement `approve_project` method in the AdvisingFaculty class.
- [ ] Implement `evaluate_project` method in the AdvisingFaculty class.
- [ ] Implement `accept_advisor_request` method in the AdvisingFaculty class.
- [ ] Implement `deny_advisor_request` method in the AdvisingFaculty class.

## TODOs for General Functionality
- [ ] Implement a function to initialize tables (`initializing` function).
- [ ] Implement a function to handle login (`login` function).
- [ ] Implement a function to exit the program (`exit_program` function).
