from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


class UserStartInlineKeyboards(InlineKeyboardMarkup):

    def ask_subscribes(self, language: str) -> InlineKeyboardMarkup:
        tg_groups = {
            "RU": "https://t.me/CHAT_MIR_PADORKOV_2_RF",
            "UZ": "https://t.me/MIR_PODARKOV_2_UZB",
            "UA": "-",
            "BY": "-",
            "KG": "-",
            "KZ": "https://t.me/CHAT_MIR_PODARKOV_2_KZ",
            "TJ": "-",
            "TM": "-",
            "TR": "-"
        }
        buttons = (
            InlineKeyboardButton(text="Наша Телеграм группа Отзывы", url="https://t.me/Mir_Podarkov_comment"),
            InlineKeyboardButton(text="Наш Телеграм канал отчет подарков", url="https://t.me/Mir_Podarkov_otchet"),
            InlineKeyboardButton(text="Наш Ютуб Канал", url="https://youtube.com/@mir_podarkov"),
            InlineKeyboardButton(text="Наш Инстаграм",
                                 url="http://instagram.com/mir_podarkov2023"),
            InlineKeyboardButton(text="👌 Я подписался!", callback_data='confirm_subscribe')
        )
        if tg_groups[language] != "-":
            self.row(InlineKeyboardButton(text="Телеграм группа Мир Подарков", url=f"{tg_groups[language]}"))
        for button in buttons:
            self.row(button)
        return self


    def ask_countries(self):
        # self.row_width = 2
        buttons = (
            InlineKeyboardButton(text="🇷🇺 Россия", callback_data="country_RU"),
            InlineKeyboardButton(text="🇺🇿 Узбекистан", callback_data="country_UZ"),
            InlineKeyboardButton(text="🇺🇦 Украина", callback_data="country_UA"),
            InlineKeyboardButton(text="🇧🇾 Беларусь", callback_data="country_BY"),
            InlineKeyboardButton(text="🇰🇬 Киргизия", callback_data="country_KG"),
            InlineKeyboardButton(text="🇰🇿 Казахстан", callback_data="country_KZ"),
            InlineKeyboardButton(text="🇹🇯 Таджикистан", callback_data="country_TJ"),
            InlineKeyboardButton(text="🇹🇲 Туркменистан", callback_data="country_TM"),
            InlineKeyboardButton(text="🇹🇷 Türkiye", callback_data="country_TR")
        )
        # for button in buttons:
        #     self.insert(button)
        self.row(buttons[0])
        self.row(buttons[1])
        self.row(buttons[5])
        return self

    def rules(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(text="🤝 Я принимаю условия", callback_data="check_username")
        return self.row(button)

    def check_username(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(text="✅ Я добавил Telegram username", callback_data="check_username")
        return self.row(button)


def ask_contact_keyboard() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text="‼️ ОТПРАВИТЬ НОМЕР ТЕЛЕФОНА 👈", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return keyboard.add(button)


