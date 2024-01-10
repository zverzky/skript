import requests
import json
import telebot

from bs4 import BeautifulSoup


TOKEN = ''
def get_data(url: str = 'https://www.cbr.ru/currency_base/daily/') -> dict[str, dict]:
    result = {}

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find('tbody')
    rows = table.find_all('tr')[1:]

    for key, row in enumerate(rows, start=1):
        digital_code, letter_code, units, currency, well = [i.text for i in row.find_all('td')]

        result[key] = {
            "Digital_code": digital_code,
            "Letter_code": letter_code,
            "units": units,
            "Currency": currency,
            "well": well
        }
    return result


def write_to_json(data: dict = get_data()):
    with open("Курс_Валют_ЦБ.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print("Все данные добавились")


def main_parsing():
    get_data()
    write_to_json()


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == '/start':
        main_parsing()
        bot.send_message(message.chat.id, f"Добрый день, {message.chat.username}.\nВведите порядковый номер "
                                          f"валюты \ Полное название валюты, информацию о которой хотите получить.")

        with open("Курс_Валют_ЦБ.json", 'r', encoding='utf-8') as file:
            table = json.load(file)

        msg = '\n'.join(f'{key}: {table[key]["Currency"]}' for key in table)
        bot.send_message(message.chat.id, msg)

    else:
        bot.send_message(message.chat.id, f"<b>Документация бота:</b>\n1. Бот в разработке\n"
                                          f"2. Бот в разработке\n"
                                          f"3. Бот в разработке", parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_dan(message):
    with open("Курс_Валют_ЦБ.json", 'r', encoding='utf-8') as file:
        table = json.load(file)
    msg = ''.join(f'{table[key]["Currency"]}' for key in table)

    for key in table:
        if key == message.text:
            bot.send_message(message.chat.id, f'Цифровой код: {table[key]["Digital_code"]}.\n'
                                              f'Буквенный код: {table[key]["Letter_code"]}.\n'
                                              f'Количество: {table[key]["units"]}.\n'
                                              f'Наименование: {table[key]["Currency"]}.\n'
                                              f'Курс к рублю: {table[key]["well"]}.\n')
            continue

        elif table[key]["Currency"] == message.text:
            bot.send_message(message.chat.id, f'Цифровой код: {table[key]["Digital_code"]}.\n'
                                              f'Буквенный код: {table[key]["Letter_code"]}.\n'
                                              f'Количество: {table[key]["units"]}.\n'
                                              f'Наименование: {table[key]["Currency"]}.\n'
                                              f'Курс к рублю: {table[key]["well"]}.\n')
            continue

    if message.text not in table.keys() and message.text not in msg:
        bot.send_message(message.chat.id, 'Ошибка ввода! Похоже, '
                                          'вы неправильно ввели данные.')


bot.polling(none_stop=True)
