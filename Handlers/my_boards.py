from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from Keyboards.my_boards_keyboards import MyBoardsInlineKeyboards
from Keyboards.sent_gift_keyboards import SentGiftKeyboards
from Messages.my_boards_messages import MyBoardsMessages
from SQL.board_models import Database_boards
from SQL.boards_time_models import Database_boards_time
from SQL.user_models import Database_user
from create_bot import bot
from settings import START_KING, START_BUILDER1, START_BUILDER2

msg = MyBoardsMessages()


async def my_boards(callback: types.CallbackQuery):
    user_id, msg_id = callback.from_user.id, callback.message.message_id
    kb = MyBoardsInlineKeyboards()
    await bot.edit_message_text(msg.my_boards(user_id), user_id, msg_id, reply_markup=kb.my_boards(user_id),
                                parse_mode="HTML")


async def accept_board(callback: types.CallbackQuery):
    user_id, msg_id, board_index, base, b_base = callback.from_user.id, callback.message.message_id, \
        int(callback.data.split("_")[-1]), Database_user(), Database_boards()
    language = base.get_user_data(user_id, ["country"])[0]
    on_board = b_base.find_on_board(user_id, str(board_index), language)
    accept = base.get_boards_access(user_id)[board_index + 1]
    if accept:
        if on_board is None or not on_board:
            kb = MyBoardsInlineKeyboards()
            await bot.edit_message_text(msg.accept_board(user_id), user_id, msg_id,
                                        reply_markup=kb.accept_board(board_index), parse_mode="HTML")
        else:
            kb = MyBoardsInlineKeyboards()
            await bot.edit_message_text(msg.board(user_id, on_board[0], on_board[1]), user_id, msg_id,
                                        reply_markup=kb.board(on_board[0], on_board[1]), parse_mode="HTML")
    else:
        kb = MyBoardsInlineKeyboards()
        await bot.edit_message_text(msg.no_access_board, user_id, msg_id, reply_markup=kb.no_access_board(),
                                    parse_mode="HTML")


async def board(callback: types.CallbackQuery):
    user_id, msg_id, b_base, board_index, base, bt_base = callback.from_user.id, callback.message.message_id, \
        Database_boards(), callback.data.split("_")[-1], Database_user(), Database_boards_time()
    father_on_board = None
    user_id_for_find = user_id
    gifter_places = [0, 0, 0, 0]
    boards_in_system = b_base.count_boards_in_system(board_index)
    language = base.get_user_data(user_id, ["country"])[0]
    while (not father_on_board or father_on_board is None or gifter_places.count(None) == 0) and boards_in_system > 0:
        father_id = base.get_user_data(user_id_for_find, ["father_id"])[0]
        father_on_board = b_base.find_on_board(father_id, board_index, language)
        if father_on_board:
            places = b_base.check_free_gifters_places(board_index, father_on_board[0], father_on_board[1])
            gifter_places = places if places else (None, None)
        user_id_for_find = father_id
        boards_in_system -= 1
    if boards_in_system != 0:
        if father_on_board[1] == 'king':
            if gifter_places[0] is None and gifter_places[1] is None:
                b_base.set_board_data(board_index, father_on_board[0], gifter1=user_id)
                bt_base.set_new_board_time(father_on_board[0], user_id)
            elif gifter_places[2] is None and gifter_places[3] is None:
                b_base.set_board_data(board_index, father_on_board[0], gifter3=user_id)
                bt_base.set_new_board_time(father_on_board[0], user_id)
            else:
                free_place = gifter_places.index(None)
                if free_place == 0:
                    b_base.set_board_data(board_index, father_on_board[0], gifter1=user_id)
                    bt_base.set_new_board_time(father_on_board[0], user_id)
                elif free_place == 1:
                    b_base.set_board_data(board_index, father_on_board[0], gifter2=user_id)
                    bt_base.set_new_board_time(father_on_board[0], user_id)
                elif free_place == 2:
                    b_base.set_board_data(board_index, father_on_board[0], gifter3=user_id)
                    bt_base.set_new_board_time(father_on_board[0], user_id)
                elif free_place == 3:
                    b_base.set_board_data(board_index, father_on_board[0], gifter4=user_id)
                    bt_base.set_new_board_time(father_on_board[0], user_id)
        elif father_on_board[1] == "builder1":
            if gifter_places[0] is None:
                b_base.set_board_data(board_index, father_on_board[0], gifter1=user_id)
                bt_base.set_new_board_time(father_on_board[0], user_id)
            elif gifter_places[1] is None:
                b_base.set_board_data(board_index, father_on_board[0], gifter2=user_id)
                bt_base.set_new_board_time(father_on_board[0], user_id)
        elif father_on_board[1] == "builder2":
            if gifter_places[0] is None:
                b_base.set_board_data(board_index, father_on_board[0], gifter3=user_id)
                bt_base.set_new_board_time(father_on_board[0], user_id)
            elif gifter_places[1] is None:
                b_base.set_board_data(board_index, father_on_board[0], gifter4=user_id)
                bt_base.set_new_board_time(father_on_board[0], user_id)
        elif father_on_board[1] == "gifter1":
            b_base.set_board_data(board_index, father_on_board[0], gifter2=user_id)
            bt_base.set_new_board_time(father_on_board[0], user_id)
        elif father_on_board[1] == "gifter2":
            b_base.set_board_data(board_index, father_on_board[0], gifter1=user_id)
            bt_base.set_new_board_time(father_on_board[0], user_id)
        elif father_on_board[1] == "gifter3":
            b_base.set_board_data(board_index, father_on_board[0], gifter4=user_id)
            bt_base.set_new_board_time(father_on_board[0], user_id)
        elif father_on_board[1] == "gifter4":
            b_base.set_board_data(board_index, father_on_board[0], gifter3=user_id)
            bt_base.set_new_board_time(father_on_board[0], user_id)
    else:
        board_id = b_base.create_new_board(int(board_index), START_BUILDER1, START_BUILDER2, START_KING, language)
        b_base.set_board_data(board_index, board_id, gifter1=user_id)
        bt_base.set_new_board_time(father_on_board[0], user_id)

    on_board = b_base.find_on_board(user_id, str(board_index), language)
    kb = MyBoardsInlineKeyboards()
    await bot.edit_message_text(msg.board(user_id, on_board[0], on_board[1]), user_id, msg_id,
                                reply_markup=kb.board(on_board[0], on_board[1]), parse_mode="HTML")
    board_info = b_base.get_board_data(on_board[0], ["uid","gifter1","gifter2","gifter3","gifter4"])
    for gifter_id in board_info[1:]:
        if gifter_id is not None and gifter_id != user_id:
            kb = SentGiftKeyboards()
            try: await bot.send_message(gifter_id, msg.gifter_added(user_id, board_index, on_board[0]),
                                        reply_markup=kb.notification(), parse_mode="HTML")
            except: pass


