import telebot
import telebot.types

bot = telebot.TeleBot('8317498777:AAH56fF4FNjtTuX34OEBMqUgcxjHbOwoxUY')

#приветственное сообщение
@bot.message_handler(commands=['start'])
def start_message(message):
    marcup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton('информация', callback_data='info')
    button2 = telebot.types.InlineKeyboardButton('че-то там еще', callback_data='something')
    marcup.add(button1,button2)
    bot.send_message(message.chat.id,f'привет, {message.chat.first_name}\nя бот, который поможет решить \nпроблему глобального потепления',
     reply_markup=marcup)

@bot.callback_query_handler(func=lambda call: call.data == 'info')
def info_message(call):
    bot.send_message(call.message.chat.id, 'Здесь будет информация о глобальном потеплении')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'something')
def something_message(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton('Причины', callback_data='causes')
    btn2 = telebot.types.InlineKeyboardButton('Последствия', callback_data='consequences')
    btn3 = telebot.types.InlineKeyboardButton('Решения', callback_data='solutions')
    btn4 = telebot.types.InlineKeyboardButton('Статистика', callback_data='stats')
    btn5 = telebot.types.InlineKeyboardButton('◀️ Назад', callback_data='back_to_start')
    markup.add(btn1, btn2, btn3, btn4)
    markup.add(btn5)
    
    bot.edit_message_text(
        'Выберите раздел:',
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

'''задача на сегодня:
добавить краткое описание проблемы потепления и способы решения этой проблемы 
при нажатии на определенную кнопку
'''

bot.polling()