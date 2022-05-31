# coding: utf - 8
import requests
import telebot
from telebot import types
token = '5076012878:AAFqm5lP8WC5qBpN_HfsCnYkr2l81DNIfJc'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_phone = types.KeyboardButton(text='Отправить свой контакт (телеграмма)', request_contact=True)
    markup.add(button_phone)
    bot.send_message(m.chat.id, 'Приветствую тебя, {0.first_name}, я информационный бот. '
                                '\nДля получения информации можете воспользоваться подсказками ниже'
                                '\nЧто бы получить доступ к функционалу, отправьте свой номер.'.format(m.from_user), reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def contact(message):
        if message.contact is not None:
            print(message.contact)
            global pol
            pol = '+' + message.contact.phone_number
            bot.send_message(message.from_user.id, 'Запись контакта прошла успешна')
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            item1 = types.KeyboardButton('История поездок')
            item2 = types.KeyboardButton('Ближайший самокат')
            item3 = types.KeyboardButton('Информация')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id,'Что вас интересует?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def phone(m, res=False):
    if m.chat.type == 'private':
        if m.text == 'История поездок':
            def history():
                phn = {'phone': pol}
                url = 'https://uram.ddns.net/uram_bot/history'
                req_j = requests.post(url, json=phn)
                req_data = req_j.json()
                if req_j.status_code == 200:
                    try:
                        for req_data['history'][0] in req_data['history']:
                            bot.send_message(m.from_user.id, ('Цена: ' + str(req_data['history'][0]['cost']) +
                                                                    '\nНачало: ' + req_data['history'][0]['start_time'].
                                                                    replace('Mon', 'Понедельник').replace('Tue',
                                                                                                          'Вторник').
                                                                    replace('Wed', 'Среда').replace('Thu', 'Четверг').
                                                                    replace('Fri', 'Пятница').replace('Sat', 'Суббота').
                                                                    replace('Sun', 'Воскресенье').replace('Jan',
                                                                                                          'Января').
                                                                    replace('Feb', 'Февраля').replace('Mar', 'Марта').
                                                                    replace('Apr', 'Апреля').replace('May', 'Мая').
                                                                    replace('June', 'Июня').replace('July', 'Июля').
                                                                    replace('Aug', 'Августа').replace('Sept',
                                                                                                      'Сентября').
                                                                    replace('Oct', 'Октября').replace('Nov', 'Ноября').
                                                                    replace('Dec', 'Декабря') +
                                                                    '\nКонец: ' + req_data['history'][0]['end_time'].
                                                                    replace('Mon', 'Понедельник').replace('Tue',
                                                                                                          'Вторник').
                                                                    replace('Wed', 'Среда').replace('Thu', 'Четверг').
                                                                    replace('Fri', 'Пятница').replace('Sat', 'Суббота').
                                                                    replace('Sun', 'Воскресенье').replace('Jan',
                                                                                                          'Января').
                                                                    replace('Feb', 'Февраля').replace('Mar', 'Марта').
                                                                    replace('Apr', 'Апреля').replace('May', 'Мая').
                                                                    replace('June', 'Июня').replace('July', 'Июля').
                                                                    replace('Aug', 'Августа').replace('Sept',
                                                                                                      'Сентября').
                                                                    replace('Oct', 'Октября').
                                                                    replace('Nov', 'Ноября').replace('Dec', 'Декабря') +
                                                                    '\nСтатус поездки: ' + req_data['history'][0][
                                                                        'status'].
                                                                    replace('end', 'завершена')))
                    except KeyError:
                        bot.send_message(m.from_user.id, 'Что то пошло не так')
                    except IndexError:
                        print()
                else:
                    bot.send_message(m.from_user.id, 'Что то пошло не так')

            t = history()

        elif m.text == 'Ближайший самокат':
            @bot.message_handler(content_types=["location"])
            def location(message):
                if message.location is not None:
                    print(message.location)
                    print(message.contact)
                    print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))

                    def greting():
                        url = 'https://uram.ddns.net/uram_bot/find'
                        req = {'lat': '18', 'lon': '18'}
                        data = message.location.latitude
                        data2 = message.location.longitude
                        req['lat'] = data
                        req['lon'] = data2
                        req['phone'] = pol
                        req_j = requests.post(url, json=req)
                        req_data = req_j.json()
                        a = req_data['lat']
                        b = req_data['lon']
                        print(a, b)
                        global result
                        result = a, b
                        print(result)
                        longitude = result[1]
                        latitude = result[0]
                        bot.send_location(m.from_user.id, latitude, longitude)

                    test = greting()
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text="Отправить свое местоположение", request_location=True)
            item5 = types.KeyboardButton(text='Назад')
            keyboard.add(button_geo, item5)
            bot.send_message(m.chat.id, "Отправьте свое местоположение", reply_markup=keyboard)
        elif m.text == 'Информация':
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            item1 = types.KeyboardButton(text='Оплата')
            item2 = types.KeyboardButton(text='Как поехать')
            item3 = types.KeyboardButton(text='Как закончить')
            item4 = types.KeyboardButton(text='Как найти')
            item5 = types.KeyboardButton(text='Назад')
            keyboard.add(item1, item2, item3, item4, item5)
            bot.send_message(m.chat.id, 'Какая информация вас интересует?', reply_markup=keyboard)
        elif m.text == 'Оплата':
            url = 'https://uram.ddns.net/uram_bot/tariffs'
            how = requests.get(url)
            how_data = how.json()
            bot.send_message(m.chat.id, "Оплатить можно по карте \nСтоимость начало поездки = "
                             + str(how_data['tariffs'][0]['cost_start']) + " рублей \n1 минута поездки = "
                             + str(how_data['tariffs'][0]['cost_minute']) + ' рублей'
                             + '\nОждиание = ' + str(how_data['tariffs'][0]['cost_pause']) + ' рублей')
        elif m.text == 'Как поехать':
            bot.send_message(m.chat.id, 'Чтобы включить электросамокат, достаточно найти его в приложении.'
                                        'Она расположена на руле рядом с информативным дисплеем.'
                                        '\nКогда самокат включится, нажмите специальный курок на руле'
                                        ' самоката и он поедет. Курок расположен на правой рукоятке.')
        elif m.text == 'Как закончить':
            bot.send_message(m.chat.id, "Нужно оставить самокат и заблокировать его.")
        elif m.text == 'Как найти':
            bot.send_message(m.chat.id, "Найти его можно по карте. Или на парковке.")
        elif m.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            item1 = types.KeyboardButton('История поездок')
            item2 = types.KeyboardButton('Ближайший самокат')
            item3 = types.KeyboardButton('Информация')
            markup.add(item1, item2, item3)
            bot.send_message(m.chat.id, 'Что вас интересует?', reply_markup=markup)


print('bot started')
bot.polling(none_stop=True, interval=0)
