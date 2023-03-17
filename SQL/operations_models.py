from datetime import datetime

import psycopg2 as ps

from settings import pg_db_credentials


class Database_operations:
    def __init__(self):
        self.connect = ps.connect(user=pg_db_credentials['USER'], password=pg_db_credentials['PASSWORD'],
                                  host=pg_db_credentials['HOST'], port=pg_db_credentials['PORT'],
                                  database=pg_db_credentials['DATABASE'])
        self.cursor = self.connect.cursor()
        self.connect.autocommit = True

    def create_table(self) -> None:
        sql_str = '''CREATE TABLE IF NOT EXISTS operations (id SERIAL PRIMARY KEY, board_id TEXT, board_index TEXT, 
        sender_id BIGINT, recipient_id BIGINT, amount INT, approve BOOLEAN, sent_time TIMESTAMP)'''
        with self.connect:
            return self.cursor.execute(sql_str)

    def create_new_operation(self, board_id: str, board_index: str, sender_id: int, recipient_id: int, amount:int,
                             sent_time: datetime) -> int:
        with self.connect:
            self.cursor.execute("INSERT INTO operations (board_id, board_index, sender_id, recipient_id, "
                                       "amount, sent_time) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                                       (board_id, board_index, sender_id, recipient_id, amount, sent_time))
            return self.cursor.fetchone()[0]

    def set_operation_data(self, operation_id: int, **kwargs) -> None:
        with self.connect:
            sql_str, value_list = f"UPDATE operations SET ", []
            for key, value in kwargs.items():
                sql_str += f'{key}=%s, '
                value_list.append(value)
        return self.cursor.execute(f"{sql_str[:-2]} WHERE id = %s", (*tuple(value_list), operation_id))

    def get_operation_data(self, operation_id: int) -> tuple:
        with self.connect:
            self.cursor.execute("SELECT * FROM operations WHERE id=%s", (operation_id,))
            return self.cursor.fetchone()

    def get_count_of_approved_gifts_on_board(self, board_id: str) -> int:
        with self.connect:
            self.cursor.execute("SELECT COUNT(*) FROM operations WHERE board_id=%s AND approve=True", (board_id,))
            return self.cursor.fetchone()[0]

    def is_sent_gift_to_king(self, board_id: str, user_id: int, king_id: int):
        with self.connect:
            self.cursor.execute("SELECT approve FROM operations WHERE (board_id=%s AND sender_id=%s AND "
                                "recipient_id=%s) "
                                "AND (approve=True OR approve is NULL)", (board_id, user_id, king_id))
            try:
                result = self.cursor.fetchone()[0]
                if result:
                    return "Confirmed"
                elif not result and result is not None:
                    return "Not confirmed"
                elif result is None:
                    return "Waiting"
            except: return 0

    def get_board_operations(self, board_id: str) -> list:
        with self.connect:
            self.cursor.execute("SELECT sender_id FROM operations WHERE board_id=%s AND approve=True",(board_id,))
            return self.cursor.fetchall()

# print(Database_operations().get_operation_data(20))