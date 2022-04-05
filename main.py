import telebot
from telebot import types

#5165717781:AAFjU1odFXMuyNSnZk4xxoEJTzc2wKUsCTA
bot = telebot.TeleBot("5165717781:AAFjU1odFXMuyNSnZk4xxoEJTzc2wKUsCTA")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.from_user.id, 'Вас приветствует NotifyBot(бот-напоминание)\n'
										   'Бот предназначен для создания напоминаний.')
	bot.send_message(message.from_user.id, 'Чтобы начать введите /notify или /n')
	bot.register_next_step_handler(message,notify_step)
def notify_step(message):
	ed_iden='Выберите единицу времени:'
	keyboard = types.InlineKeyboardMarkup()
	key_hour = types.InlineKeyboardButton(text='Часы', callback_data='hour')
	keyboard.add(key_hour)
	key_min = types.InlineKeyboardButton(text='Минуты', callback_data='min')
	keyboard.add(key_min)
	key_day = types.InlineKeyboardButton(text='Дни', callback_data='days')
	keyboard.add(key_day)
	bot.send_message(message.from_user.id, text=ed_iden, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_ed(call,text):
	if call.data=='hour':
		q1='Выбраны часы. \n Через сколько часов напомнить? \n Или введите число часов самостоятельно.'
		keyboard = types.InlineKeyboardMarkup()
		key_1hour = types.InlineKeyboardButton(text='1 час', callback_data='1')
		keyboard.add(key_1hour)
		key_2hours = types.InlineKeyboardButton(text='2 часа', callback_data='2')
		keyboard.add(key_2hours)
		key_3hours = types.InlineKeyboardButton(text='3 часа', callback_data='3')
		keyboard.add(key_3hours)
		bot.send_message(call.from_user.id, text=q1, reply_markup=keyboard)
		kolvo_hours=text.message
		kolvo_hours=int(kolvo_hours)




bot.infinity_polling()






