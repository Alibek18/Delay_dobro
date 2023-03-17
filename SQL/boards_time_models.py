from datetime import datetime, timedelta

import psycopg2 as ps

from settings import pg_db_credentials


class Database_boards_time:
    def __init__(self):
        self.connect = ps.connect(user=pg_db_credentials['USER'], password=pg_db_credentials['PASSWORD'],
                                  host=pg_db_credentials['HOST'], port=pg_db_credentials['PORT'],
                                  database=pg_db_credentials['DATABASE'])
        self.cursor = self.connect.cursor()
        self.connect.autocommit = True

    def set_new_board_time(self, board_id: str, user_id: int) -> None:
        start_time = datetime.now()
        with self.connect:
            return self.cursor.execute("INSERT INTO boards_time (board_id, user_id, start_time) VALUES (%s, %s, %s)",
                                (board_id, user_id, start_time))

    def check_time_for_ban(self) -> list:
        time_for_check = datetime.now() - timedelta(hours=2)
        with self.connect:
            self.cursor.execute("SELECT id,board_id,user_id FROM boards_time WHERE start_time < %s", (time_for_check,))
            return self.cursor.fetchall()

    def delete(self, board_id: str, user_id: int) -> None:
        with self.connect:
            return self.cursor.execute("DELETE FROM boards_time WHERE board_id = %s AND user_id = %s",
                                       (board_id, user_id))

# print(Database_boards_time().check_time_for_ban())