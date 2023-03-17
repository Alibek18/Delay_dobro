from SQL.board_models import Database_boards
from SQL.operations_models import Database_operations
from SQL.user_models import Database_user


class MyBoardsMessages:

    def __init__(self):
        self.board_gifters = "Дарители:"
        self.no_access_board = "‼️ Вы должны сначала закрыть предыдущую доску и пройти квалификацию пригласив " \
                               "нового участника, который должен отправить подарок!"

    @staticmethod
    def board_names(user_id: int) -> tuple:
        language = Database_user().get_user_data(user_id, ["country"])[0]
        gift_size = {
            "RU": ("100", "200", "400", "800", "1,600", "3,200", "6,400", "12,000", "24,000", "48,000", "100,000",
                   "200,000", "400,000", "800,000", "1,600,000", "3,200,000"),
            "UZ": ("10,000", "20,000", "40,000", "80,000", "160,000", "320,000", "640,000", "1,200,000", "2,400,000",
                   "4,800,000", "10,000,000", "20,000,000", "40,000,000", "80,000,000", "160,000,000", "320,000,000"),
            "BY": ("5", "10", "20", "40", "80", "160", "320", "640", "1,200", "2,400", "4,800", "10,000", "20,000",
                   "40,000", "80,000", "160,000"),
            "KG": ("100", "200", "400", "800", "1,600", "3,200", "6,400", "12,000", "24,000", "48,000", "100,000",
                   "200,000", "400,000", "800,000", "1,600,000", "3,200,000"),
            "KZ": ("500", "1,000", "2,000", "4,000", "8,000", "16,000", "32,000", "64,000", "120,000", "240,000",
                   "480,000", "1,000,000", "2,000,000", "4,000,000", "8,000,000", "16,000,000"),
            "TJ": ("10", "20", "40", "80", "160", "320", "640", "1,200", "2,400", "4,800",
                   "10,000", "20,000", "40,000", "80,000", "160,000", "320,000"),
            "TM": ("5", "10", "20", "40", "80", "160", "320", "640", "1,200", "2,400", "4,800", "10,000", "20,000",
                   "40,000", "80,000", "160,000"),
            "TR": ("20", "40", "80", "160", "320", "640", "1,200", "2,400", "4,800", "10,000", "20,000", "40,000",
                   "80,000", "160,000", "320,000", "640,000"),
            "UA": ("50", "100", "200", "400", "800", "1,600", "3,200", "6,400", "12,000", "24,000", "48,000",
                   "100,000", "200,000", "400,000", "800,000", "1,600,000")
        }
        return (f"Начальная-I 🎁{gift_size[language][0]}",
                f"Начальная-II 🎁{gift_size[language][1]}",
                f"Начальная-III 🎁{gift_size[language][2]}",
                f"Средняя 🎁{gift_size[language][3]}",
                f"Железная 🎁{gift_size[language][4]}",
                f"Бронзовая 🎁{gift_size[language][5]}",
                f"️Серебро 🎁{gift_size[language][6]}",
                f"Нефритовая 🎁{gift_size[language][7]}",
                f"Хрустальная 🎁{gift_size[language][8]}",
                f"Золотая 🎁{gift_size[language][9]}",
                f"️Платина 🎁{gift_size[language][10]}",
                f"Адамантовый 🎁{gift_size[language][11]}",
                f"Жемчужная 🎁{gift_size[language][12]}",
                f"Алмазная 🎁{gift_size[language][13]}",
                f"Кристальная 🎁{gift_size[language][14]}",
                f"️Элитная 🎁{gift_size[language][15]}")

    @staticmethod
    def my_boards(user_id: int) -> str:
        base = Database_user()
        gifts_received = base.get_user_data(user_id, ['gift_received'])
        return f"🏆 Список досок в которых вы участвуете 🏆\n\n🎁 Ваши подарки: {gifts_received[0]} руб."

    @staticmethod
    def accept_board(user_id: int) -> str:
        base = Database_user()
        father_id = base.get_user_data(user_id, ["father_id"])[0]
        father_login, father_phone = base.get_user_data(father_id, ["username", "user_phone"])
        return f"⚠️ ВНИМАНИЕ!!!\n\n‼️ Убедитесь, что вашего наставника есть свободные места на доске.\n\n" \
               f"🔸 Логин наставника: @{father_login}\n🔸 Номер телефона: {father_phone}\n\n" \
               f"✅ Если на доске наставника нет свободных мест, вы попадете на доску к его наставнику или ещё " \
               f"выше.\n\n"

    @staticmethod
    def board(user_id: int, board_id: str, place: str) -> str:
        base, b_base, o_base = Database_user(), Database_boards(), Database_operations()
        boards = ("🔴Начальная-I", "⭕️Начальная-II", "♦️Начальная-III", "🟤Средняя", "🌑Железная", "🟠Бронзовая",
                  "⚪️Серебро", "🟢Нефритовая", "🌀Хрустальная", "🟡Золотая", "⚫️Платина", "🔵Адамантовая",
                  "🫧Жемчужная", "💎Алмазная", "🍸Кристальная", "⭐️Элитная")
        places = {"gifter0": "Даритель", "gifter1": "Даритель", "gifter2": "Даритель", "gifter3": "Даритель",
                  "builder1": "Строитель", "builder2": "Строитель", "king": "Получатель"}
        board_info = b_base.find_board(board_id)
        board_index = int(board_info[0][-1])
        gifter_count = len([x for x in board_info[2:6] if x is not None])
        partners_count = base.count_partners_on_board(user_id, board_info)
        approve_gifts_count = o_base.get_count_of_approved_gifts_on_board(board_id)
        boards_access = base.get_boards_access(user_id)[1:]
        if len(set(boards_access)) == 1:
            kvalification = "✅"
        else:
            kvalification = "✅" if boards_access[board_index + 1] == True else "❌"
        return f"❇️ Доска - {boards[board_index]}\n" \
               f"⚜️ ID Доски: {board_info[1]}\n" \
               f"👥 Дарителей на доске: {gifter_count}\n" \
               f"🎁 Подтверждено: {approve_gifts_count} из 4\n" \
               f"📍 Место: {places.get(place)}\n" \
               f"🔑 Квалификация: {kvalification}\n" \
               f"🚻 Партнеров на доске: {partners_count}\n"
               # f"🔁 Пройдено досок <i>count board complete</i>"

    @staticmethod
    def king_data(board_id: str, user_id: int):
        base, b_base, o_base = Database_user(), Database_boards(), Database_operations()
        king_id = b_base.get_board_data(board_id, ["uid", "king"])[1]
        king_data = base.get_user_data(king_id, ["username", "user_full_name", "user_phone", "father_id"])
        father_username = base.get_user_data(king_data[3], ["username"])[0]
        board_info = b_base.find_board(board_id)
        partners_count = base.count_partners_on_board(king_id, board_info)
        language = base.get_user_data(user_id, ["country"])[0]
        summ_dict = {
            "RU": ("100", "200", "400", "800", "1,600", "3,200", "6,400", "12,000", "24,000", "48,000", "100,000",
                   "200,000", "400,000", "800,000", "1,600,000", "3,200,000"),
            "UZ": ("10,000", "20,000", "40,000", "80,000", "160,000", "320,000", "640,000", "1,200,000", "2,400,000",
                   "4,800,000", "10,000,000", "20,000,000", "40,000,000", "80,000,000", "160,000,000", "320,000,000"),
            "BY": ("5", "10", "20", "40", "80", "160", "320", "640", "1,200", "2,400", "4,800", "10,000", "20,000",
                   "40,000", "80,000", "160,000"),
            "KG": ("100", "200", "400", "800", "1,600", "3,200", "6,400", "12,000", "24,000", "48,000", "100,000",
                   "200,000", "400,000", "800,000", "1,600,000", "3,200,000"),
            "KZ": ("500", "1,000", "2,000", "4,000", "8,000", "16,000", "32,000", "64,000", "120,000", "240,000",
                   "480,000", "1,000,000", "2,000,000", "4,000,000", "8,000,000", "16,000,000"),
            "TJ": ("10", "20", "40", "80", "160", "320", "640", "1,200", "2,400", "4,800",
                   "10,000", "20,000", "40,000", "80,000", "160,000", "320,000"),
            "TM": ("5", "10", "20", "40", "80", "160", "320", "640", "1,200", "2,400", "4,800", "10,000", "20,000",
                   "40,000", "80,000", "160,000"),
            "TR": ("20", "40", "80", "160", "320", "640", "1,200", "2,400", "4,800", "10,000", "20,000", "40,000",
                   "80,000", "160,000", "320,000", "640,000"),
            "UA": ("50", "100", "200", "400", "800", "1,600", "3,200", "6,400", "12,000", "24,000", "48,000",
                   "100,000", "200,000", "400,000", "800,000", "1,600,000")
        }
        currency = {
            "RU": "РУБ|RUB", "UZ": "Сум", "BY": "РУБ|BYN", "KG": "Сом", "KZ": "Тенге", "TJ": "Сомони", "TM": "Манат",
            "TR": "Лира", "UA": "Гривна"
        }
        is_sent_gift = o_base.is_sent_gift_to_king(board_id, user_id, king_id)
        if is_sent_gift == 0 or is_sent_gift == "Not confirmed":
            gift_msg = f"Сумма к дарению: {summ_dict[language][int(board_info[0][-1])]} {currency[language]}"
        elif is_sent_gift == "Confirmed":
            gift_msg = f"Подарено: {summ_dict[language][int(board_info[0][-1])]} {currency[language]}"
        elif is_sent_gift == "Waiting":
            gift_msg = f"Ожидаем подтверждения от получателя вашего отправленного подарка" \
                       f" {summ_dict[language][int(board_info[0][-1])]} {currency[language]}"
        else:
            gift_msg = "<i>system_error</i>"
        return f"🔑 Логин: @{king_data[0]}\n" \
               f"🙂 Имя: {king_data[1]}\n" \
               f"☎️ Телефон: {king_data[2]}\n" \
               f"🤝 Кто пригласил: @{father_username}\n" \
               f"✳️ Партнеров на доске: {partners_count}\n" \
               f"🎁 {gift_msg}"

    @staticmethod
    def board_family(board_info: tuple) -> str:
        base, b_base = Database_user(), Database_boards()
        message = ""
        for i in range(7):
            if board_info[i + 2] is not None:
                username, user_full_name, father_id = base.get_user_data(board_info[i + 2],
                                                                         ["username", "user_full_name",
                                                                          "father_id"])
                father_username = base.get_user_data(father_id, ["username"])[0]
                partners_count = base.count_partners_on_board(board_info[i + 2], board_info)
                if i + 2 in [2, 3, 4, 5]:
                    status = "🥇 Даритель"
                elif i + 2 in [6, 7]:
                    status = "🥈 Строитель"
                elif i + 2 == 8:
                    status = "🏵 Получатель"
                else:
                    status = ""
                board_index = int(board_info[0][-1])
                boards_access = base.get_boards_access(board_info[i + 2])[1:]
                if len(set(boards_access)) == 1:
                    kvalification = "✅"
                else:
                    kvalification = "✅" if boards_access[board_index + 1] == True else "❌"
                message += f"🏆Статус: {status}\n" \
                           f"🔑Логин: @{username}\n" \
                           f"👤Имя: {user_full_name}\n" \
                           f"🎓Кто пригласил: @{father_username}\n" \
                           f"🔑 Квалификация: {kvalification}\n" \
                           f"👥Партнеров на доске: {partners_count}\n\n"
                           # f"🔁 Пройдено досок: <i>count boards complete</i>\n\n"
        return message

    @staticmethod
    def gifter_data(gifter_id: str, board_id: str) -> str:
        base, b_base = Database_user(), Database_boards()
        username, user_full_name, father_id = base.get_user_data(int(gifter_id), ["username", "user_full_name",
                                                                                  "father_id"])
        father_username = base.get_user_data(father_id, ["username"])[0]
        board_info = b_base.find_board(board_id)
        partners_count = base.count_partners_on_board(int(gifter_id), board_info)
        return f"👤Имя: {user_full_name}\n" \
               f"🔑Логин: @{username}\n" \
               f"🎓Кто Пригласил: @{father_username}\n" \
               f"👥Партнеров на доске: {partners_count}"

    @staticmethod
    def gifter_added(user_id: int, board_index: str, board_id: str) -> str:
        base = Database_user()
        username = base.get_user_data(user_id, ["username"])
        boards = ("🔴Начальная-I", "⭕️Начальная-II", "♦️Начальная-III", "🟤Средняя", "🌑Железная", "🟠Бронзовая",
                  "⚪️Серебро", "🟢Нефритовая", "🌀Хрустальная", "🟡Золотая", "⚫️Платина", "🔵Адамантовая",
                  "🫧Жемчужная", "💎Алмазная", "🍸Кристальная", "⭐️Элитная")
        return "😻 На вашу доску присоедился Даритель!\n\n" \
               f"🔑 Логин: @{username[0]}\n" \
               f"🥇 Тип доски: {boards[int(board_index)]}\n" \
               f"📍 ID доски: {board_id}\n\n" \
               f"🎯 Успевайте занять свободные места!"
