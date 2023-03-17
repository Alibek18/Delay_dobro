import psycopg2 as ps

from settings import pg_db_credentials


class Database_user:
    def __init__(self):
        self.connect = ps.connect(user=pg_db_credentials['USER'], password=pg_db_credentials['PASSWORD'],
                                  host=pg_db_credentials['HOST'], port=pg_db_credentials['PORT'],
                                  database=pg_db_credentials['DATABASE'])
        self.cursor = self.connect.cursor()
        self.connect.autocommit = True

    def create_table(self) -> None:
        with self.connect:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (user_id BIGINT PRIMARY KEY, username TEXT, user_full_name TEXT, user_phone TEXT, ref_link TEXT,
            father_id BIGINT, 
            country TEXT, activated BOOLEAN DEFAULT FALSE, gifts_received_count INT DEFAULT 0, 
            gift_received INT DEFAULT 0, gift_sent_count INT DEFAULT 0, gift_sent INT DEFAULT 0, 
            ban_count INT DEFAULT 0, banned_to TIMESTAMP)''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS boards_access 
            (user_id BIGINT PRIMARY KEY, board0 BOOLEAN DEFAULT TRUE, board1 BOOLEAN DEFAULT FALSE,
            board2 BOOLEAN DEFAULT FALSE, board3 BOOLEAN DEFAULT FALSE, board4 BOOLEAN DEFAULT FALSE,
            board5 BOOLEAN DEFAULT FALSE, board6 BOOLEAN DEFAULT FALSE, board7 BOOLEAN DEFAULT FALSE,
            board8 BOOLEAN DEFAULT FALSE, board9 BOOLEAN DEFAULT FALSE, board10 BOOLEAN DEFAULT FALSE, 
            board11 BOOLEAN DEFAULT FALSE, board12 BOOLEAN DEFAULT FALSE, board13 BOOLEAN DEFAULT FALSE, 
            board14 BOOLEAN DEFAULT FALSE, board15 BOOLEAN DEFAULT FALSE)''')
            return self.cursor.execute('''CREATE TABLE IF NOT EXISTS boards_time 
                        (id SERIAL PRIMARY KEY, board_id TEXT, user_id BIGINT, start_time TIMESTAMP)''')

    def is_new_user(self, user_id: int) -> bool:
        with self.connect:
            self.cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            return bool(not len(self.cursor.fetchall()))

    def is_referral_link_exists(self, ref_link: str) -> bool:
        with self.connect:
            self.cursor.execute("SELECT ref_link FROM users WHERE ref_link = %s", (ref_link,))
            return bool(len(self.cursor.fetchall()))

    def create_new_user(self, user_id: int, ref_link: str, father_id: int) -> None:
        with self.connect:
            self.cursor.execute("INSERT INTO users (user_id, ref_link, father_id) "
                                       "VALUES (%s, %s, %s)", (user_id, ref_link, father_id))
            return self.cursor.execute("INSERT INTO boards_access (user_id) "
                                "VALUES (%s)", (user_id,))

    def find_father(self, ref_link: str) -> int:
        with self.connect:
            self.cursor.execute("SELECT user_id FROM users WHERE ref_link=%s",(ref_link,))
            result = self.cursor.fetchone()
            return result[0] if result else 0

    def get_user_data(self, user_id: int, args: list) -> tuple:
        args_string = ','.join(args)
        sql_str = f"SELECT {args_string} FROM users WHERE user_id=%s"
        with self.connect:
            self.cursor.execute(sql_str, (user_id,))
        return self.cursor.fetchall()[0]

    def set_user_data(self, user_id: int, **kwargs) -> None:
        with self.connect:
            sql_str, value_list = f"UPDATE users SET ", []
            for key, value in kwargs.items():
                sql_str += f'{key}=%s, '
                value_list.append(value)
        return self.cursor.execute(f"{sql_str[:-2]} WHERE user_id = %s", (*tuple(value_list), user_id))

    def get_boards_access(self, user_id: int) -> tuple:
        with self.connect:
            self.cursor.execute('''SELECT * FROM boards_access WHERE user_id=%s''',(user_id,))
            return self.cursor.fetchall()[0]

    def set_boards_access(self, user_id: int, board_index: str) -> None:
        sql_str = f"UPDATE boards_access SET {board_index}=True WHERE user_id=%s"
        with self.connect:
            return self.cursor.execute(sql_str,(user_id,))

    def count_partners_on_board(self, user_id: int, board_info: tuple) -> int:
        count = 0
        for person_id in board_info[2:]:
            if person_id is not None:
                result = self.get_user_data(person_id, ["father_id"])
                count += 1 if result[0] == user_id else 0
        return count


# print(Database_user().get_user_data(2054965991, ["country"])[0])
