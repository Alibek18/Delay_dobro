from SQL.user_models import Database_user
from settings import BOT_ADDRESS

class ReferralMessages:

    @staticmethod
    def referral(user_id):
        ref_link, activated = Database_user().get_user_data(user_id, ["ref_link", "activated"])
        return f"✅ Ваша ссылка для привлечения участников:\n\n`{BOT_ADDRESS}?start={ref_link}`\n\n" \
               f"‼️ Нажмите на вашу ссылку и она будет автоматически скопирована! Отправьте её вашему другу и " \
               f"получайте подарки вместе! 🚀" if activated \
            else "👉 Вам нужно активировать реферальную ссылку.\n\n" \
                 "✅ Для этого отправьте подарок и получите подтверждение.\n\n" \
                 "❕ После подтверждения реферальная ссылка появится в данном разделе."


