from SQL.user_models import Database_user


class Admin_Panel_Messages:
    def __init__(self):
        self.ask_father_id = "Введите ID Наставника"
        self.not_isdigit_id = "ID должен состоять только из цифр!"
        self.not_find_user = "Пользователь не найден!"
        self.change_father_id_ask_user_id = "Введите User ID"
        self.admin_panel = "Выберите функцию"

    @staticmethod
    def find_user(user_id: int, change: bool):
        user_id, username, user_full_name, user_phone, father_id, country = \
            Database_user().get_user_data(user_id, ["user_id", "username", "user_full_name", "user_phone",
                                                    "father_id", "country"])
        father_username = Database_user().get_user_data(father_id, ["username"])[0]
        first_row = "Пользователь найден!\n\n" if not change else "Данные пользователя изменены!\n\n"
        return first_row + \
            f"ID: {user_id}\n" \
            f"Username: @{username}\n" \
            f"Имя: {user_full_name}\n" \
            f"Телефон: {user_phone}\n" \
            f"Страна: {country}\n\n" \
            f"ID Наставника: {father_id}\n" \
            f"Username Наставника: @{father_username}"

    @staticmethod
    def find_father(father_id: int, user_id: int):
        new_father_id, new_father_username, new_father_user_full_name, new_father_user_phone, new_father_country = \
            Database_user().get_user_data(father_id, ["user_id", "username", "user_full_name", "user_phone", "country"])

        user_id, username, user_full_name, user_phone, old_father_id, country = \
            Database_user().get_user_data(user_id, ["user_id", "username", "user_full_name", "user_phone",
                                                    "father_id", "country"])
        old_father_username = Database_user().get_user_data(father_id, ["username"])

        return f"Данные пользователя:\n\n" \
               f"ID: {user_id}\n" \
               f"Username: @{username}\n" \
               f"Имя: {user_full_name}\n" \
               f"Телефон: {user_phone}\n" \
               f"Страна: {country}\n" \
               f"ID текщего Наставника: {old_father_id}\n" \
               f"Username текущего Наставника: @{old_father_username}\n\n" \
               f"Данные Наставника на замену:\n\n" \
               f"ID: {new_father_id}\n" \
               f"Username: @{new_father_username}\n" \
               f"Имя: {new_father_user_full_name}\n" \
               f"Телефон: {new_father_user_phone}\n" \
               f"Страна: {new_father_country}\n\n" \
               f"Все верно, заменить?"
