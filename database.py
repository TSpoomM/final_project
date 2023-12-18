import csv


class CsvReader:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def read_csv(self):
        data = []
        for file in self.file_paths:
            try:
                with open(file) as csv_file:
                    rows = csv.DictReader(csv_file)
                    for row in rows:
                        data.append(dict(row))
            except FileNotFoundError:
                return None
        return data


class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.tables = {}

    def add_table(self, table_name, columns):
        self.tables[table_name] = Table(table_name, columns)

    def get_table(self, table_name):
        return self.tables.get(table_name)

    def create_table(self, table_name, columns=None):
        if table_name in self.tables:
            raise ValueError(f"Table '{table_name}' already exists in the database.")

        if columns is not None:
            self.tables[table_name] = Table(table_name, columns)
        else:
            self.tables[table_name] = Table(table_name)

    def update_table(self, table_name, data):
        table = self.get_table(table_name)
        if table:
            table.update(data)
        else:
            return None

    def insert_data(self, table_name, data):
        table = self.get_table(table_name)
        if table:
            table.insert(data)
        else:
            return None


class Table:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns
        self.data = []

    def insert(self, values):
        # Check if the entry has the correct number of columns
        if len(values) != len(self.columns):
            raise ValueError("Number of columns in the entry does not match the table's schema.")

        # Create a dictionary with column names as keys
        entry_dict = dict(zip(self.columns, values))

        # Add the entry to the data list
        self.data.append(entry_dict)

    def update(self, entry_id, data):
        for entry in self.data:
            if entry.get(entry_id) == entry_id:
                entry.update(data)
                break

    def show_data(self):
        print(f"Data in {self.table_name} table:")
        for entry in self.data:
            print(entry)




# Read data from CSV and insert into a table
csv_file_paths = ['persons.csv', 'login.csv']
csv_reader = CsvReader(file_paths=csv_file_paths)
csv_data = csv_reader.read_csv()

# Create a database and tables
database = Database('my_database')

for file_path in csv_file_paths:
    table_name = file_path.split('.')[0]  # Extract table name from file path
    columns = csv_data[0].keys()  # Extract column names from CSV data
    database.add_table(table_name, columns)

# Insert data into the tables
for entry_data in csv_data:
    table_name_data = entry_data['ID'].split('_')[0]  # Extract table name from ID
    database.insert_data(table_name_data, entry_data)

# Example update
table_to_update = 'persons'
entry_id_to_update = 'id'
key_to_update = 'name'
value_to_update = 'Taylor Swift'

# Assuming 'ID' is the key to identify entries
update_data = {key_to_update: value_to_update}
update_successful = database.tables[table_to_update].update(entry_id_to_update, update_data)

