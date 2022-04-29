import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
# Импорт токена бота
with open('token.txt', 'r') as conf:
     token_bot = conf.readline()
# Создание бота
bot = telebot.TeleBot(token_bot)
gp = ''
day = ''
soup = None
callback_data = None
zameny2 = []
url = ''
@bot.message_handler(content_types=['text'])
# Команда старт
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Введите вашу группу. Пример ввода 21ТА1")
        bot.register_next_step_handler(message, get_gp)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')
# Получение gp, создание клавиатуры опроса дня.
def get_gp(message):
    global gp
    gp = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("На сегодня")
    item2 = types.KeyboardButton("На завтра")
    item3 = types.KeyboardButton("/start")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(message.from_user.id, 'Расписание на сегодня или на завтра? ', reply_markup=markup)
    bot.register_next_step_handler(message, parser)
# Парсинг
def parser(message):
# Чтение введенных данных и выбор дня'
    if message.text == 'На сегодня':
        url = 'https://www.ypec.ru/rasp-s'
    else:
        url = 'https://www.ypec.ru/rasp-z'

    response = requests.post(url, data={'grp': gp, 'value' : gp}).text #Формируем запрос с нужной группой
    global soup, zameny2
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
    #bot.register_next_step_handler(message, zameny_out);
#def zameny_out(message):
    if zameny2 != []:
        bot.send_message(message.from_user.id, 'Замены:\n' + ' '.join(zameny2))
    temp2 = []  # Словарь очищенный от тегов
    temp2.append(soup.find('table', align='center').find('font').get_text())  # Заголовок (день недели + группа)
    temp = []  # Словарь для сырых данных
    e = 0
    try:
        temp = (soup.find('td', class_='isp_tec').findAllNext('td', ['isp', 'isp2']))  # Парсинг данных
    except:
        bot.send_message(message.from_user.id, 'Ошибка')
        e = 1
    # Удаление тегов
    if e != 1:
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
        bot.send_message(message.from_user.id, '\n'.join(sch_f))
bot.polling(none_stop=True, interval=0)
