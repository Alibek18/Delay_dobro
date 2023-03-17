from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Keyboards.start_keyboards import UserStartInlineKeyboards, ask_contact_keyboard
from Keyboards.main_menu_keyboard import MainMenuInlineKeyboards
from Messages.start_messages import Start_Messages
from Messages.main_menu_messages import MainMenuMessages
from SQL.user_models import Database_user
from create_bot import bot

msg = Start_Messages()

# class StartFSM(StatesGroup):
#     ask_username = State()


async def start_message_ask_language(message: types.Message):
    try:
        await message.delete()
    except:
        pass
    base = Database_user()
    user_id = message.from_user.id
    if base.is_new_user(user_id):
        if message.get_args():
            father_ref_link = message.get_args()
            if base.is_referral_link_exists(father_ref_link):
                ref_link = await get_start_link(user_id, encode=True)
                father_id = base.find_father(father_ref_link)
                base.create_new_user(user_id, ref_link.split('=')[1], father_id)
                kb = UserStartInlineKeyboards()
                start_msg = await bot.send_message(user_id, msg.ask_country,
                                                   reply_markup=kb.ask_countries(), parse_mode="HTML")
                try:
                    await bot.delete_message(user_id, start_msg.message_id - 2)
                except:
                    pass
            else:
                start_msg = await bot.send_message(user_id, msg.bad_deep_link)
                try:
                    await bot.delete_message(user_id, start_msg.message_id - 2)
                except:
                    pass
        else:
            start_msg = await bot.send_message(user_id, msg.no_deep_link)
            try:
                await bot.delete_message(user_id, start_msg.message_id - 2)
            except:
                pass
    else:
        kb = MainMenuInlineKeyboards()
        await bot.send_message(user_id, MainMenuMessages().main_menu, reply_markup=kb.main_menu(user_id),
                               parse_mode='HTML')

async def write_country_and_ask_subscribe(callback: types.CallbackQuery):
    user_id, msg_id, base, country = callback.from_user.id, callback.message.message_id, Database_user(), \
        callback.data.split('_')[1]
    base.set_user_data(user_id, country=country)
    kb = UserStartInlineKeyboards()
    await bot.edit_message_text(msg.start_message_ask_subscribe, user_id, msg_id,
                                reply_markup=kb.ask_subscribes(country), parse_mode="HTML")

async def check_subscribe_and_ask_contact(callback: types.CallbackQuery):
    await callback.answer()
    user_id, msg_id, chat_id_for_all, channel_id, subscribe_for_all, subscribe_country, subscribe_channel = \
        callback.from_user.id, callback.message.message_id, -1001826992179, -1001780434562, False, False, False
    language = Database_user().get_user_data(user_id, ["country"])[0]
    country_ids = {
        "RU": -1001770363847,
        "UZ": -1001650126779,
        "UA": -1001541736003, #0
        "BY": -1001541736003, #0
        "KG": -1001541736003, #0
        "KZ": -1001541736003,
        "TJ": -1001541736003, #0
        "TM": -1001541736003, #0
        "TR": -1001541736003 #0
    }
    try:
        chat_member = await bot.get_chat_member(chat_id_for_all, user_id)
        print(f"chat_id_for_all: {chat_member}")
        subscribe_for_all = True if chat_member.status != types.ChatMemberStatus.LEFT and chat_member.status != \
                            types.ChatMemberStatus.KICKED else False
    except: pass
    try:
        chat_member = await bot.get_chat_member(channel_id, user_id)
        print(f"channel: {chat_member}")
        subscribe_channel = True if chat_member.status != types.ChatMemberStatus.LEFT and chat_member.status != \
                            types.ChatMemberStatus.KICKED else False
    except: pass
    try:
        chat_member = await bot.get_chat_member(country_ids[language], user_id)
        print(f"country: {chat_member}")
        subscribe_country = True if chat_member.status != types.ChatMemberStatus.LEFT and chat_member.status != \
                            types.ChatMemberStatus.KICKED else False
    except: pass
    if subscribe_for_all and subscribe_country and subscribe_channel:
        kb = ask_contact_keyboard()
        try:
            await callback.message.delete()
        except:
            pass
        await bot.send_message(user_id, msg.ask_contact, reply_markup=kb, parse_mode="HTML")
    else:
        kb = UserStartInlineKeyboards()
        try:
            await bot.edit_message_text(msg.retry_subscribe, user_id, msg_id, reply_markup=kb.ask_subscribes(language),
                                        parse_mode="HTML")
        except: pass


async def write_contact_and_ask_rules(message: types.Message):
    user_id, base = message.from_user.id, Database_user()
    await message.delete()
    try:
        await bot.delete_message(user_id, message.message_id - 1)
    except:
        pass
    base.set_user_data(user_id, user_full_name=message.contact.full_name, user_phone=message.contact.phone_number,
                       username=message.from_user.username)
    kb = UserStartInlineKeyboards()
    await bot.send_message(user_id, msg.rules, reply_markup=kb.rules(), parse_mode="HTML")


async def ask_username_or_main_menu(callback: types.CallbackQuery):
    user_id, msg_id, base = callback.from_user.id, callback.message.message_id, Database_user()
    username = callback.from_user.username
    if username is None:
        await callback.answer("Добавь Telegram username!", show_alert=True)
        kb = UserStartInlineKeyboards()
        try:
            await bot.edit_message_text(msg.no_username, user_id, msg_id, reply_markup=kb.check_username(),
                                    parse_mode="HTML")
        except: pass
    else:
        base.set_user_data(user_id, username=username)
        kb = MainMenuInlineKeyboards()
        await bot.edit_message_text(MainMenuMessages().main_menu, user_id, msg_id, reply_markup=kb.main_menu(user_id),
                                    parse_mode="HTML")



def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_message_ask_language, commands=["start"])
    dp.register_callback_query_handler(write_country_and_ask_subscribe, Text(startswith="country"))
    dp.register_callback_query_handler(check_subscribe_and_ask_contact, text="confirm_subscribe")
    dp.register_message_handler(write_contact_and_ask_rules, content_types=types.ContentType.CONTACT)
    dp.register_callback_query_handler(ask_username_or_main_menu, text="check_username")


