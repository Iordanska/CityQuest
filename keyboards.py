from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_tip_kb(user):
    if user['is_tip'] and user['points'] >= 5:

        kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[InlineKeyboardButton(text='Подcказка (-5)',
                                                                                      callback_data='get_tip')]])
        return kb
    else:
        return None
