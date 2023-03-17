from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from SQL.board_models import Database_boards
from SQL.operations_models import Database_operations
from SQL.user_models import Database_user
from Messages.my_boards_messages import MyBoardsMessages
from Keyboards.GlobalKeyboards import back_to_main_menu_with_custom_back, global_back_main_menu_button, \
    global_back_button

class MyBoardsInlineKeyboards(InlineKeyboardMarkup):

    def my_boards(self, user_id: int):
        access_tuple = Database_user().get_boards_access(user_id)[1:]
        button_names = MyBoardsMessages().board_names(user_id)
        yes, no = "✅", "❌"
        buttons = []
        for i, access in enumerate(access_tuple):
            text = f"{yes} {button_names[i]}" if access_tuple[i] else f"{no} {button_names[i]}"
            callback_data = f"my_board_{i}"
            button = InlineKeyboardButton(text=text, callback_data=callback_data)
            buttons.append(button)
        for button in reversed(buttons):
            self.row(button)
        return self.row(global_back_main_menu_button())

    def accept_board(self, board_index) -> InlineKeyboardMarkup:
        self.row(InlineKeyboardButton(text="✅ Подтверждаю", callback_data=f"accept_board_{board_index}"))
        return self.row(InlineKeyboardButton(text="⛔️ Еще подожду", callback_data="my_boards"))

    @staticmethod
    def no_access_board() -> InlineKeyboardMarkup:
        return back_to_main_menu_with_custom_back("my_boards")

    def board(self, board_id: str, place: str) -> InlineKeyboardMarkup:
        buttons = (
            InlineKeyboardButton(text="⚜️ Данные получателя", callback_data=f"king_data_{board_id}"),
            InlineKeyboardButton(text="👨‍👩‍👧‍👦 Показать команду доски", callback_data=f"board_family_{board_id}"),
            InlineKeyboardButton(text="👥 Показать дарителей", callback_data=f"board_gifters_{board_id}")
        )
        if place.find("gifter") != -1 or place.find("builder") != -1:
            for button in buttons:
                self.row(button)
        else:
            self.row(buttons[1])
            self.row(buttons[2])
        self.row(global_back_button("my_boards"))
        return self.row(global_back_main_menu_button())

    def king_data(self, board_id: str, board_index: str, user_id: int) -> InlineKeyboardMarkup:
        base, b_base, o_base = Database_user(), Database_boards(), Database_operations()
        language = base.get_user_data(user_id, ["country"])[0]
        king_id = b_base.get_board_data(board_id, ["uid", "king"])[1]
        king_data = base.get_user_data(king_id, ["username", "user_full_name", "user_phone"])
        is_sent_gift = o_base.is_sent_gift_to_king(board_id, user_id, king_id)
        user_place = b_base.find_on_board(user_id, board_index, language)[1]
        self.row(InlineKeyboardButton(text="☎️ Связаться с получателем", url=f"https://t.me/{king_data[0]}"))
        if (is_sent_gift == 0 or is_sent_gift == "Not confirmed") and user_place.find("builder") == -1 \
                and user_place != "king":
            self.row(InlineKeyboardButton(text="✅ Я отправил подарок",
                                      callback_data=f"sentgift_{board_index}_{board_id}"))
        self.row(global_back_button(f"my_board_{board_index}"))
        return self.row(global_back_main_menu_button())

    def board_family(self, board_info) -> InlineKeyboardMarkup:
        self.row(global_back_button(f"my_board_{board_info[0][-1]}"))
        return self.row(global_back_main_menu_button())

    def board_gifters(self, board_info: tuple) -> InlineKeyboardMarkup:
        base, o_base, gifters_list, default_list, prefix_emodzi = Database_user(), Database_operations(), [], \
            ["🥇 Даритель-1", "🥇 Даритель-2", "🥇 Даритель-3", "🥇 Даритель-4"], ["✅", "⏳", "❌"]
        for user_id in board_info[2:6]:
            if user_id is not None:
                gift_status = o_base.is_sent_gift_to_king(board_info[1], user_id, board_info[8])
                if gift_status == 0 or gift_status == "Not confirmed":
                    prefix = prefix_emodzi[2]
                elif gift_status == "Waiting":
                    prefix = prefix_emodzi[1]
                else:
                    prefix = prefix_emodzi[0]
            else:
                prefix =""
            username = base.get_user_data(user_id, ["username"])[0] if user_id is not None else "0"
            gifters_list.append(f"{prefix} {username}") if username else gifters_list.append(f"{prefix} Аноним")
        for i in range(4):
            if gifters_list[i] == " 0":
                gifters_list[i] = default_list[i]
        buttons = (
            InlineKeyboardButton(text=gifters_list[0], callback_data=f"gifter_{board_info[1]}_{board_info[2]}"),
            InlineKeyboardButton(text=gifters_list[1], callback_data=f"gifter_{board_info[1]}_{board_info[3]}"),
            InlineKeyboardButton(text=gifters_list[2], callback_data=f"gifter_{board_info[1]}_{board_info[4]}"),
            InlineKeyboardButton(text=gifters_list[3], callback_data=f"gifter_{board_info[1]}_{board_info[5]}"),
        )
        self.row(buttons[0],buttons[2])
        self.row(buttons[1],buttons[3])
        self.row(global_back_button(f"my_board_{board_info[0][-1]}"))
        return self.row(global_back_main_menu_button())

    def gifter_data(self, board_id: str) -> InlineKeyboardMarkup:
        self.row(global_back_button(f"board_gifters_{board_id}"))
        return self.row(global_back_main_menu_button())




