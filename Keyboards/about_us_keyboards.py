from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Keyboards.GlobalKeyboards import global_back_main_menu_button


class AboutUsInlineKeyboards(InlineKeyboardMarkup):

    def about_us(self, boards: bool = False, statuses: bool = False) -> InlineKeyboardMarkup:
        boards_text = "🔘 💵 Доски" if boards else "💵 Доски"
        statuses_text = "🔘 🥇 Статусы" if statuses else "🥇 Статусы"
        buttons = (
            InlineKeyboardButton(text=boards_text, callback_data="about_us_boards"),
            InlineKeyboardButton(text=statuses_text, callback_data="statuses")
        )
        self.row(buttons[0], buttons[1])
        return self.row(global_back_main_menu_button())
