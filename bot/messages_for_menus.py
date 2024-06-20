from typing import Dict

HELPER = """
<b>/start</b> - <em>Запустить бота</em>
<b>/estimate</b> - <em>Оценить стоимость квартиры по параметрам</em>
<b>/help</b> - <em>Список команд</em>
<b>/about</b> - <em>Информация о боте</em>
"""

ABOUT = """
<b>БОТ ОЦЕНКИ</b>
<b>Для чего предназначен?</b> - <em>Данный бот предназначен для приблизительной оценки цены квартир в Санкт-Петербурге.</em>
<b>Как он устроен?</b> - <em>Актуальная информация собирается с открытых торговых площадок; на ее основе выполняется предсказание стоимости.</em>
<b>Нужна помощь?</b> - <em>Введите /help</em>
"""

START_ESTIMATION = """
На каждом шаге будет предложено ввести значение для параметра.\n
Чем больше параметров введено, тем точнее предсказанная цена.
Если что-то пошло не так, следует ввести /restart и начать заново.
"""

not_available_now = 'К сожалению, сервис на данный момент не доступен, попробуйте позже.'

print_command_text = {
    'help': HELPER,
    'about': ABOUT,
}

features_msg_text = {
    'address': 'Адрес квартиры',
    'rooms': 'Количество комнат',
    'total_area': 'Площадь квартиры (м2)',
    'stage': 'Этаж',
    'elevator': 'Есть ли лифт?',
    'largage_elevator': 'Есть ли грузовой лифт?',
}


def format_usr_input(data: Dict) -> str:
    """Форматирует собранные признаки в строку."""
    features_repr = '🏢 Введены следующие данные о квартире:🏢\n'
    for feature_name, cyr_name in features_msg_text.items():
        value = data[feature_name]
        if feature_name in {'largage_elevator', 'elevator'}:
            value = 'да' if value else 'нет'
        if feature_name == 'rooms':
            value = value if value else '0 (студия)'
        features_repr += f"{cyr_name} -> <b>{str(value).replace('.', ',')}</b>\n"
    return features_repr


def format_response_from_model(model_response: Dict[str, float]) -> str:
    """Форматирует ответ модели в строку."""
    m2_price = f"{model_response['m2_price'] / 1_000:.1f}".replace('.', ',')
    total_price = f"{model_response['total_price'] / 1_000_000:.1f}".replace('.', ',')
    return f"""\n⭐️Результаты оценки⭐️
Квадратный метр ≈ 😱<b>{m2_price} т.р./м2</b>😱
Общая стоимость ≈ 💲<b>{total_price} млн. рублей</b>💲.

👍Спасибо за использование нашего бота!👍
Продолжить? - нажмите ➡️ /estimate)
"""
