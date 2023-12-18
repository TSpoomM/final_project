# Project Evaluation Proposal

## Objective
The objective of this proposal is to outline a set of actions and corresponding code that are necessary to evaluate a project within the context of the project management system.

## Actions and Code Outline

### 1. Display Project Details
#### Action:
Display project details to the evaluator for a comprehensive understanding.

#### Code:
```python
class User:
    def __init__(self, user_id, username, password):
        self.ID = user_id
        self.username = username
        self.password = password
        
        
class Faculty(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'faculty'
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
```
### 2. Evaluate Project Content
#### Action:
Evaluate the content and progress of the project based on predefined criteria.

#### Code:
```python
class User:
    def __init__(self, user_id, username, password):
        self.ID = user_id
        self.username = username
        self.password = password
        
        
class Faculty(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'faculty'
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
```

### 3. Provide Feedback
#### Action:
Provide constructive feedback to the project team based on the evaluation.

#### Code:
```python
class User:
    def __init__(self, user_id, username, password):
        self.ID = user_id
        self.username = username
        self.password = password
        
        
class Faculty(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        self.role = 'faculty'
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
```

### 4. Approve or Reject Project
#### Action:
Make a decision to approve or reject the project based on the evaluation results.

#### code:
```python
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
```



















