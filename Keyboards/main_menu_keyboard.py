from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import admin_list

class MainMenuInlineKeyboards(InlineKeyboardMarkup):
    def main_menu(self, user_id: int):
        self.row_width = 2
        buttons = (
            InlineKeyboardButton(text="💰 Мои доски", callback_data="my_boards"),
            InlineKeyboardButton(text="🎉 О нас", callback_data="about_us"),
            InlineKeyboardButton(text="👥 Приглашение", callback_data="referral"),
            InlineKeyboardButton(text="👏 Мой статус", callback_data="my_status"),
            InlineKeyboardButton(text="⚙️ Инструменты", callback_data="instruments")
        )
        self.row(buttons[0])
        self.row(buttons[1], buttons[2])
        self.row(buttons[3], buttons[4])
        return self if user_id not in admin_list \
            else self.row(InlineKeyboardButton(text="💎 Панель администратора", callback_data="admin_panel"))
