gp = input("Введите вашу группу" '\n').upper() #Ввод группы
day = input('Сегодня' + ' ' + 'или' + ' ' + 'Завтра?'+'\n') # На сегодня или завтра (расписание)
url = ''
# Чтение введенных данных и выбор дня
if day == 'Сегодня':
    url = 'https://www.ypec.ru/rasp-s'
else:
    url = 'https://www.ypec.ru/rasp-z'
import requests
from bs4 import BeautifulSoup
response = requests.post(url, data={'grp': gp, 'value' : gp}).text #Формируем запрос с нужной группой
soup = BeautifulSoup(response, 'html.parser') #Создаем парсер
def changes():
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
        print('\n' + 'ЗАМЕНА(Ы)') # Заголовок замены
        for i in range(len(zameny2)):
            print(zameny2[i], end=' ')
    else:
        print('\n' + 'ЗАМЕН НЕТ') # Строка ЗАМЕН НЕТ
def schedule():
    temp2 = [] #Словарь очищенный от тегов
    temp2.append(soup.find('table', align='center').find('font').get_text()) # Заголовок (день недели + группа)
    temp = [] # Словарь для сырых данных
    temp = (soup.find('td', class_='isp_tec').findAllNext('td', ['isp', 'isp2'])) # Парсинг данных
    # Удаление тегов
    for i in range(len(temp)):
        temp2.append(temp[i].get_text())
    # Вывод одного дня (стоп слово :) следующий день недели из списка)
    for i in temp2:
        days_of_week = ['Понидельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        if i not in days_of_week:
            print(i)
        else:
            break
try:
    schedule()
except AttributeError:
    print('Группа введена не верно. Пример ввода 21ТА1')
changes()