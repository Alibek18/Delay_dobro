from aiogram.types import InlineKeyboardMarkup

from Keyboards.GlobalKeyboards import global_back_main_menu_button


class ReferralKeyboards(InlineKeyboardMarkup):

    def referral(self):
        return self.row(global_back_main_menu_button())
