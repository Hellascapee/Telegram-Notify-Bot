#модули
import telebot
from telebot import types
import time
import sqlite3
bot = telebot.TeleBot('5348582930:AAE2KdROhTqjD7LoFlt5OSPtIDkn7l5jbW0')
#вспомогательные массивы
msup=['/min','/day','/hour']
m1sup=['/n','/notify']
sup=[2,3,4]
sup2=[5,6,7,8,9,0]

def error_format(message):
	bot.send_message(message.chat.id,'❌ Ошибка. Проверьте формат вашего напоминания! ❌ Формат: \n'
									 '\n'
									 'Напомни/напомнить/напоминание *ваш текст напоминания* через *число* единица измерения (час/день/минута)')

#фильтры
symbols = [0,1,2,3,4,5,6,7,8,9,'0','1','2','3','4','5','6','7','8','9']
alter=['напомни','напомнить','напоминание']
hours=['час','часов','часа']
mins=['минута','минут','минуты']
days=['день','дня','дни']
#коннект к базе данных

conn = sqlite3.connect('database.db',check_same_thread=False)
cursor = conn.cursor()

#работа с базой данных

def db_table_val(us_id,text):
    cursor.execute('INSERT INTO test (us_id, text) VALUES (?, ?)',
                   (us_id,text))
    conn.commit()

def sql_carry(us_id, text):
	check = cursor.execute('SELECT * FROM test WHERE us_id=?', (us_id,))
	if check.fetchone() is None:
		db_table_val(us_id, text)
	else:
		delete = """DELETE from test where us_id = ?"""
		cursor.execute(delete, (us_id,))
		conn.commit()
		db_table_val(us_id, text)

#начало работы бота
@bot.message_handler(commands=['start'])
def welcome(message):
	menu=types.ReplyKeyboardMarkup(resize_keyboard=True)
	menu1=types.KeyboardButton('⏱ Создать напоминание')
	menu2 = types.KeyboardButton('⚙ Помощь по боту')
	menu.add(menu1,menu2)
	bot.send_message(message.chat.id, '✉ Вас приветствует NotifyBot (бот-напоминание) ✉\n', reply_markup=menu)

#информация о боте
@bot.message_handler(commands=['info'])
def help(message):
	bot.send_message(message.chat.id, '❓ Для того чтобы создать уведомление: \n1) Введите команду /n или нажмите на кнопку клавиатуры "Создать напоминание" или используйте быстрое напоминание и введите данные о своем уведомлении в формате:\n'
									  '\n'
									  'Напомни/напомнить/напоминание *ваш текст напоминания* через *число* единица измерения (минута/час/день). \n'
									  '\n'
									  '2)Введите текст уведомления. \n3)Выберите единицу измерения. \n4)Укажите количество минут/часов/дней. \n'
									  'Команды бота: /info ; /start ; /n ')
#создать уведомление 1 способ
@bot.message_handler(commands=['n'])
def request_0(message):
	bot.send_message(message.chat.id, '🗒 О чем напомнить?')
	bot.register_next_step_handler(message,request)

@bot.message_handler(content_types=['document','audio','photo'])
def error_type(message):
	bot.send_message(message.chat.id,'Я вас не понимаю! 😔 Список команд бота: /info ; /start ; /n')

