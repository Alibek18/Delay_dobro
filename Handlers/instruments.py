from aiogram import types, Dispatcher




async def instruments(callback: types.CallbackQuery):
    await callback.answer("Скоро будет доступно!", show_alert=True)



def register_instruments_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(instruments, text="instruments")