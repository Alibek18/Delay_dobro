from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Keyboards.GlobalKeyboards import global_back_main_menu_button, global_back_button

class AdminPanelKeyboards(InlineKeyboardMarkup):

    def admin_panel(self):
        button = InlineKeyboardButton(text="Заменить наставника", callback_data="adm_change_father")
        self.row(button)
        return self.row(global_back_main_menu_button())

    def admpanel_back(self):
        return self.row(global_back_button("admin_panel"))

    def find_user_change_father_id(self):
        button = InlineKeyboardButton(text="Заменить наставника", callback_data="adm_ask_father_id")
        self.row(button)
        return self.row(global_back_button("admin_panel"))

    def approve_user_change_father_id(self):
        button = InlineKeyboardButton(text="Да, все верно! Заменить!", callback_data="adm_approve_change_father_id")
        self.row(button)
        return self.row(global_back_button("admin_panel"))