@bot.message_handler(content_types=['text'])
def message_handler(message):
	mes=message.text.split(' ')
	if message.text == '⏱ Создать напоминание':
		request_0(message)
	elif message.text == '⚙ Помощь по боту':
		help(message)
	elif mes[0].lower() in alter:
		if 'через' not in mes:
			error_format(message)
		elif mes.index('через')==len(mes)-1:
			error_format(message)
		else:
			hours = ['час', 'часов', 'часа']
			mins = ['минута', 'минут', 'минуты', 'минуту']
			days = ['день', 'дня', 'дни']
			us_id = message.from_user.id
			text=''
			mes.remove(mes[0])
			num=mes.index('через')
			if num+1==len(mes)-1:
				error_format(message)
			elif mes[num+2] not in days and mes[num+2] not in mins and mes[num+2] not in hours:
				error_format(message)
			else:
				for i in range(0,num):
					text=text+' '+mes[i]
					sql_carry(us_id,text)
				for i in range(num+1,len(mes)):
					hours = ['час', 'часов', 'часа']
					mins = ['минута', 'минут', 'минуты','минуту']
					days = ['день', 'дня', 'дни']
					if mes[i] in hours:
						def hours_alter(mes,num):
							for i in range(num+1,len(mes)):
								if mes[num+1] in symbols or int(mes[num+1])%10 in symbols:
									kolvo_=int(mes[num+1])
									us_id = message.from_user.id
									for value in cursor.execute('SELECT * FROM test WHERE us_id=?', (us_id,)):
										reqq = value[1]
									if kolvo_ == 1:
										end = 'час'
									elif kolvo_ in sup:
										end = 'часа'
									elif kolvo_ > 4 and kolvo_ < 20 or kolvo_ // 10 > 1 and kolvo_ % 10 in sup2:
										end = 'часов'
									else:
										end = 'часов'
									bot.send_message(message.chat.id,
													 '💬 Напоминание успешно создано. Я напомню вам о' + str(reqq) + ' через ' + str(kolvo_) + ' ' + str(
														 end) + '!')
									time.sleep(kolvo_ * 60 * 60)
									bot.send_message(message.chat.id, text='🔔 Время для' + reqq + '!')
									break
								else:
									error_format(message)
									break
						hours_alter(mes, num)
					elif mes[i] in mins:
						def mins_alter(mes,num):
							for i in range(num+1,len(mes)):
								if mes[num+1] in symbols or int(mes[num+1])%10 in symbols:
									kolvo_=int(mes[num+1])
									us_id = message.from_user.id
									for value in cursor.execute('SELECT * FROM test WHERE us_id=?', (us_id,)):
										reqq = value[1]
									if kolvo_ == 1:
										end = 'минуту'
									elif kolvo_ in sup:
										end = 'минуты'
									elif kolvo_ > 4 and kolvo_ < 20 or kolvo_ // 10 > 1 and kolvo_ % 10 in sup2:
										end = 'минут'
									else:
										end = 'минуты'
									bot.send_message(message.chat.id,
													 '💬 Напоминание успешно создано. Я напомню вам о' + str(reqq) + ' через ' + str(kolvo_) + ' ' + str(
														 end) + '!')
									time.sleep(kolvo_ * 60)
									bot.send_message(message.chat.id, text='🔔 Время для' + reqq + '!')
									break
								else:
									error_format(message)
									break
						mins_alter(mes,num)
					elif mes[i] in days:
						def days_alter(mes,num):
							for i in range(num + 1, len(mes)):
								if mes[num + 1] in symbols or int(mes[num+1])%10 in symbols:
									kolvo_ = int(mes[num + 1])
									us_id = message.from_user.id
									for value in cursor.execute('SELECT * FROM test WHERE us_id=?', (us_id,)):
										reqq = value[1]
									if kolvo_ == 1:
										end = 'день'
									elif kolvo_ in sup:
										end = 'дня'
									elif kolvo_ > 4 and kolvo_ < 20 or kolvo_ // 10 > 1 and kolvo_ % 10 in sup2:
										end = 'дней'
									else:
										end = 'дней'
									bot.send_message(message.chat.id,
													 '💬 Напоминание успешно создано. Я напомню вам о' + str(reqq) + ' через ' + str(kolvo_) + ' ' + str(
														 end) + '!')
									time.sleep(kolvo_ * 60 * 24 * 60)
									bot.send_message(message.chat.id, text='🔔 Время для' + reqq + '!')
									break
								else:
									error_format(message)
									break
						days_alter(mes,num)
	else:
		bot.send_message(message.chat.id,'Я вас не понимаю! 😔 Список команд бота: /info ; /start ; /n')

def request(message):

	#получение текста уведомления и отправка его в базу данных

	req_ = message.text
	text = req_
	us_id = message.from_user.id
	sql_carry(us_id,text)

	#фильтр на команды

	if req_=='/start':
		welcome(message)
	elif req_ in m1sup:
		request_0(message)
	elif req_=='⚙ Помощь по боту' or req_=='/info':
		help(message)
	elif req_=='⏱ Создать напоминание':
		request_0(message)
	else:
		keyboard_(message)
		# вывод клавиатуры
