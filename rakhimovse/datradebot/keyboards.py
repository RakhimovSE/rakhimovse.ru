from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def _get_inline_keyboard_markup(mapping):
    inline_keyboard = []
    for row in mapping:
        inline_row = [InlineKeyboardButton(text=text, callback_data=data) for data, text in row]
        inline_keyboard.append(inline_row)
    return InlineKeyboardMarkup(inline_keyboard)


def get_main_menu_keyboard():
    mapping = [
        [
            ('about_us', 'О нас'),
            ('payment:menu', 'Стоимость'),
        ],
        [
            ('partner:menu', 'Партнёрство'),
            ('promo', 'Промокод'),
        ],
        [
            ('faq', 'FAQ'),
            ('settings:menu', 'Настройки'),
        ],
    ]
    return _get_inline_keyboard_markup(mapping)


def get_payment_menu_keyboard():
    mapping = [
        [
            ('exchange_info', 'Курсы валют'),
            ('subscription_info', 'О подписке'),
        ],
        [
            ('pay_1month', '1 месяц'),
            ('pay_6month', '6 месяцев'),
            ('pay_12month', '12 месяцев'),
        ],
        [
            ('main:menu', 'Назад'),
        ],
    ]
    return _get_inline_keyboard_markup(mapping)


def get_partner_menu_keyboard():
    mapping = [
        [
            ('partner_info', 'Условия и вознаграждения'),
        ],
        [
            ('become_partner', 'Стать партнёром'),
            ('ref_link', 'Реф. ссылка'),
        ],
        [
            ('wallet_info', 'Баланс'),
            ('main:menu', 'Назад'),
        ],
    ]
    return _get_inline_keyboard_markup(mapping)


def get_settings_menu_keyboard():
    mapping = [
        [
            ('set_ru', '🇷🇺 Русский'),
            ('set_en', '🇺🇸 English'),
        ],
        [
            ('main:menu', 'Назад'),
        ],
    ]
    return _get_inline_keyboard_markup(mapping)
