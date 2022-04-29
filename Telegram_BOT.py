import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
token_bot = ''
# Импорт токена бота
with open('token.txt', 'r') as conf:
     token_bot = conf.readline()
# Создание бота
bot = telebot.TeleBot(token_bot)
# Комманда /start

@bot.message_handler(content_types=["text"])
def start(message):
    if message.text == '/start':
    # Добавляем две кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("На сегодня")
        item2 = types.KeyboardButton("На завтра")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id,'Расписание на сегодня или на завтра? ',reply_markup=markup)
    day = message.text
    bot.send_message(message.chat.id, day)
    while day != 'На сегодня' or 'На завтра':
        day = message.text.strip()
    bot.register_next_step_handler(message, group)
    return day

def group(message):
    bot.send_message(message.chat.id, 'Введите вашу группу. Пример ввода 21ТА1')
    gp = message.text
    return gp
# Получение сообщений от юзера

def handle_text(message, day,gp):
# Чтение введенных данных и выбор дня

    if day == 'На сегодня':
        url = 'https://www.ypec.ru/rasp-s'
    else:
        url = 'https://www.ypec.ru/rasp-z'
    response = requests.post(url, data={'grp': gp, 'value' : gp}).text #Формируем запрос с нужной группой
    soup = BeautifulSoup(response, 'html.parser') #Создаем парсер
    zameny = soup.find('table', class_='isp').find_next_siblings('table', class_='isp') # Парсинг таблички замен
    zameny2 = [] # Список для очитски от тегов
    # Очистка от тегов + деление по пробелу
    for i in range(len(zameny)):
        zameny2.append(zameny[i].get_text().split())
    zameny2 = zameny2[0] # Вытаскиваем список из списка
    j = 0
    # Удаляем не нужные данные
    while j != 7:
        zameny2.remove(zameny2[0])
        j += 1
    # Вывод замен
    if zameny2 != []:
        bot.send_message(message.chat.id, 'Замены:\n' + ' '.join(zameny2))
    temp2 = []  # Словарь очищенный от тегов
    temp2.append(soup.find('table', align='center').find('font').get_text())  # Заголовок (день недели + группа)
    temp = []  # Словарь для сырых данных
    temp = (soup.find('td', class_='isp_tec').findAllNext('td', ['isp', 'isp2']))  # Парсинг данных
    # Удаление тегов
    for i in range(len(temp)):
        temp2.append(temp[i].get_text())
    # Вывод одного дня (стоп слово :) следующий день недели из списка)
    sch_f = []
    for i in temp2:
        days_of_week = ['Понидельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        if i not in days_of_week:
            sch_f.append(i)
        else:
            break
    bot.send_message(message.chat.id, '\n'.join(sch_f))
#Запуск бота

bot.polling(none_stop=True, interval=0)
