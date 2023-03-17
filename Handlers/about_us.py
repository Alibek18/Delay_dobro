from aiogram import types, Dispatcher

from Keyboards.about_us_keyboards import AboutUsInlineKeyboards
from Messages.about_us_messages import AboutUsMessages
from create_bot import bot

msg = AboutUsMessages()


async def about_us(callback: types.CallbackQuery):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = AboutUsInlineKeyboards()
    await bot.edit_message_text(msg.about_us, user_id, msg_id, reply_markup=kb.about_us(), parse_mode="HTML")


async def about_us_boards(callback: types.CallbackQuery):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = AboutUsInlineKeyboards()
    try:
        await bot.edit_message_text(msg.about_us_boards(user_id), user_id, msg_id,
                                    reply_markup=kb.about_us(boards=True), parse_mode="HTML")
    except:
        pass


async def about_us_statuses(callback: types.CallbackQuery):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = AboutUsInlineKeyboards()
    try:
        await bot.edit_message_text(msg.about_us_statuses, user_id, msg_id, reply_markup=kb.about_us(statuses=True),
                                    parse_mode="HTML")
    except:
        pass


def register_about_us_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(about_us, text="about_us")
    dp.register_callback_query_handler(about_us_boards, text="about_us_boards")
    dp.register_callback_query_handler(about_us_statuses, text="statuses")
