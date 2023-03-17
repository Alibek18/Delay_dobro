from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def back_to_main_menu_with_custom_back(callback_data):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data=callback_data))
    return keyboard.row(InlineKeyboardButton(text="⭐️ Главное меню ⭐️", callback_data="main_menu"))


def global_back_button(callback_data):
    return InlineKeyboardButton(text="🔙 Назад", callback_data=callback_data)

def global_back_main_menu_button():
    return InlineKeyboardButton(text="⭐️ Главное меню ⭐️", callback_data="main_menu")

def global_notification_button():
    return InlineKeyboardButton(text="👌 Ок", callback_data="deleteself")