async def king_data(callback: types.CallbackQuery):
    user_id, msg_id, board_id, b_base = callback.from_user.id, callback.message.message_id, \
        callback.data.split("_")[-1], Database_boards()
    kb = MyBoardsInlineKeyboards()
    board_index = b_base.find_board(board_id)[0][-1]
    await bot.edit_message_text(msg.king_data(board_id, user_id), user_id, msg_id,
                                reply_markup=kb.king_data(board_id, board_index, user_id), parse_mode="HTML")


async def board_family(callback: types.CallbackQuery):
    user_id, msg_id, board_id, b_base = callback.from_user.id, callback.message.message_id, \
        callback.data.split("_")[-1], Database_boards()
    board_info = b_base.find_board(board_id)
    kb = MyBoardsInlineKeyboards()
    await bot.edit_message_text(msg.board_family(board_info), user_id, msg_id, reply_markup=kb.board_family(board_info),
                                parse_mode="HTML")


async def board_gifters(callback: types.CallbackQuery):
    user_id, msg_id, board_id, b_base = callback.from_user.id, callback.message.message_id, \
        callback.data.split("_")[-1], Database_boards()
    board_info = b_base.find_board(board_id)
    kb = MyBoardsInlineKeyboards()
    await bot.edit_message_text(msg.board_gifters, user_id, msg_id, reply_markup=kb.board_gifters(board_info),
                                parse_mode="HTML")


async def gifter_data(callback: types.CallbackQuery):
    user_id, msg_id, gifter_id, board_id = callback.from_user.id, callback.message.message_id, \
        callback.data.split("_")[-1], callback.data.split("_")[-2]
    kb = MyBoardsInlineKeyboards()
    if gifter_id != "None":
        await bot.edit_message_text(msg.gifter_data(gifter_id, board_id), user_id, msg_id,
                                    reply_markup=kb.gifter_data(board_id), parse_mode="HTML")
    else:
        await callback.answer()


def register_my_boards_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(my_boards, text="my_boards")
    dp.register_callback_query_handler(accept_board, Text(startswith="my_board_"))
    dp.register_callback_query_handler(board, Text(startswith="accept_board_"))
    dp.register_callback_query_handler(king_data, Text(startswith="king_data_"))
    dp.register_callback_query_handler(board_family, Text(startswith="board_family_"))
    dp.register_callback_query_handler(board_gifters, Text(startswith="board_gifters_"))
    dp.register_callback_query_handler(gifter_data, Text(startswith="gifter_"))
