import telebot
from telebot import types
from config import *
from db import *


bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	tg_id = message.chat.id
	user_full_name = message.from_user.full_name
	bot.send_message(tg_id, f"Приветствую, {user_full_name}! Чтобы начать со мной работу напиши мне команду: /help")
	user = get_user(tg_id)
	print(user)
	if user is None:
		insert(tg_id)
	else:
		bot.send_message(tg_id, 'Вы уже зарегестрированы! ')

@bot.message_handler(commands=['help'])
def help(message, res=False):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton('Новости')
	item2 = types.KeyboardButton('Категории')
	item3 = types.KeyboardButton('Посмотреть свои подписки')
	markup.add(item1, item2, item3)
	bot.send_message(message.chat.id, "Выберите что вы хотите сделать: ", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_text(message):
	tg_id = message.chat.id
	cats = get_category()
	back = types.KeyboardButton("В основное меню")
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	if message.text.strip() == 'Категории':
		text = 'Выберите категорию на которую хотите подписаться: \n'
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		for i in cats:
			text += f'{i[0]}) {i[2]} \n'
			btn = types.KeyboardButton(f'Подписаться на {i[2]}')
			markup.add(btn)
		markup.add(back)
		bot.send_message(message.chat.id, text, reply_markup=markup)

	if message.text.startswith('Подписаться на'):
		cat = message.text[15:]
		cat_id = getIdCat(cat)[0]

		if isSub(tg_id, cat_id) == None:
			insertSub(tg_id, cat_id)
			text = f"Подписка на '{cat}' оформлена"
		else:
			text = f"Вы уже подписаны на '{cat}'"

		bot.send_message(message.chat.id, text, reply_markup=markup)

	if message.text.strip() == 'Посмотреть свои подписки':
		subs = getSubUser(tg_id)
		text = 'Ваши подписки: \n'
		for i in subs:
			text += f'{i[0]}\n'
			markup.add(types.KeyboardButton(f"Отписаться от {i[0]}"))
		markup.add(back)

		bot.send_message(message.chat.id, text, reply_markup=markup)

	if message.text.startswith('Отписаться от'):
		sub = message.text[14:]
		cat_id = getIdCat(sub)
		if isSub(tg_id, cat_id) == None:
			text = f"Вы еще не подписаны на '{sub}'"
			bot.send_message(message.chat.id, text)
		else:
			delSub(tg_id, cat_id)
			subs = getSubUser(tg_id)
			back = types.KeyboardButton('В основное меню')
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			markup.add(back)
			for i in subs:
				markup.add(types.KeyboardButton(f"Отписаться от {i[0]}"))
			bot.send_message(message.chat.id, f"Вы отписались от категории '{sub}'", reply_markup=markup)



	if message.text == 'В основное меню':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton('Новости')
		item2 = types.KeyboardButton('Категории')
		item3 = types.KeyboardButton('Посмотреть свои подписки')
		markup.add(item1, item2, item3)
		bot.send_message(message.chat.id, "Выберите, что вы хотите сделать: ", reply_markup=markup)



bot.infinity_polling()
