import telebot
from db import SQLParser
from telebot import apihelper
import warnings
import time

myfile = open ("telegram_api.txt", "r")
data=myfile.readlines()
myfile.close()
bot = telebot.TeleBot(data[0], threaded=False);
#apihelper.proxy = {'https': 'socks5://8.210.163.246:50032'}
#apihelper.proxys = {'http': 'socks5://telegram.vpn99.net:55655','https': 'socks5://telegram.vpn99.net:55655'}
data_base = SQLParser()
data_base.create_db()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id,
                     'Здравствуйте, я бот сокращатель лекций. '
                     'Пришлите мне ссылку на видео, и я с радостью его укорочу. '
                     'Или ссылку на целый плейлист, и я сам буду укорачивать новые видео. '
                     'Это не ускорение видео, я вырезаю те фрагменты, когда лектор молчит. '
                     'Таким образом после уменьшения видео, его почти так же комфортно смотреть. '
                     'Дополнительно используя x2 ускорение можно получить почти 4-ёх кратный прирост скорости '
                     'сохряняя информативность лекции')
    bot.send_message(message.from_user.id,
                     'Обработанные файлы доступны по ссылке '
                     'https://drive.google.com/drive/folders/1n1Zi4KbOKQgOaoKyYuo4Vs0vARAhXsBr?usp=sharing')
    bot.send_message(message.from_user.id, 'Отсылайте сообщения в формате /send_link https://www.youtube.com...')
    bot.send_message(message.from_user.id, 'Чтобы прислать плейлист, просто пришлите ссылку на видео из плейлиста')
    data_base.save(0, message.from_user.id, 'user')


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.from_user.id,
                     'Обработанные файлы доступны по ссылке '
                     'https://drive.google.com/drive/folders/1n1Zi4KbOKQgOaoKyYuo4Vs0vARAhXsBr?usp=sharing')
    bot.send_message(message.from_user.id, 'Отсылайте сообщения в формате /send_link https://www.youtube.com...')
    bot.send_message(message.from_user.id, 'Чтобы прислать плейлист, просто пришлите ссылку на видео из плейлиста')
    data_base.save(0, message.from_user.id, 'user')


@bot.message_handler(commands=['send_link'])
def link_messages(message):
    bot.send_message(message.from_user.id, 'ваша ссылка: ' + message.text[11::])
    data_base.save(0, message.from_user.id, 'user')
    if data_base.get_status(0, message.from_user.id) == 'ban':
        bot.send_message(message.from_user.id, 'Извените, но вы были забанены.')
    else:
        link = message.text[11::]
        print(link) #просто пишет в консоль ссылки, которые принял
        if not (('https://www.youtube.com/watch' in link) or ('http://www.youtube.com/watch' in link) or
                ('https://m.youtube.com/watch' in link) or ('http://m.youtube.com/watch' in link) or
                ('https://youtube.com/watch' in link) or ('http://youtube.com/watch' in link)):
            bot.send_message(message.from_user.id, 'Ваша ссылка имеет неправильный формат')
        else:
            if 'list' in link:
                bot.send_message(message.from_user.id,
                                 'Ваша ссылка принята, статус:' + data_base.save(2, link, 'in queue'))
            else:
                bot.send_message(message.from_user.id,
                                 'Ваша ссылка принята, статус:' + data_base.save(1, link, 'in queue'))
            bot.send_message(message.from_user.id, 'Чтобы узнать статус обработки, отправьте эту ссылку ещё раз')


@bot.message_handler(commands=['get_users'])
def users_messages(message):
    if data_base.get_status(0, message.from_user.id) == 'admin':
        for i in data_base.get_all(0):
            bot.send_message(message.from_user.id, str(i[0]) + ' ' + str(i[1]))
    else:
        bot.send_message(message.from_user.id, 'Вы не админ')


@bot.message_handler(commands=['get_videos'])
def videos_messages(message):
    if data_base.get_status(0, message.from_user.id) == 'admin':
        for i in data_base.get_all(1):
            bot.send_message(message.from_user.id, str(i[0]) + ' ' + str(i[1]))
    else:
        bot.send_message(message.from_user.id, 'Вы не админ')


@bot.message_handler(commands=['get_playlists'])
def playlists_messages(message):
    if data_base.get_status(0, message.from_user.id) == 'admin':
        for i in data_base.get_all(2):
            bot.send_message(message.from_user.id, str(i[0]) + ' ' + str(i[1]))
    else:
        bot.send_message(message.from_user.id, 'Вы не админ')


@bot.message_handler(commands=['ban_user'])
def ban_messages(message):
    if data_base.get_status(0, message.from_user.id) == 'admin':
        data_base.set_status(0, int(message.text[10::]), 'ban')
    else:
        bot.send_message(message.from_user.id, 'Вы не админ')


@bot.message_handler(commands=['send_to_all'])
def all_messages(message):
    if data_base.get_status(0, message.from_user.id) == 'admin':
        for i in data_base.get_all(0):
            bot.send_message(i[0], message.text[13::])
    else:
        bot.send_message(message.from_user.id, 'Вы не админ')

while True:
    try:
        bot.polling(none_stop=False, interval=5)
    except:
        warnings.warn(message="connection error", category=UserWarning, stacklevel=1)
        time.sleep(5)


