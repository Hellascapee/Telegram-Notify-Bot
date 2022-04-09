import telebot
from telebot import types
import time
msup=['/min','/day','/hour','/help','/start','/n','/notify']
bot = telebot.TeleBot('5214967905:AAGjM1jR_j4uCQMb_fOoMGmFFj1yyLhQt0w')
sup=[]
sup1=[]
sup2=['1','2','3','4']
sup3=[2,3,4]
sup4=[5,6,7,8,9,0]
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
	bot.send_message(message.chat.id, 'Вас приветствует NotifyBot(бот-напоминание)\n'
										   'Бот предназначен для создания напоминаний.\n'
										   'Чтобы начать введите /notify или /n')
@bot.message_handler(commands=['n', 'notify'])
def request(message):
	bot.send_message(message.chat.id, 'О чем напомнить?')
	bot.register_next_step_handler(message,choose)
def choose(message):
	req=message.text
	sup.append(req)
	if sup[0] in msup:
		bot.send_message(message.from_user.id,'Для начала введите текст будущего уведомления!')
		sup.remove(sup[0])
		bot.register_next_step_handler(message,choose)
	else:
		ed_iden = 'Выберите единицу времени:'
		keyboard = types.InlineKeyboardMarkup()
		key_hour = types.InlineKeyboardButton(text='Минуты', callback_data='min')
		key_min = types.InlineKeyboardButton(text='Часы', callback_data='hour')
		key_day = types.InlineKeyboardButton(text='Дни', callback_data='days')
		keyboard.add(key_min,key_hour,key_day)
		bot.send_message(message.chat.id, text=ed_iden, reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def choose_1(call):
	if call.data=='min':
		bot.send_message(call.message.chat.id,'Введите целое количество минут.')
		bot.register_next_step_handler(call.message, mins)
	elif call.data=='hour':
		bot.send_message(call.message.chat.id,'Введите целое количество часов.')
		bot.register_next_step_handler(call.message, hour)
	elif call.data == 'days':
		bot.send_message(call.message.chat.id, 'Введите целое количество дней.')
		bot.register_next_step_handler(call.message, day)
def mins(call):
	text = call.text
	if text=='1':
		end='минуту'
	elif int(text) in sup3:
		end='минуты'
	elif int(text)>4 and int(text)<20 or int(text)//10>1 and int(text)%10 in sup4:
		end='минут'
	else:
		end='минуты'
	kolvo=int(text)
	bot.send_message(call.chat.id, 'Я напомню вам о '+str(sup[0])+' через '+str(kolvo)+' '+str(end)+'!')
	time.sleep(kolvo*60)
	bot.send_message(call.chat.id,text=sup)
def hour(call):
	text = call.text
	if text == '1':
		end = 'час'
	elif int(text) in sup3:
		end = 'часа'
	elif int(text) > 4 and int(text) < 20 or int(text) // 10 > 1 and int(text) % 10 in sup4:
		end = 'часов'
	else:
		end = 'часов'
	kolvo = int(text)
	bot.send_message(call.chat.id, 'Я напомню вам о ' + str(sup[0]) + ' через ' + str(kolvo) + ' ' + str(end) + '!')
	time.sleep(kolvo * 60 * 60)
	bot.send_message(call.chat.id, text=sup)
def day(call):
	text = call.text
	if text == '1':
		end = 'день'
	elif int(text) in sup3:
		end = 'дня'
	elif int(text) > 4 and int(text) < 20 or int(text) // 10 > 1 and int(text) % 10 in sup4:
		end = 'дней'
	else:
		end = 'дней'
	kolvo = int(text)
	bot.send_message(call.chat.id,'Я напомню вам о ' + str(sup[0]) + ' через ' + str(kolvo) + ' ' + str(end) + '!')
	time.sleep(kolvo * 24 * 60 * 60)
	bot.send_message(call.chat.id, text=sup)
bot.infinity_polling()
