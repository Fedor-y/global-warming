import telebot
import telebot.types

bot = telebot.TeleBot('8317498777:AAH56fF4FNjtTuX34OEBMqUgcxjHbOwoxUY')

#приветственное сообщение
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton('хочу', callback_data='yes')
    button2 = telebot.types.InlineKeyboardButton('не хочу', callback_data='no')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, 
                     f'''привет, {message.chat.first_name}\nты хочешь знать что такое глобальное потепление и как ты можешь помочь планете?''',
                     reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def info_message(call):
    bot.answer_callback_query(call.id)  # Сначала отвечаем на callback
    bot.send_message(call.message.chat.id, 
                     '''Глобальное потепление — это долгосрочное повышение средней температуры
климатической системы Земли, происходящее преимущественно из-за деятельности человека.

Основная причина: Усиление парникового эффекта из-за выбросов парниковых газов (углекислый газ, метан)
от сжигания ископаемого топлива, вырубки лесов, промышленности и сельского хозяйства.''')
    
    bot.send_message(call.message.chat.id, 
                     'Но ты можешь повлиять на эту проблему и помочь планете!\nХочешь знать как?')
    
    markup = telebot.types.InlineKeyboardMarkup()
    yes_button = telebot.types.InlineKeyboardButton('Да!', callback_data='yea')
    no_button = telebot.types.InlineKeyboardButton('Нет...', callback_data='nah')
    markup.add(yes_button, no_button)
    bot.send_message(call.message.chat.id, 'Выбери вариант:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'nah')
def not_interested(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 
                     'Окей! Если захочешь узнать больше - нажми /start снова.')

@bot.callback_query_handler(func=lambda call: call.data == 'yea')
def send_help_options(call):
    bot.answer_callback_query(call.id)
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    button1 = telebot.types.InlineKeyboardButton('🏠 Узнать об энергоэффективности дома', 
                                                 callback_data='energy')
    button2 = telebot.types.InlineKeyboardButton('🗑️ Посмотреть инструкцию по сортировке мусора', 
                                                 callback_data='sorting')
    button3 = telebot.types.InlineKeyboardButton('😂 Посмотреть экологический мем', 
                                                 callback_data='meme')
    markup.add(button1, button2, button3)
    
    bot.send_message(call.message.chat.id, 
                     'Отлично! Вот несколько способов, с которых можно начать:\nВыбери интересующий раздел:', 
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['energy', 'sorting', 'meme'])
def send_selected_info(call):
    bot.answer_callback_query(call.id)
    
    if call.data == 'energy':
        bot.send_message(call.message.chat.id,
                         '''**Энергоэффективность дома:**
                         • Замени лампочки на светодиодные
                         • Утепли окна и двери
                         • Используй программируемый термостат
                         • Выключай электроприборы из розетки
                         • Установи датчики движения для света

*Эти меры могут сократить счета за энергию на 20-30%!*''',
                         parse_mode='Markdown')
        
    elif call.data == 'sorting':
        bot.send_message(call.message.chat.id,
                         '''**Сортировка мусора:**
                         • **Пластик** (1, 2, 4, 5) - бутылки, упаковка
                         • **Стекло** - банки, бутылки (без крышек)
                         • **Бумага** - картон, газеты, журналы
                         • **Металл** - алюминиевые и стальные банки
                         • **Опасные отходы** - батарейки, лампы, техника - сдавать в специальные пункты!

📝 **Важно:** Перед сдачей сполосни и сплющи упаковку!''',
                         parse_mode='Markdown')
        
    elif call.data == 'meme':
        # Временно используем текстовый мем, но можно добавить фото
        bot.send_message(call.message.chat.id,
                         '🌱 *Экологический мем дня:*\n\n'
                         'Когда забываешь выключить свет, уходя из комнаты:\n'
                         'Планета: 👀\n'
                         'Твой счет за электричество: 📈\n\n'
                         'Когда сортируешь мусор правильно:\n'
                         'Планета: 😊🌍',
                         parse_mode='Markdown')
    
    # Добавляем кнопку "Назад" к основному меню
    markup = telebot.types.InlineKeyboardMarkup()
    back_button = telebot.types.InlineKeyboardButton('← Назад к выбору', callback_data='yea')
    markup.add(back_button)
    bot.send_message(call.message.chat.id, 
                     'Хочешь узнать о других способах помочь?', 
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'no')
def say_for_no(call):
    bot.answer_callback_query(call.id)  # Добавляем ответ на callback
    bot.send_message(call.message.chat.id, 
                     'Хорошо, нажми /start, если передумаешь')

bot.polling()
