from aiogram import types, Dispatcher

from create_bot import bot
from Keyboards.referral_keyboards import ReferralKeyboards
from Messages.referral_messages import ReferralMessages

msg = ReferralMessages()

async def referral(callback: types.CallbackQuery):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = ReferralKeyboards()
    await bot.edit_message_text(msg.referral(user_id), user_id, msg_id, reply_markup=kb.referral(),
                                parse_mode="Markdown")

def register_referral_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(referral, text="referral")