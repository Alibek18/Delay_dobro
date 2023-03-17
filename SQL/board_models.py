import uuid

import psycopg2 as ps

from settings import pg_db_credentials, START_KING, START_BUILDER1, START_BUILDER2


class Database_boards:
    def __init__(self):
        self.connect = ps.connect(user=pg_db_credentials['USER'], password=pg_db_credentials['PASSWORD'],
                                  host=pg_db_credentials['HOST'], port=pg_db_credentials['PORT'],
                                  database=pg_db_credentials['DATABASE'])
        self.cursor = self.connect.cursor()
        self.connect.autocommit = True

    def create_table(self) -> None:
        with self.connect:
            for i in range(16):
                sql_str = f'''CREATE TABLE IF NOT EXISTS boards{i}
            (uid TEXT, gifter1 BIGINT, gifter2 BIGINT, gifter3 BIGINT, gifter4 BIGINT, 
            builder1 BIGINT, builder2 BIGINT, king BIGINT, gift_count INT DEFAULT 0, active BOOLEAN DEFAULT TRUE, 
            language TEXT)'''
                self.cursor.execute(sql_str)
            return

    def create_first_boards(self) -> None:
        languages = ("RU", "UZ", "UA", "BY", "KG", "KZ", "TJ", "TM", "TR")
        count = 16
        with self.connect:
            for i in range(16):
                id_str = str(uuid.uuid4()).replace('-', '')
                id_str = '-'.join([id_str[0:4], id_str[4:8], id_str[8:12], id_str[12:16]])
                sql_str = f'''INSERT INTO boards{i} (uid, king, builder1, builder2, language) 
                VALUES ('{id_str}', 5697755398, 5930784733, 5439806977, 'UZ')'''
                self.cursor.execute(sql_str)
                count-=1
                print(count)
        return

    def create_new_board(self, board_index: int, builder1: int, builder2: int, king: int, language: str):
        with self.connect:
            id_str = str(uuid.uuid4()).replace('-', '')
            id_str = '-'.join([id_str[0:4], id_str[4:8], id_str[8:12], id_str[12:16]])
            sql_str = f"INSERT INTO boards{board_index} (uid, builder1, builder2, king, language) " \
                      f"VALUES ('{id_str}', {builder1}, {builder2}, {king}, '{language}') RETURNING uid"
            self.cursor.execute(sql_str)
            return self.cursor.fetchone()[0]

    def set_board_data(self, board_index: str, board_id: str, **kwargs) -> None:
        with self.connect:
            sql_str, value_list = f"UPDATE boards{board_index} SET ", []
            for key, value in kwargs.items():
                sql_str += f'{key}=%s, '
                value_list.append(value)
        return self.cursor.execute(f"{sql_str[:-2]} WHERE uid = %s", (*tuple(value_list), board_id))

    def check_free_gifters_places(self, board_index: str, board_id: str, father_place: str):
        with self.connect:
            if father_place == "king":
                sql_str = f"SELECT gifter1, gifter2, gifter3, gifter4 FROM boards{board_index} WHERE uid='{board_id}'"
                self.cursor.execute(sql_str)
                result = self.cursor.fetchone()
                return result if result else (None, None, None, None)
            elif father_place == "builder1":
                sql_str = f"SELECT gifter1, gifter2 FROM boards{board_index} WHERE uid='{board_id}'"
                self.cursor.execute(sql_str)
                result = self.cursor.fetchone()
                return result if result else (None, None)
            elif father_place == "builder2":
                sql_str = f"SELECT gifter3, gifter4 FROM boards{board_index} WHERE uid='{board_id}'"
                self.cursor.execute(sql_str)
                result = self.cursor.fetchone()
                return result if result else (None, None)
            elif father_place == "gifter1":
                sql_str = f"SELECT gifter2 FROM boards{board_index} WHERE uid='{board_id}'"
                self.cursor.execute(sql_str)
                result = self.cursor.fetchone()
                return result if result else None
            elif father_place == "gifter2":
                sql_str = f"SELECT gifter1 FROM boards{board_index} WHERE uid='{board_id}'"
                self.cursor.execute(sql_str)
                result = self.cursor.fetchone()
                return result if result else None
            elif father_place == "gifter3":
                sql_str = f"SELECT gifter4 FROM boards{board_index} WHERE uid='{board_id}'"
                self.cursor.execute(sql_str)
                result = self.cursor.fetchone()
                return result if result else None
            elif father_place == "gifter4":
                sql_str = f"SELECT gifter3 FROM boards{board_index} WHERE uid='{board_id}'"
                self.cursor.execute(sql_str)
                result = self.cursor.fetchone()
                return result if result else None

    def find_on_board(self, user_id: int, board_index: str, language: str):
        column_names = ("uid", "gifter1", "gifter2", "gifter3", "gifter4", "builder1", "builder2", "king", "active")
        with self.connect:
            sql_str = f"SELECT * FROM boards{board_index} WHERE (gifter1 = {user_id} OR gifter2 = {user_id} " \
                      f"OR gifter3 = {user_id} OR gifter4 = {user_id} OR builder1 = {user_id} OR builder2 = {user_id} " \
                      f"OR king = {user_id}) AND active = True AND language = '{language}';"
            self.cursor.execute(sql_str)
            result = self.cursor.fetchall()
            if result:
                boards_list = [(board[0], column_names[board.index(user_id)]) for board in result]
                return next(((t[0], t[1]) for t in boards_list if t[1] == 'king'),
                            next(((t[0], t[1]) for t in boards_list if 'builder' in t[1]),
                                 next(((t[0], t[1]) for t in boards_list if 'gifter' in t[1]), None)))
            else:
                return result

    def find_board(self, board_id: str):
        with self.connect:
            sql_str = f"SELECT 'boards0' AS boards0, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards0 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards1' AS boards1, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards1 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards2' AS boards2, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards2 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards3' AS boards3, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards3 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards4' AS boards4, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards4 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards5' AS boards5, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards5 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards6' AS boards6, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards6 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards7' AS boards7, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards7 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards8' AS boards8, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards8 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards9' AS boards9, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards9 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards10' AS boards10, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards10 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards11' AS boards11, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards11 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards12' AS boards12, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards12 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards13' AS boards13, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards13 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards14' AS boards14, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards14 WHERE uid='{board_id}' " \
                      f"UNION " \
                      f"SELECT 'boards15' AS boards15, uid, gifter1, gifter2, gifter3, gifter4, builder1, " \
                      f"builder2, king FROM boards15 WHERE uid='{board_id}' "
            self.cursor.execute(sql_str)
        return self.cursor.fetchone()


    def count_boards_in_system(self, board_index: str) -> int:
        with self.connect:
            sql_str = f"SELECT COUNT(*) FROM boards{board_index} WHERE active = True"
            self.cursor.execute(sql_str)
            return self.cursor.fetchone()[0]


    def get_board_data(self, board_id: str, args: list) -> tuple:
        args_string = ','.join(args)
        sql_str = f"SELECT {args_string} FROM (" \
                  f"SELECT {args_string} FROM boards0 UNION ALL " \
                  f"SELECT {args_string} FROM boards1 UNION ALL " \
                  f"SELECT {args_string} FROM boards2 UNION ALL " \
                  f"SELECT {args_string} FROM boards3 UNION ALL " \
                  f"SELECT {args_string} FROM boards4 UNION ALL " \
                  f"SELECT {args_string} FROM boards5 UNION ALL " \
                  f"SELECT {args_string} FROM boards6 UNION ALL " \
                  f"SELECT {args_string} FROM boards7 UNION ALL " \
                  f"SELECT {args_string} FROM boards8 UNION ALL " \
                  f"SELECT {args_string} FROM boards9 UNION ALL " \
                  f"SELECT {args_string} FROM boards10 UNION ALL " \
                  f"SELECT {args_string} FROM boards11 UNION ALL " \
                  f"SELECT {args_string} FROM boards12 UNION ALL " \
                  f"SELECT {args_string} FROM boards13 UNION ALL " \
                  f"SELECT {args_string} FROM boards14 UNION ALL " \
                  f"SELECT {args_string} FROM boards15) AS all_boards " \
                  f"WHERE uid='{board_id}'"
        with self.connect:
            self.cursor.execute(sql_str)
        return self.cursor.fetchone()

# print(Database_boards().create_first_boards())
