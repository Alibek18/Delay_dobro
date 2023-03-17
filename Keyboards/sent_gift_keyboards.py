from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Keyboards.GlobalKeyboards import global_back_button, global_back_main_menu_button, global_notification_button

class SentGiftKeyboards(InlineKeyboardMarkup):

    def approve_sent(self, board_index, board_id) -> InlineKeyboardMarkup:
        self.row_width = 2
        self.insert(InlineKeyboardButton(text="✅ Да", callback_data=f"appsentgift_{board_index}_{board_id}"))
        return self.insert(InlineKeyboardButton(text="⛔️ Нет", callback_data=f"my_board_{board_index}"))


    def confirm_sent(self, board_index) -> InlineKeyboardMarkup:
        self.row(global_back_button(f"my_board_{board_index}"))
        return self.row(global_back_main_menu_button())

    def ask_about_gift(self, operation_id: int) -> InlineKeyboardMarkup:
        buttons = (
            InlineKeyboardButton(text="✅ Да, я получил подарок", callback_data=f"gift_confirm_{operation_id}"),
            InlineKeyboardButton(text="❌ Нет, я не получил подарок", callback_data=f"gift_escape_{operation_id}")
        )
        self.row(buttons[0])
        return self.row(buttons[1])

    def notification(self):
        return self.row(global_notification_button())