def keyboard_(message):
	keyboard_1 = '🕒 Выберите единицу времени:'
	keyboard = types.InlineKeyboardMarkup()
	key_hour = types.InlineKeyboardButton(text='Минуты', callback_data='min')
	key_min = types.InlineKeyboardButton(text='Часы', callback_data='hour')
	key_day = types.InlineKeyboardButton(text='Дни', callback_data='days')
	keyboard.add(key_min, key_hour, key_day)
	bot.send_message(message.chat.id, text=keyboard_1, reply_markup=keyboard)


#определение единицы измерения исходя из call.data

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
#основная часть - бот засыпает на определенное время
def mins(call):
	text = call.text
	for i in text:
		if i not in symbols:
			def error(message):
				bot.send_message(message.chat.id, '❌ Ошибка. Введите целое количество минут. ❌')
				keyboard_(message)
			error(call)
			break
		else:
			mins_1(call)
			break
def mins_1(call):
	us_id=call.from_user.id
	for value in cursor.execute('SELECT * FROM test WHERE us_id=?', (us_id,)):
		reqq=value[1]
	text = call.text
	if text=='1':
		end='минуту'
	elif int(text) in sup:
		end='минуты'
	elif int(text)>4 and int(text)<20 or int(text)//10>1 and int(text)%10 in sup2:
		end='минут'
	else:
		end='минуты'
	kolvo=int(text)
	bot.send_message(call.chat.id, '💬 Напоминание успешно создано. Я напомню вам о '+str(reqq)+' через '+str(kolvo)+' '+str(end)+'!')
	time.sleep(kolvo*60)
	bot.send_message(call.chat.id,text='🔔 Время для '+reqq+'!')


def hour(call):
	alpha = [chr(ord("А") + i) for i in range(32)]
	alpha1 = [chr(i) for i in range(65, 91)]
	text = call.text
	for i in text:
		if i.upper() in alpha or i.upper() in alpha1:
			def error(message):
				bot.send_message(message.chat.id, '❌ Ошибка. Введите целое количество часов. ❌')
				keyboard_(message)
			error(call)
			break
		else:
			hour_1(call)
			break
def hour_1(call):
	us_id=call.from_user.id
	for value in cursor.execute('SELECT * FROM test WHERE us_id=?', (us_id,)):
		reqq=value[1]
	text = call.text
	if text == '1':
		end = 'час'
	elif int(text) in sup:
		end = 'часа'
	elif int(text) > 4 and int(text) < 20 or int(text) // 10 > 1 and int(text) % 10 in sup2:
		end = 'часов'
	else:
		end = 'часов'
	kolvo = int(text)
	bot.send_message(call.chat.id, '💬 Напоминание успешно создано. Я напомню вам о ' + str(reqq) + ' через ' + str(kolvo) + ' ' + str(end) + '!')
	time.sleep(kolvo * 60 * 60)
	bot.send_message(call.chat.id,text='🔔 Время для '+reqq+'!')


def day(call):
	alpha = [chr(ord("А") + i) for i in range(32)]
	alpha1 = [chr(i) for i in range(65, 91)]
	text = call.text
	for i in text:
		if i.upper() in alpha or i.upper() in alpha1:
			def error(message):
				bot.send_message(message.chat.id, '❌ Ошибка. Введите целое количество дней. ❌')
				keyboard_(message)
			error(call)
			break
		else:
			day_1(call)
			break
def day_1(call):
	us_id=call.from_user.id
	for value in cursor.execute('SELECT * FROM test WHERE us_id=?', (us_id,)):
		reqq=value[1]
	text = call.text
	if text == '1':
		end = 'день'
	elif int(text) in sup:
		end = 'дня'
	elif int(text) > 4 and int(text) < 20 or int(text) // 10 > 1 and int(text) % 10 in sup2:
		end = 'дней'
	else:
		end = 'дней'
	kolvo = int(text)
	bot.send_message(call.chat.id,'💬 Напоминание успешно создано. Я напомню вам о ' + str(reqq) + ' через ' + str(kolvo) + ' ' + str(end) + '!')
	time.sleep(kolvo * 24 * 60 * 60)
	bot.send_message(call.chat.id, text='🔔 Время для '+reqq+'!')
bot.infinity_polling(timeout=10, long_polling_timeout = 5)
