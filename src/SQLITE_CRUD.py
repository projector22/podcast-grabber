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


    def __del__(self):
        """Class destructor, closes the database connection.
        """
        self.conn.close()


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

    def select_all(self, table: str, fields: str|list = '*', where: dict = None, order_by: str = None, limit: int = None) -> list:
        """Select any amount of data from a table.

        Args:
            table (str): The table to select from.
            fields (str | list, optional): The fields to select. Defaults to '*'.
            where (dict, optional): Where clause if desired. Defaults to None.
            order_by (str, optional): Order by clause if desired. Defaults to None.
            limit (int, optional): Limit by clause. Defaults to None.

        Returns:
            list: List of tuples containing records of from the database.
        """
        sql = self._prepare_select_sql(table, fields, where, order_by, limit)
        if where is not None and len(where) > 0:
            results = self.conn.execute(sql, tuple(self.values))
        else:
            results = self.conn.execute(sql)

        sorted_data = []
        for row in results:
            sorted_data.append(row)
        return sorted_data
        
        

    def select_one(self, table: str, fields: str|list = '*', where: dict = None) -> tuple:
        """Perform a select one string.

        Args:
            table (str): The table to select from.
            fields (str | list, optional): The fields to select. Defaults to '*'.
            where (dict, optional): Where clause if desired. Defaults to None.

        Returns:
            tuple: A single result record.
        """
        sql = self._prepare_select_sql(table, fields, where, limit=1)
        if where is not None and len(where) > 0:
            results = self.conn.execute(sql, tuple(self.values))
        else:
            results = self.conn.execute(sql)
        for row in results:
            sorted_data = row
        return sorted_data

    
    def _prepare_select_sql(self, table: str, fields: str|list = '*', where: dict = None, order_by: str = None, limit: int = None) -> str:
        """Prepare the SQL statement to be used for selecting data.

        Args:
            table (str): The table to select from.
            fields (str | list, optional): The fields to select. Defaults to '*'.
            where (dict, optional): Where clause if desired. Defaults to None.
            order_by (str, optional): Order by clause if desired. Defaults to None.
            limit (int, optional): Limit by clause. Defaults to None.

        Returns:
            str: Fully formed SQL SELECT string.
        """
        sql = "SELECT "
        if type(fields) == list:
            sel_fields = '`' + '`,`'.join(fields) + '`'
        else:
            sel_fields = fields
        sql += "{field} FROM {table_id}".format(
            field=sel_fields,
            table_id=table
        )

        if where is not None and len(where) > 0:
            self.values = []
            sql += self._prepare_where(where)

        if order_by is not None:
            sql += " ORDER BY {ob}".format(ob=order_by)

        if limit is not None:
            sql += " LIMIT {lim}".format(lim=limit)

        return sql
    

    def _prepare_where(self, where: dict) -> str:
        """Prepare the queries, handling things like, not equal or IN

        Args:
            where (dict): The parsed where clauses.

        Returns:
            str: Prepared WHERE string
        """
        like = lambda a : a[-5:] == " LIKE"
        not_like = lambda a : a[-9:] == " NOT LIKE"
        ## Null testing seems to break this, @todo fix
        is_null = lambda a : a[-8:] == " IS NULL"
        is_not_null = lambda a : a[-12:] == " IS NOT NULL"
        is_not_equal = lambda a : a[-3:] == " <>"
        greater_than = lambda a : a[-2:] == " >"
        less_than = lambda a : a[-2:] == " <"
        greater_equals_to = lambda a : a[-3:] == " >="
        less_equals_to = lambda a : a[-3:] == " <="
        is_in = lambda a : a[-3:] == " IN"
        is_not_in = lambda a : a[-7:] == " NOT IN"

        where_str = " WHERE "
        wheres = []
        for key in where:
            if like(key) or not_like(key):
                wheres.append(key + " ?")
                self.values.append(where[key])
            elif is_not_equal(key) or greater_than(key) or less_than(key):
                wheres.append(key + "?")
                self.values.append(where[key])
            elif greater_equals_to(key) or less_equals_to(key):
                wheres.append(key + "?")
                self.values.append(where[key])
            elif is_in(key) or is_not_in(key):
                set_where = key + " ("
                q_marks = []
                for value in where[key]:
                    self.values.append(value)
                    q_marks.append("?")
                set_where += ",".join(q_marks)
                set_where += ")"
                wheres.append(set_where)
            else:
                wheres.append(key + "=?")
                self.values.append(where[key])
        where_str += " AND ".join(wheres)
        return where_str


    def list_tables(self) -> list:
        """Generate a list of tables in the database.

        Returns:
            list: List of table names
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = []
        results = self.cursor.fetchall()
        for table in results:
            tables.append(table[0])
        return tables


    def _kill(self):
        """Kill the script immediately.
        """
        import sys
        sys.exit()
