import sqlite3
from database_errors import InvalidInitializer, InvalidSize
from gevent.event import Event
from shemutils import Logger

'# Define static variables for module'
INTEGER = "INTEGER"
TEXT = "TEXT"
NULL = "NULL"


class Controller(object):
    """
    Controller object made to control execution operations
    """
    def __init__(self, objects):
        if len(objects) < 2:
            del self
        self.handle = objects[0]
        self.cursor = objects[1]
        self.logger = None

    def execute(self, sql):
        if type(sql) is not str:
            return -1
        try:
            self.cursor.execute(sql)  # execute query passed to function
        except sqlite3.OperationalError as e:
            if self.logger:
                self.logger.error("Error executing query: {0}".format(e))
            else:
                raise sqlite3.OperationalError

        if self.logger:
            self.logger.info("Executed SQL: {0}".format(sql))


class Database(object):
    def __init__(self, db_name, verbose=False):
        """
        Database object to control data storage
        Procedures:
            1. Database opening
            2. Controller creation
        :param db_name: string
        """

        '# --------------------------------------- #'
        '# Natural variables '
        self.db_filename = self._parse_db_name(db_name)
        self.open = Event()  # this Flag is used to get database status concerning its ability to operate.
        self.logger = Logger("DATABASE", logfile="%s.log" % db_name)
        '# --------------------------------------- #'

        '# Try to open database fd'
        handle, cursor = self._open()
        '# Give the handles and cursor to Controller Object'
        self.controller = Controller((handle, cursor))
        if verbose is not False:
            self.controller.logger = self.logger

    def _open(self):
        try:
            handle = sqlite3.connect(self.db_filename)
            cursor = handle.cursor()
            self.open.set()
            return handle, cursor
        except Exception as e:
            self.logger.error("Error opening database: {0}".format(e))
            return None

    @staticmethod
    def _parse_db_name(db_filename, extension=".db"):
        k = len(db_filename)
        if db_filename[k-3:] != extension:
            db_filename += extension
        return db_filename

    def save(self):
        return self.controller.handle.commit()

    def close(self):
        return self.controller.handle.close() if self.controller.handle is not None else None


class Table(object):
    """
    To create a table use the following syntax:
    t1 = Table("TableName", {"Name":TEXT, "Age":INTEGER})
    """
    def __init__(self, name, columns):
        self.name = str(name)
        self.columns = columns if self._validate(columns) is 0 else None
        self.num_col = len(self.columns) if self.columns is not None else None

    @staticmethod
    def _validate(columns):
        if type(columns) != dict:
            raise InvalidInitializer
        return 0

    def _colstr(self):
        output = ""
        if not self.columns:
            return -1
        for column in self.columns.keys():
            p = self.columns[column]
            output += "{0} {1}, ".format(p[0], p[1])
        return output[:-2] + ")"

    def create(self):
        """
        :return: string containing SQL to construct the table
        """
        return "CREATE TABLE IF NOT EXISTS {0} (id INTEGER PRIMARY KEY AUTOINCREMENT, {1}".format(self.name,
                                                                                                  self._colstr())

    def remove_row(self, c, k):
        """
        :param c: string containing column name
        :param k: string to search through table
        :return: string containing SQL query to do the desired operation
        """
        return "DELETE FROM {0} WHERE {1} = '{2}'".format(self.name, c, k)

    def remove_rows(self, c, k):
        """
        :param c: string containing column name
        :param k: string to search through table
        :return: string containing SQL query to do the desired operation
        """
        return "DELETE FROM {0} WHERE {1} LIKE '%{2}%'".format(self.name, c, k)

    def update_row(self, c2, k, c1, v):
        """
        :param c1: string containing column to be updated
        :param v: string containing new value for the row
        :param c2: string containing column name for the query condition
        :param k: string containing keyword value for the query condition
        :return: string containing SQL query to do the desired operation
        """
        return "UPDATE {0} SET {1} = '{2}' WHERE {3} LIKE '%{4}%'".format(self.name, c1, k, c2, v)

    def insert_data(self, data):
        """
        :param data: list containing data in the same number of elements that this table has -1 (for id column)
        :return: string containing SQL query to do the desired operation
        """
        if type(data) != list:
            raise TypeError
        return "INSERT INTO {0} VALUES (NULL, {1})".format(self.name, self._format_data(data))

    def _format_data(self, data):
        output = ""
        if type(data) != list:
            raise TypeError
        if len(data) != self.num_col:
            raise InvalidSize
        for d in data:
            output += "'{0}', ".format(d)
        return output[:-2]
