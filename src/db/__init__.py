import warnings
from data_base_manager import *
from .utils import sql_execute



class SQLParser:
    def __init__(self):
        self.db_name = 'data.db'
        self.tables = ['video', 'playlist', 'channel']

    # def get(self, name_of_table, link):#
    #     with sql_execute(self.db_name) as cursor:
    #         answer = list(cursor.execute("""SELECT * FROM {} WHERE link = '{}'"""
    #                                      .format(name_of_table, link)))
    #     return answer

    def get_all(self, name_of_table):
        with sql_execute(self.db_name) as cursor:
            answer = list(cursor.execute("""SELECT * FROM {} """.format(name_of_table)))
        return answer

    def get_video_with_status(self, status):
        update_videos(self)
        with sql_execute(self.db_name) as cursor:
            answer = list(cursor.execute("""SELECT * FROM {} WHERE status = '{}'""".format(self.tables[0], status)))
        if len(answer) == 0:
            return ''
        else:
            return answer[0][0]

    def set_status(self, link, status):  #
        with sql_execute(self.db_name) as cursor:
            if (len(list(cursor.execute(
                    """SELECT * FROM {} WHERE link = '{}'""".format(self.tables[0], link)))) == 0):
                cursor.execute("""INSERT INTO {} VALUES ('{}', '{}')""".format(self.tables[0], link, status))
            else:
                cursor.execute(
                    """UPDATE {} SET status = '{}' WHERE link = '{}'""".format(self.tables[0], status, link))

    def save(self, name_of_table, link, status=None):
        if not name_of_table == self.tables[0]:
            with sql_execute(self.db_name) as cursor:
                if (len(list(cursor.execute(
                        """SELECT * FROM {} WHERE link = '{}'""".format(name_of_table, link)))) == 0):
                    cursor.execute(f"INSERT INTO '{name_of_table}' VALUES ('{link}')")
        else:
            with sql_execute(self.db_name) as cursor:
                if (len(list(cursor.execute(
                        """SELECT * FROM {} WHERE link = '{}'""".format(name_of_table, link)))) == 0):
                    cursor.execute(f"INSERT INTO '{name_of_table}' VALUES ('{link}', '{status}')")

    def clear_db(self, name_of_table=None):
        with sql_execute(self.db_name) as cursor:
            if name_of_table is not None:
                # TODO: try unary quotes!
                try:
                    cursor.execute("""DELETE FROM {}""".format(name_of_table))
                except:
                    warnings.warn(message=name_of_table + " was already deleted",
                                  category=UserWarning, stacklevel=1)
            else:
                for i in self.tables:
                    try:
                        cursor.execute("""DELETE FROM {}""".format(i))
                    except:
                        warnings.warn(message=i + " was already deleted", category=UserWarning, stacklevel=1)

    def create_db(self):
        with sql_execute(self.db_name) as cursor:
            try:
                cursor.execute(f"""CREATE TABLE {self.tables[0]} (link, status)""")
            except:
                warnings.warn(message="0 table was already created", category=UserWarning, stacklevel=1)
            try:
                cursor.execute(f"""CREATE TABLE {self.tables[1]} (link)""")
            except:
                warnings.warn(message="1 table was already created", category=UserWarning, stacklevel=1)
            try:
                cursor.execute(f"""CREATE TABLE {self.tables[2]} (link)""")
            except:
                warnings.warn(message="2 table was already created", category=UserWarning, stacklevel=1)

    def get_videos_with_status(self, status):
        update_videos(self)
        with sql_execute(self.db_name) as cursor:
            answer = list(
                cursor.execute("""SELECT * FROM {} WHERE status = '{}'""".format(self.tables[0], status)))
        return answer
