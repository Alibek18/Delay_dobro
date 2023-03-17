from aiogram import types, Dispatcher

from create_bot import bot
from Messages.main_menu_messages import MainMenuMessages
from Keyboards.main_menu_keyboard import MainMenuInlineKeyboards

msg = MainMenuMessages()

async def main_menu(callback: types.CallbackQuery):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = MainMenuInlineKeyboards()
    await bot.edit_message_text(msg.main_menu, user_id, msg_id, reply_markup=kb.main_menu(user_id), parse_mode="HTML")

async def deleteself(callback: types.CallbackQuery):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = MainMenuInlineKeyboards()
    try:
        await callback.message.delete()
    except:
        await bot.edit_message_text(msg.main_menu, user_id, msg_id, reply_markup=kb.main_menu(user_id),
                                    parse_mode="HTML")

def register_main_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(main_menu, text="main_menu")
    dp.register_callback_query_handler(deleteself, text="deleteself")