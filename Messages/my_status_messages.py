from SQL.user_models import Database_user
from SQL.board_models import Database_boards

class MyStatusMessages:

    @staticmethod
    def my_status(user_id: int) -> str:
        base = Database_user()
        login, father_id = base.get_user_data(user_id, ["username", "father_id"])
        father_login = base.get_user_data(father_id, ["username"])[0] if father_id != 0 else login
        return f"📍 Ваш ID: {user_id}\n🔑 Логин: @{login}\n🤝 Кто пригласил: @{father_login}\n\n" \
                  f"📋 Активированные доски:"