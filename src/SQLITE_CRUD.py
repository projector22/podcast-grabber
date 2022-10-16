class crud:
    """Perform various CRUD operations against an SQLite database.

    Author:
        Gareth Palmer <bravdthepally@gmail.com>
    """
    def __init__(self, db_name: str) -> None:
        """Class Constructor

        Args:
            db_name (str): Name of the database to be worked on.
        """
        self.db_name = db_name
        import sqlite3
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()


    def create_table(self, table_name: str, field_list: list) -> None:
        """Create a table on the database.

        Args:
            table_name (str): Name of the new table.
            field_list (list): list of strings which indicate what fields should be used.
        """
        sql = 'CREATE TABLE {table} ({fields});'.format(table=table_name, fields=', '.join(field_list))
        self.conn.execute(sql)


    def insert(self, table: str, fields: dict):
        """Perform an SQL INSERT operation.

        Args:
            table (str): The table into which the data should be inserted
            fields (dict): Key => Value pairs of data to insert.
        """
        field_labels = []
        q_marks = []
        value_data = []
        for line in fields:
            field_labels.append(line)
            q_marks.append('?')
            value_data.append(fields[line])
        sql = 'INSERT INTO {table_name} ({fields_l}) VALUES ({values})'.format(
            table_name=table,
            fields_l=','.join(field_labels),
            values=','.join(q_marks)
        )
        self.conn.execute(sql, tuple(value_data))
        self.conn.commit()


    def update(self):
        pass
    def delete(self):
        pass

    def select_all(self):
        pass
    def select_one(self):
        pass