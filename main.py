import telebot
from telebot import types
import time
bot = telebot.TeleBot('5214967905:AAGjM1jR_j4uCQMb_fOoMGmFFj1yyLhQt0w')
#supports arr
sup=[]
sup1=[]
sup2=['1','2','3','4']
sup3=[2,3,4]
sup4=[5,6,7,8,9,0]
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
	bot.send_message(message.from_user.id, 'Вас приветствует NotifyBot(бот-напоминание)\n'
										   'Бот предназначен для создания напоминаний.')
	bot.send_message(message.from_user.id, 'Чтобы начать введите /notify или /n')
	bot.register_next_step_handler(message,request)
@bot.message_handler(commands=['n', 'notify'])
def request(message):
	bot.send_message(message.from_user.id, 'О чем напомнить?')
	bot.register_next_step_handler(message,choose)
	sup1.append(1)
def choose(message):
	req=message.text
	sup.append(req)
	sup.append(1)
	if ('/min' in sup or sup1==[]) or ('/hour' in sup or sup1==[]) or ('/day' in sup or sup1==[]):
		bot.send_message(message.from_user.id,'Для начала введите текст будущего уведомления!')
		if '/min' in sup:
			sup.remove('/min')
		if '/hour' in sup:
			sup.remove('/hour')
		if '/day' in sup:
			sup.remove('/day')
		bot.register_next_step_handler(message,choose)
	else:
		ed_iden = 'Выберите единицу времени:'
		keyboard = types.InlineKeyboardMarkup()
		key_hour = types.InlineKeyboardButton(text='Минуты', callback_data='min')
		keyboard.add(key_hour)
		key_min = types.InlineKeyboardButton(text='Часов', callback_data='hour')
		keyboard.add(key_min)
		key_day = types.InlineKeyboardButton(text='Дни', callback_data='days')
		keyboard.add(key_day)
		bot.send_message(message.from_user.id, text=ed_iden, reply_markup=keyboard)
		@bot.callback_query_handler(func=lambda call: True)
		def choose_1(call):
			if call.data=='min':
				bot.send_message(message.from_user.id,'Введите целое количество минут.')
				@bot.message_handler(func=lambda message: True)
				def min_1(message):
					text = message.text
					if text=='1':
						end='минуту'
					elif int(text) in sup3:
						end='минуты'
					elif int(text)>4 and int(text)<20 or int(text)//10>1 and int(text)%10 in sup4:
						end='минут'
					else:
						end='минуты'
					kolvo=int(text)
					bot.send_message(message.from_user.id, 'Я напомню вам о '+str(req)+' через '+str(kolvo)+' '+str(end)+'!')
					time.sleep(kolvo*60)
					bot.send_message(message.from_user.id,text=sup)
			elif call.data=='hour':
				bot.send_message(message.from_user.id, 'Введите целое количество часов.')
				@bot.message_handler(func=lambda message: True)
				def hour_1(message):
					text = message.text
					if text == '1':
						end = 'час'
					elif int(text) in sup3:
						end = 'часа'
					elif int(text) > 4 and int(text) < 20 or int(text) // 10 > 1 and int(text) % 10 in sup4:
						end = 'часов'
					else:
						end = 'часов'
					kolvo = int(text)
					bot.send_message(message.from_user.id,'Я напомню вам о ' + str(req) + ' через ' + str(kolvo) + ' ' + str(end) + '!')
					time.sleep(kolvo * 60*60)
					bot.send_message(message.from_user.id, text=sup)
			elif call.data=='days':
				bot.send_message(message.from_user.id, 'Введите целое количество дней.')
				@bot.message_handler(func=lambda message: True)
				def day_1(message):
					text = message.text
					if text == '1':
						end = 'день'
					elif int(text) in sup3:
						end = 'дня'
					elif int(text) > 4 and int(text) < 20 or int(text) // 10 > 1 and int(text) % 10 in sup4:
						end = 'дней'
					else:
						end = 'дней'
					kolvo = int(text)
					bot.send_message(message.from_user.id,'Я напомню вам о ' + str(req) + ' через ' + str(kolvo) + ' ' + str(end) + '!')
					time.sleep(kolvo * 24*60*60)
					bot.send_message(message.from_user.id, text=sup)
bot.infinity_polling()
