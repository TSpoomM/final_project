import csv
import os


class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.tables = {}

    def add_table(self, table_name, columns):
        self.tables[table_name] = Table(table_name, columns)


class Table:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns
        self.data = []

    def insert(self, entry):
        # Check if the entry has the correct number of columns
        if len(entry) != len(self.columns):
            raise ValueError("Number of columns in the entry does not match the table's schema.")

        # Create a dictionary with column names as keys
        entry_dict = dict(zip(self.columns, entry))

        # Add the entry to the data list
        self.data.append(entry_dict)

    def show_data(self):
        print(f"Data in {self.table_name} table:")
        for entry in self.data:
            print(entry)


# Create a Database instance
my_database = Database('my_database')

# Read the CSV file and add a 'persons' table to the database
csv_file_path = 'persons.csv'
table_name = 'persons'

with open(csv_file_path) as f:
    rows = csv.DictReader(f)
    columns = rows.fieldnames

    # Add the 'persons' table to the database
    my_database.add_table(table_name, columns)

    # Get the 'persons' table from the database
    persons_table = my_database.tables[table_name]

    # Insert data into the 'persons' table
    for row in rows:
        entry = [row[column] for column in columns]
        persons_table.insert(entry)

# Show data in the 'persons' table
# persons_table.show_data()
# print()
