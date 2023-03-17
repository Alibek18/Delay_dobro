import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from SQL.board_models import Database_boards
from SQL.boards_time_models import Database_boards_time
from SQL.operations_models import Database_operations
from SQL.user_models import Database_user
from create_bot import bot
from Messages.sent_gift_messages import SentGiftMessages
from Keyboards.sent_gift_keyboards import SentGiftKeyboards
from settings import START_KING

msg = SentGiftMessages()

async def sent_gift_approve(callback: types.CallbackQuery):
    user_id, msg_id, callback_data = callback.from_user.id, callback.message.message_id, callback.data.split("_")
    board_index, board_id = callback_data[1], callback_data[2]
    kb = SentGiftKeyboards()
    await bot.edit_message_text(msg.approve_sent, user_id, msg_id,
                                reply_markup=kb.approve_sent(board_index, board_id), parse_mode="HTML")

async def sent_gift(callback: types.CallbackQuery):
    user_id, msg_id, callback_data = callback.from_user.id, callback.message.message_id, callback.data.split("_")
    summ_dict = {
        "RU": ("100", "200", "400", "800", "1600", "3200", "6400", "12000", "24000", "48000", "100000",
               "200000", "400000", "800000", "1600000", "3200000"),
        "UZ": ("10000", "20000", "40000", "80000", "160000", "320000", "640000", "1200000", "2400000",
               "4800000", "10000000", "20000000", "40000000", "80000000", "160000000", "320000000"),
        "BY": ("5", "10", "20", "40", "80", "160", "320", "640", "1200", "2400", "4800", "10000", "20000",
               "40000", "80000", "160000"),
        "KG": ("100", "200", "400", "800", "1600", "3200", "6400", "12000", "24000", "48000", "100000",
               "200000", "400000", "800000", "1600000", "3200000"),
        "KZ": ("500", "1000", "2000", "4000", "8000", "16000", "32000", "64000", "120000", "240000",
               "480000", "1000000", "2000000", "4000000", "8000000", "16000000"),
        "TJ": ("10", "20", "40", "80", "160", "320", "640", "1200", "2400", "4800",
               "10000", "20000", "40000", "80000", "160000", "320000"),
        "TM": ("5", "10", "20", "40", "80", "160", "320", "640", "1200", "2400", "4800", "10000", "20000",
               "40000", "80000", "160000"),
        "TR": ("20", "40", "80", "160", "320", "640", "1200", "2400", "4800", "10000", "20000", "40000",
               "80000", "160000", "320000", "640000"),
        "UA": ("50", "100", "200", "400", "800", "1600", "3200", "6400", "12000", "24000", "48000",
               "100000", "200000", "400000", "800000", "1600000")
    }
    currency = {
        "RU": "РУБ|RUB", "UZ": "Сум", "BY": "РУБ|BYN", "KG": "Сом", "KZ": "Тенге", "TJ": "Сомони", "TM": "Манат",
        "TR": "Лира", "UA": "Гривна"
    }
    board_index, board_id = callback_data[1], callback_data[2]
    base, b_base, o_base, bt_base = Database_user(), Database_boards(), Database_operations(), Database_boards_time()
    king_id = b_base.get_board_data(board_id, ["uid", "king"])[1]
    language = base.get_user_data(user_id, ["country"])[0]
    amount = int(summ_dict[language][int(board_index)])
    time_now = datetime.datetime.now()
    operation_id = o_base.create_new_operation(board_id, board_index, user_id, king_id, amount, time_now)
    bt_base.delete(board_id, user_id)
    kb = SentGiftKeyboards()
    await bot.edit_message_text(msg.confirm_sent_gift, user_id, msg_id, reply_markup=kb.confirm_sent(board_index),
                                parse_mode="HTML")
    try:
        kbs = SentGiftKeyboards()
        await bot.send_message(king_id, msg.ask_about_gift(user_id, board_index),
                               reply_markup=kbs.ask_about_gift(operation_id))
    except:
        pass

