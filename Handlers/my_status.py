from aiogram import types, Dispatcher

from create_bot import bot
from Keyboards.my_status_keyboards import MyStatusKeyboards
from Messages.my_status_messages import MyStatusMessages

msg = MyStatusMessages()

async def my_status(callback: types.CallbackQuery):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = MyStatusKeyboards()
    await bot.edit_message_text(msg.my_status(user_id), user_id, msg_id, reply_markup=kb.my_status(), parse_mode="HTML")

def register_my_status_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(my_status, text="my_status")