import warnings
from .utils import sql_execute


class SQLParser:
    def __init__(self):
        self.db_name = 'lecture_bot.db'
        self.tables = ['users_table', 'videolinks_table', 'playlistlinks_table']

    def get(self, num_of_table, link):
        with sql_execute(self.db_name) as cursor:
            answer = list(cursor.execute("""SELECT * FROM {} WHERE link = '{}'"""
                                         .format(self.tables[num_of_table], link)))
        return answer

    def get_all(self, num_of_table):
        with sql_execute(self.db_name) as cursor:
            answer = list(cursor.execute("""SELECT * FROM {} """.format(self.tables[num_of_table])))
        return answer

    def get_status(self, num_of_table, link):
        with sql_execute(self.db_name) as cursor:
            answer = list(cursor.execute("""SELECT * FROM {} WHERE link = '{}'""".format(self.tables[num_of_table], link)))
        if len(answer) == 0:
            return ''
        else:
            return answer[0][1]

    def set_status(self, num_of_table, link, status):
        with sql_execute(self.db_name) as cursor:
            if (len(list(cursor.execute(
                    """SELECT * FROM {} WHERE link = '{}'""".format(self.tables[num_of_table], link)))) == 0):
                cursor.execute("""INSERT INTO {} VALUES ('{}', '{}')""".format(self.tables[num_of_table], link, status))
            else:
                cursor.execute(
                    """UPDATE {} SET status = '{}' WHERE link = '{}'""".format(self.tables[num_of_table], status, link))

    def save(self, num_of_table, link, status):
        with sql_execute(self.db_name) as cursor:
            if (len(list(cursor.execute(
                    """SELECT * FROM {} WHERE link = '{}'""".format(self.tables[num_of_table], link)))) == 0):
                cursor.execute(f"INSERT INTO '{self.tables[num_of_table]}' VALUES ('{link}', '{status}')")
            else:
                answer = list(
                    cursor.execute("""SELECT * FROM {} WHERE link = '{}'""".format(self.tables[num_of_table], link)))
                status = answer[0][1]
        return status

    def clear_db(self, num_of_table=None):
        with sql_execute(self.db_name) as cursor:
            if num_of_table is not None:
                # TODO: try unary quotes!
                try:
                    cursor.execute("""DELETE FROM {}""".format(self.tables[num_of_table]))
                except:
                    warnings.warn(message=self.tables[num_of_table] + " was already deleted",
                                  category=UserWarning, stacklevel=1)
            else:
                for i in self.tables:
                    try:
                        cursor.execute("""DELETE FROM {}""".format(i))
                    except:
                        warnings.warn(message=i + " was already deleted", category=UserWarning, stacklevel=1)

    def create_db(self):
        with sql_execute(self.db_name) as cursor:
            for i in self.tables:
                try:
                    cursor.execute(f"""CREATE TABLE {i} (link, status)""")
                except:
                    warnings.warn(message=i+" was already created", category=UserWarning , stacklevel=1)

        self.save(0, 423216896, 'admin')

    def get_with_status(self, num_of_table, status):
        with sql_execute(self.db_name) as cursor:
            answer = list(
                cursor.execute("""SELECT * FROM {} WHERE status = '{}'""".format(self.tables[num_of_table], status)))
        return answer