async def gift_confirm_or_escape(callback: types.CallbackQuery):
    king_id, msg_id, todo, operation_id, o_base, base, b_base, bt_base = callback.from_user.id, \
        callback.message.message_id, callback.data.split("_")[-2], int(callback.data.split("_")[-1]), \
        Database_operations(), Database_user(), Database_boards(), Database_boards_time()
    try: await callback.message.delete()
    except: await callback.answer()
    if todo == "confirm":
        o_base.set_operation_data(operation_id, approve=True)
        kb, oper_data = SentGiftKeyboards(), o_base.get_operation_data(operation_id)
        board_index, sender_id, board_id = int(oper_data[2]), oper_data[3], oper_data[1]
        bt_base.delete(board_id, sender_id)
        is_activated, father_id = base.get_user_data(sender_id, ["activated", "father_id"])
        language = base.get_user_data(sender_id, ["country"])[0]

        channel_id = -1001780434562 #отправка сообщения в канал
        try:
            await bot.send_message(channel_id, msg.channel_message(oper_data[2], oper_data[5], language))
        except: pass

        if not is_activated:
            base.set_user_data(sender_id, activated=True)
            kb = SentGiftKeyboards()
            try: await bot.send_message(sender_id, msg.activated, reply_markup=kb.notification(), parse_mode="HTML")
            except: pass

        sender_boards_access = base.get_boards_access(sender_id)[1:]
        if(len(set(sender_boards_access))) == 2:
            next_board_index = f"board{board_index + 1}"
            base.set_boards_access(sender_id, next_board_index)

        # father_boards_access = base.get_boards_access(father_id)[1:]
        # if len(set(father_boards_access)) == 2:
        #     next_board_index = f"board{board_index+1}"
        #     base.set_boards_access(father_id, next_board_index)
        kb = SentGiftKeyboards()
        try: await bot.send_message(father_id, msg.kvalification(sender_id, board_index),
                                    reply_markup=kb.notification(), parse_mode="HTML")
        except: pass

        try:
            kb = SentGiftKeyboards()
            await bot.send_message(sender_id, msg.gift_received(oper_data), reply_markup=kb.notification(),
                                   parse_mode="HTML")
        except: pass

        sender_place = b_base.find_on_board(sender_id, str(board_index), language)[1]
        approved_board_sender_id = [i[0] for i in o_base.get_board_operations(oper_data[1])]
        gifter1, gifter2, gifter3, gifter4, builder1, builder2 = \
            b_base.get_board_data(oper_data[1],["uid","gifter1","gifter2","gifter3", "gifter4", "builder1",
                                                "builder2"])[1:]
        if len(approved_board_sender_id) == 4:
            b_base.set_board_data(str(board_index), oper_data[1], active=False)
            try:
                kb = SentGiftKeyboards()
                await bot.send_message(king_id, msg.close_board(oper_data[1]), reply_markup=kb.notification(),
                                       parse_mode="HTML")
            except: pass

        if sender_place in ["gifter1", "gifter2"]:
            if gifter1 in approved_board_sender_id and gifter2 in approved_board_sender_id:
                new_board = b_base.create_new_board(board_index, gifter1, gifter2, builder1, language)
                for builder in [gifter1, gifter2]:
                    kb = SentGiftKeyboards()
                    try: await bot.send_message(builder, msg.new_board_builder_notification(board_index, new_board),
                                                reply_markup=kb.notification(), parse_mode="HTML")
                    except:pass
                kb = SentGiftKeyboards()
                try: await bot.send_message(builder1, msg.new_board_king_notification(board_index, new_board),
                                           reply_markup=kb.notification(), parse_mode="HTML")
                except: pass
        if sender_place in ["gifter3", "gifter4"]:
            if gifter3 in approved_board_sender_id and gifter4 in approved_board_sender_id:
                new_board = b_base.create_new_board(board_index, gifter3, gifter4, builder2, language)
                for builder in [gifter1, gifter2]:
                    kb = SentGiftKeyboards()
                    try: await bot.send_message(builder, msg.new_board_builder_notification(board_index, new_board),
                                                reply_markup=kb.notification(), parse_mode="HTML")
                    except:pass
                kb = SentGiftKeyboards()
                try: await bot.send_message(builder1, msg.new_board_king_notification(board_index, new_board),
                                           reply_markup=kb.notification(), parse_mode="HTML")
                except: pass



    elif todo == "escape":
        o_base.set_operation_data(operation_id, approve=False)
        try:
            kb, oper_data = SentGiftKeyboards(), o_base.get_operation_data(operation_id)
            await bot.send_message(oper_data[3], msg.gift_escape(oper_data), reply_markup=kb.notification(),
                                   parse_mode="HTML")
        except: pass





def register_sent_gift_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(sent_gift_approve, Text(startswith="sentgift_"))
    dp.register_callback_query_handler(sent_gift, Text(startswith="appsentgift_"))
    dp.register_callback_query_handler(gift_confirm_or_escape, Text(startswith="gift_"))