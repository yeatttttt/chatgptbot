import misc
import main
import telebot
from telebot import types


bot = telebot.TeleBot(misc.tg_bot_api)

def tgbot():              

	@bot.message_handler(commands=['start'])
	def send_welcome(message):
	    user_id = message.from_user.id
	    # Create a welcome message with inline keyboard
	    markup = types.InlineKeyboardMarkup(row_width=1)
	    item = types.InlineKeyboardButton("Задайте мне вопрос.", callback_data='question')
	    markup.add(item)
	    bot.send_message(message.chat.id, "Привет! Я телеграм-бот ChatGPT. Я здесь, чтобы помочь вам с любыми вопросами. Пожалуйста, нажмите кнопку ниже, чтобы задать мне вопрос.", reply_markup=markup)

	@bot.callback_query_handler(func=lambda call: True)
	def callback_query(call):
	    if call.data == 'question':
	        bot.answer_callback_query(call.id)
	        bot.send_message(call.message.chat.id, "Пожалуйста введите вопрос.")

	@bot.message_handler(func=lambda message: True)
	def echo_all(message):
		print("30% - message got, collecting info")
		user_id = message.from_user.id
		username = message.from_user.username
		firstname = message.from_user.first_name

		if message.text == 'question':
			return
		print("40% - answer build up started")
		bot.reply_to(message, main.chatgpt(firstname, username, user_id, message.text))




	bot.polling(none_stop=True, interval=0, timeout=10)