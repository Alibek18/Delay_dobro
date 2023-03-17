from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot

from SQL.user_models import Database_user
from Messages.admin_panel_messages import Admin_Panel_Messages
from Keyboards.admin_panel_keyboards import AdminPanelKeyboards

msg = Admin_Panel_Messages()

class AdminPanelFSM(StatesGroup):
    ask_user_id = State()
    ask_father_id = State()

async def admin_functions_keyboard(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = AdminPanelKeyboards()
    await bot.edit_message_text(msg.admin_panel, user_id, msg_id, reply_markup=kb.admin_panel(), parse_mode = "HTML")

async def change_father_id_ask_user_id(callback: types.CallbackQuery, state: FSMContext):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = AdminPanelKeyboards()
    await bot.edit_message_text(msg.change_father_id_ask_user_id, user_id, msg_id, reply_markup=kb.admpanel_back())
    await AdminPanelFSM.ask_user_id.set()
    await state.update_data(msg_to_edit=msg_id)

async def find_or_not_user(message: types.Message, state: FSMContext):
    state_data, user_id, base = await state.get_data(), message.from_user.id, Database_user()
    msg_id = state_data["msg_to_edit"]
    try: await message.delete()
    except: pass
    if message.text.isdigit():
        user_id_for_find = int(message.text)
        if not base.is_new_user(user_id_for_find):
            kb = AdminPanelKeyboards()
            await bot.edit_message_text(msg.find_user(user_id_for_find, change=False), user_id, msg_id,
                                        reply_markup=kb.find_user_change_father_id())
            await state.update_data(user_id_for_change = user_id_for_find)
        else:
            kb = AdminPanelKeyboards()
            try: await bot.edit_message_text(msg.not_find_user, user_id, msg_id,
                                        reply_markup=kb.admpanel_back())
            except: pass
    else:
        kb = AdminPanelKeyboards()
        try: await bot.edit_message_text(msg.not_isdigit_id, user_id, msg_id,
                                    reply_markup=kb.admpanel_back())
        except: pass

async def ask_father_id(callback: types.CallbackQuery, state: FSMContext):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = AdminPanelKeyboards()
    await bot.edit_message_text(msg.ask_father_id, user_id, msg_id, reply_markup=kb.admpanel_back())
    await AdminPanelFSM.ask_father_id.set()
    await state.update_data(msg_to_edit=msg_id)

async def find_or_not_father_id(message: types.Message, state: FSMContext):
    state_data, user_id, base = await state.get_data(), message.from_user.id, Database_user()
    msg_id = state_data["msg_to_edit"]
    try: await message.delete()
    except: pass
    if message.text.isdigit():
        father_id_for_find = int(message.text)
        if not base.is_new_user(father_id_for_find):
            kb = AdminPanelKeyboards()
            user_id_for_change = state_data["user_id_for_change"]
            await bot.edit_message_text(msg.find_father(father_id_for_find, user_id_for_change), user_id, msg_id,
                                        reply_markup=kb.approve_user_change_father_id())
            await state.update_data(father_id_for_change=father_id_for_find)
        else:
            kb = AdminPanelKeyboards()
            await bot.edit_message_text(msg.not_find_user, user_id, msg_id,
                                        reply_markup=kb.admpanel_back())
    else:
        kb = AdminPanelKeyboards()
        await bot.edit_message_text(msg.not_isdigit_id, user_id, msg_id,
                                    reply_markup=kb.admpanel_back())

async def change_father_id(callback: types.CallbackQuery, state: FSMContext):
    user_id, msg_id, base, state_data = callback.from_user.id, callback.message.message_id, Database_user(), \
        await state.get_data()
    user_id_for_change, father_id_for_change = state_data["user_id_for_change"], state_data["father_id_for_change"]
    base.set_user_data(user_id_for_change, father_id=father_id_for_change)
    kb = AdminPanelKeyboards()
    await bot.edit_message_text(msg.find_user(user_id_for_change, change=True), user_id, msg_id,
                                reply_markup=kb.admpanel_back())



def register_admin_panel_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(admin_functions_keyboard, text="admin_panel", state="*")
    dp.register_callback_query_handler(change_father_id_ask_user_id, text="adm_change_father", state="*")
    dp.register_message_handler(find_or_not_user, state=AdminPanelFSM.ask_user_id)
    dp.register_callback_query_handler(ask_father_id, text="adm_ask_father_id", state=AdminPanelFSM.ask_user_id)
    dp.register_message_handler(find_or_not_father_id, state=AdminPanelFSM.ask_father_id)
    dp.register_callback_query_handler(change_father_id, state="*")