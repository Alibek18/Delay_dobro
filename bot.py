from aiogram.utils import executor

from create_bot import dp

import SQL
import Handlers

async def on_startup(_):
    SQL.user_models.Database_user().create_table()
    print('User tables created')
    SQL.board_models.Database_boards().create_table()
    print('Board tables created')
    SQL.operations_models.Database_operations().create_table()
    print('Operation tables created')
    print('Bot Online')

Handlers.start_branch.register_start_handlers(dp)
Handlers.main_menu.register_main_menu_handlers(dp)
Handlers.about_us.register_about_us_handlers(dp)
Handlers.my_boards.register_my_boards_handlers(dp)
Handlers.referral.register_referral_handlers(dp)
Handlers.my_status.register_my_status_handlers(dp)
Handlers.sent_gift.register_sent_gift_handlers(dp)
Handlers.instruments.register_instruments_handlers(dp)
Handlers.admin_panel.register_admin_panel_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)