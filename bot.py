import telebot
import telebot.types

bot = telebot.TeleBot('8317498777:AAH56fF4FNjtTuX34OEBMqUgcxjHbOwoxUY')

# Хранилище состояний пользователей
user_states = {}

# Функции для управления состояниями
def get_user_state(chat_id):
    if chat_id not in user_states:
        user_states[chat_id] = {
            'messages': [],
            'waiting_for_input': None,
            'calc_data': {}
        }
    return user_states[chat_id]

def save_message_id(chat_id, message_id):
    state = get_user_state(chat_id)
    state['messages'].append(message_id)

def clear_user_messages(chat_id):
    state = get_user_state(chat_id)
    try:
        for msg_id in state['messages']:
            try:
                bot.delete_message(chat_id, msg_id)
            except:
                pass
    except:
        pass
    state['messages'] = []
    state['waiting_for_input'] = None

# Приветственное сообщение
@bot.message_handler(commands=['start'])
def start_message(message):
    clear_user_messages(message.chat.id)
    state = get_user_state(message.chat.id)
    state['waiting_for_input'] = None
    
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton('Да, хочу узнать!', callback_data='main_yes')
    button2 = telebot.types.InlineKeyboardButton('Пока нет', callback_data='main_no')
    markup.add(button1, button2)
    
    msg = bot.send_message(message.chat.id, 
                         f'''🌍 Привет, {message.chat.first_name}!

Хочешь узнать о глобальном потеплении и как ты можешь помочь планете?''',
                         reply_markup=markup)
    
    save_message_id(message.chat.id, msg.message_id)

# Главное меню
@bot.callback_query_handler(func=lambda call: call.data == 'main_yes')
def info_message(call):
    clear_user_messages(call.message.chat.id)
    state = get_user_state(call.message.chat.id)
    state['waiting_for_input'] = None
    
    msg1 = bot.send_message(call.message.chat.id, 
                         '''🌡️ **Глобальное потепление** — это долгосрочное повышение средней температуры
климатической системы Земли, происходящее преимущественно из-за деятельности человека.

**Основная причина:** Усиление парникового эффекта из-за выбросов парниковых газов
(углекислый газ, метан) от сжигания ископаемого топлива, вырубки лесов, промышленности и сельского хозяйства.''',
                         parse_mode='Markdown')
    
    save_message_id(call.message.chat.id, msg1.message_id)
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    energy_calc = telebot.types.InlineKeyboardButton('🧮 Рассчитать энергоэффективность', callback_data='calc_energy')
    waste_info = telebot.types.InlineKeyboardButton('🗑️ Узнать о сортировке отходов', callback_data='waste_types')
    tips = telebot.types.InlineKeyboardButton('💡 Советы по экожизни', callback_data='eco_tips')
    meme = telebot.types.InlineKeyboardButton('😂 Экологический мем', callback_data='meme')
    markup.add(energy_calc, waste_info, tips, meme)
    
    msg2 = bot.send_message(call.message.chat.id, 
                         'Но ты можешь повлиять на эту проблему!\nВыбери, что тебя интересует:',
                         reply_markup=markup)
    
    save_message_id(call.message.chat.id, msg2.message_id)

# Меню калькулятора энергоэффективности
@bot.callback_query_handler(func=lambda call: call.data == 'calc_energy')
def energy_calculator(call):
    clear_user_messages(call.message.chat.id)
    state = get_user_state(call.message.chat.id)
    state['waiting_for_input'] = None
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    calc_now = telebot.types.InlineKeyboardButton('🧮 Рассчитать сейчас', callback_data='start_calc')
    back = telebot.types.InlineKeyboardButton('← Назад', callback_data='main_yes')
    markup.add(calc_now, back)
    
    msg = bot.send_message(call.message.chat.id,
                         '''💡 **Калькулятор энергоэффективности**

Оценим, сколько энергии ты можешь сэкономить дома:
• Лампочки накаливания → светодиодные
• Энергопотребление приборов
• Отопление и утепление

Нажми "Рассчитать сейчас" для начала расчета:''',
                         parse_mode='Markdown',
                         reply_markup=markup)
    
    save_message_id(call.message.chat.id, msg.message_id)

# Начало расчета
@bot.callback_query_handler(func=lambda call: call.data == 'start_calc')
def start_energy_calc(call):
    clear_user_messages(call.message.chat.id)
    state = get_user_state(call.message.chat.id)
    state['waiting_for_input'] = 'bulbs'
    state['calc_data'] = {}
    
    msg = bot.send_message(call.message.chat.id,
                         '''Введи количество лампочек накаливания в твоем доме:
(или напиши "0", если у тебя уже светодиодные)

_Напиши просто число, например: 10_''',
                         parse_mode='Markdown')
    
    save_message_id(call.message.chat.id, msg.message_id)

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_messages(message):
    state = get_user_state(message.chat.id)
    waiting_for = state.get('waiting_for_input')
    
    if waiting_for == 'bulbs':
        process_bulbs_input(message)
    elif waiting_for == 'hours':
        process_hours_input(message)
    else:
        # Если пользователь не в процессе калькулятора, но отправил текст
        # Проверяем, не является ли это командой
        if not message.text.startswith('/'):
            # Удаляем предыдущие сообщения и показываем стартовое меню
            clear_user_messages(message.chat.id)
            start_message(message)

# Обработка ввода количества лампочек
def process_bulbs_input(message):
    state = get_user_state(message.chat.id)
    
    try:
        bulbs = int(message.text)
        if bulbs < 0:
            raise ValueError
        
        state['calc_data']['bulbs'] = bulbs
        state['waiting_for_input'] = 'hours'
        
        # Удаляем предыдущие сообщения
        clear_user_messages(message.chat.id)
        
        msg = bot.send_message(message.chat.id,
                             f'''✅ Принято: {bulbs} лампочек

Теперь введи среднее количество часов в день, когда горит свет:
(например: 5 или 5.5)

_Введи число часов, можно с десятичной точкой_''',
                             parse_mode='Markdown')
        
        save_message_id(message.chat.id, msg.message_id)
        
    except ValueError:
        # Не очищаем все сообщения, только добавляем ошибку
        error_msg = bot.send_message(message.chat.id,
                                   "❌ Пожалуйста, введи целое положительное число!\n\nНапример: 8")
        save_message_id(message.chat.id, error_msg.message_id)

# Обработка ввода количества часов
def process_hours_input(message):
    state = get_user_state(message.chat.id)
    
    try:
        # Заменяем запятую на точку и преобразуем
        hours_text = message.text.replace(',', '.')
        hours = float(hours_text)
        
        if hours < 0 or hours > 24:
            raise ValueError
        
        bulbs = state['calc_data'].get('bulbs', 0)
        
        # Расчет экономии
        # Лампа накаливания 60Вт = светодиодная 8-10Вт
        old_power = bulbs * 60 * hours * 30  # Вт*ч в месяц
        new_power = bulbs * 9 * hours * 30   # Вт*ч в месяц
        economy_kwh = (old_power - new_power) / 1000
        
        # Стоимость электроэнергии ~5 руб/кВт*ч
        economy_rub = economy_kwh * 5
        co2_reduction = economy_kwh * 0.5  # кг CO2 на кВт*ч
        
        # Сбрасываем состояние ожидания
        state['waiting_for_input'] = None
        
        # Очищаем сообщения и показываем результат
        clear_user_messages(message.chat.id)
        
        # Формируем результат
        if bulbs == 0:
            result_text = f'''📊 **Результаты расчета:**

🎉 У тебя уже установлены светодиодные лампы!
Ты экономишь примерно {co2_reduction:.1f} кг CO₂ в месяц.

Продолжай в том же духе! 🌱'''
        else:
            trees = max(1, int(co2_reduction * 12 / 20))
            result_text = f'''📊 **Результаты расчета:**

💡 **Экономия на освещении:**
• Старые лампы: {bulbs} шт × 60Вт = {bulbs * 60}Вт
• Новые LED: {bulbs} шт × 9Вт = {bulbs * 9}Вт
• Часов в день: {hours}

💰 **Ежемесячная экономия:**
• Электроэнергия: {economy_kwh:.1f} кВт⋅ч
• Деньги: {economy_rub:.0f} руб
• CO₂: {co2_reduction:.1f} кг

🌍 **За год это:**
• {economy_rub*12:.0f} руб экономии
• {co2_reduction*12:.1f} кг меньше CO₂
(это как посадить {trees} дерево{'в' if trees > 1 else ''}!)'''

        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        back = telebot.types.InlineKeyboardButton('← Назад к меню', callback_data='main_yes')
        markup.add(back)
        
        msg = bot.send_message(message.chat.id, result_text,
                             parse_mode='Markdown',
                             reply_markup=markup)
        
        save_message_id(message.chat.id, msg.message_id)
        
    except ValueError:
        error_msg = bot.send_message(message.chat.id,
                                   "❌ Пожалуйста, введи число от 0 до 24!\n\nНапример: 6 или 6.5")
        save_message_id(message.chat.id, error_msg.message_id)

# [Остальной код остается без изменений - справочник отходов, эко-советы, мемы и т.д.]

# Справочник по сортировке отходов
@bot.callback_query_handler(func=lambda call: call.data == 'waste_types')
def waste_types_menu(call):
    clear_user_messages(call.message.chat.id)
    state = get_user_state(call.message.chat.id)
    state['waiting_for_input'] = None
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    # Группы отходов
    categories = [
        ('Пластик ♻️', 'plastic'),
        ('Стекло 🍶', 'glass'),
        ('Бумага 📄', 'paper'),
        ('Металл 🥫', 'metal'),
        ('Опасные ⚠️', 'hazardous'),
        ('Органика 🥗', 'organic'),
        ('Текстиль 👕', 'textile'),
        ('Электроника 📱', 'electronics'),
        ('Батарейки 🔋', 'batteries'),
        ('Лампочки 💡', 'lamps'),
        ('← Назад', 'main_yes')
    ]
    
    buttons = []
    for text, callback in categories:
        buttons.append(telebot.types.InlineKeyboardButton(text, callback_data=f'waste_{callback}'))
    
    # Распределяем кнопки по 2 в ряд
    for i in range(0, len(buttons), 2):
        if i+1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    
    msg = bot.send_message(call.message.chat.id,
                         '🗑️ **Справочник по сортировке отходов**\n\nВыбери категорию:',
                         parse_mode='Markdown',
                         reply_markup=markup)
    
    save_message_id(call.message.chat.id, msg.message_id)

# Обработчики для каждой категории отходов
@bot.callback_query_handler(func=lambda call: call.data.startswith('waste_'))
def show_waste_info(call):
    waste_type = call.data.split('_')[1]
    
    if waste_type == 'main':
        info_message(call)
        return
    
    clear_user_messages(call.message.chat.id)
    state = get_user_state(call.message.chat.id)
    state['waiting_for_input'] = None
    
    waste_info = {
        'plastic': '''♻️ **Пластик (маркировка 1, 2, 4, 5):**
• Бутылки от напитков (1 - PET)
• Упаковка от молока, йогуртов (2 - HDPE)
• Пакеты, плёнка (4 - LDPE)
• Контейнеры, крышки (5 - PP)

✅ **Как готовить:**
1. Сполоснуть
2. Снять этикетки
3. Сплющить
4. Сложить отдельно пакеты

🚫 **Не принимается:**
• Упаковка от майонеза/кетчупа (3 - PVC)
• Пенопласт (6 - PS)
• Смешанный пластик (7 - OTHER)''',
        
        'glass': '''🍶 **Стекло:**
• Бутылки от напитков
• Банки от консервов, детского питания
• Стеклянная тара

✅ **Как готовить:**
1. Сполоснуть
2. Удалить крышки/пробки
3. Не бить!

🚫 **Не принимается:**
• Керамика, фарфор
• Хрусталь
• Автостекло
• Зеркала''',
        
        'paper': '''📄 **Бумага и картон:**
• Газеты, журналы
• Картонные коробки
• Офисная бумага
• Книги (без твёрдых обложек)

✅ **Как готовить:**
1. Удалить скрепки, скотч
2. Расправить коробки
3. Сложить стопкой

🚫 **Не принимается:**
• Чеки, бумага для выпечки
• Ламинированная бумага
• Обои
• Грязная/жирная бумага''',
        
        'metal': '''🥫 **Металл:**
• Алюминиевые банки
• Консервные банки
• Крышки от банок
• Фольга (чистая)

✅ **Как готовить:**
1. Сполоснуть
2. Сплющить
3. Сложить отдельно алюминий и сталь

🚫 **Не принимается:**
• Баллончики из-под аэрозолей
• Металлические тюбики''',
        
        'hazardous': '''⚠️ **Опасные отходы:**
• Ртутные градусники
• Лекарства с истекшим сроком
• Химические средства
• Краски, лаки, растворители

✅ **Как поступать:**
1. Не выбрасывать в общий мусор!
2. Сдать в специальные пункты приёма
3. Узнать адреса: eco2.ru/recycling''',
        
        'organic': '''🥗 **Органические отходы:**
• Очистки овощей/фруктов
• Остатки пищи
• Чайная заварка, кофе
• Яичная скорлупа

✅ **Компостирование:**
1. Собирать в отдельное ведро
2. Использовать для компоста
3. Или биоразлагаемые пакеты

🚫 **Не компостировать:**
• Мясо, рыбу, кости
• Молочные продукты
• Жирные отходы''',
        
        'textile': '''👕 **Текстиль:**
• Одежда в хорошем состоянии
• Обувь (парами)
• Постельное бельё
• Полотенца

✅ **Как поступать:**
1. Постирать и высушить
2. Сдать в благотворительность
3. Или в контейнеры для текстиля

♻️ **Переработка:**
Изношенную одежду перерабатывают на:
• Тряпки для уборки
• Наполнители
• Новые ткани''',
        
        'electronics': '''📱 **Электроника:**
• Телефоны, планшеты
• Ноутбуки, компьютеры
• Наушники, кабели
• Бытовые приборы

✅ **Как поступать:**
1. Удалить личные данные
2. Сдать в магазины электроники
3. Или в специальные пункты

💰 **Можно получить скидку** на новую технику при сдаче старой!''',
        
        'batteries': '''🔋 **Батарейки и аккумуляторы:**
• Пальчиковые батарейки
• Кнопочные батарейки
• Аккумуляторы от телефонов
• Аккумуляторы от ноутбуков

⚠️ **Опасность:**
Одна батарейка загрязняет 20 м² земли!

✅ **Пункты приёма:**
• Магазины электроники
• Супермаркеты
• Отдельные контейнеры''',
        
        'lamps': '''💡 **Лампочки:**
• Энергосберегающие (люминесцентные)
• Светодиодные LED
• Галогенные

⚠️ **Энергосберегающие** содержат ртуть!

✅ **Как поступать:**
1. Аккуратно, не разбивая
2. Сдать в специальные пункты
3. Или в магазины стройматериалов

🚫 **Лампы накаливания** можно в общий мусор'''
    }
    
    if waste_type in waste_info:
        markup = telebot.types.InlineKeyboardMarkup()
        back = telebot.types.InlineKeyboardButton('← Назад к категориям', callback_data='waste_types')
        markup.add(back)
        
        msg = bot.send_message(call.message.chat.id,
                             waste_info[waste_type],
                             parse_mode='Markdown',
                             reply_markup=markup)
        
        save_message_id(call.message.chat.id, msg.message_id)

# Эко-советы
@bot.callback_query_handler(func=lambda call: call.data == 'eco_tips')
def eco_tips(call):
    clear_user_messages(call.message.chat.id)
    state = get_user_state(call.message.chat.id)
    state['waiting_for_input'] = None
    
    tips = '''💡 **Простые эко-советы на каждый день:**

🏠 **Дома:**
• Выключай свет, выходя из комнаты
• Закрывай кран при чистке зубов
• Используй многоразовые сумки
• Пей воду из фильтра, не покупай бутилированную

🛒 **Покупки:**
• Выбирай продукты без упаковки
• Покупай местные сезонные продукты
• Бери с собой контейнер для еды навынос
• Отказывайся от пластиковых трубочек

🚌 **Транспорт:**
• Ходи пешком на короткие расстояния
• Используй велосипед или самокат
• Пользуйся общественным транспортом
• Объединяй поездки на машине

💻 **Цифровая экология:**
• Очищай почту от спама
• Храни файлы в облаке, а не на устройстве
• Отправляй документы по email, не печатай
• Отписывайся от ненужных рассылок

🌱 **Начни с малого - планета скажет спасибо!**'''
    
    markup = telebot.types.InlineKeyboardMarkup()
    back = telebot.types.InlineKeyboardButton('← Назад', callback_data='main_yes')
    markup.add(back)
    
    msg = bot.send_message(call.message.chat.id, tips,
                         parse_mode='Markdown',
                         reply_markup=markup)
    
    save_message_id(call.message.chat.id, msg.message_id)

# Экологический мем
@bot.callback_query_handler(func=lambda call: call.data == 'meme')
def send_meme(call):
    clear_user_messages(call.message.chat.id)
    state = get_user_state(call.message.chat.id)
    state['waiting_for_input'] = None
    
    memes = [
        '''Когда забываешь выключить свет:
Планета: 🌍😭
Твой кошелёк: 💸😱

Когда сортируешь мусор:
Планета: 🌍😊
Будущее поколение: 👶❤️''',
        
        '''Эколог в ресторане:
- Можно без трубочки, пожалуйста.
Планета: 🌍👍
Черепаха: 🐢❤️''',
        
        '''Покупка многоразовой бутылки:
Сначала: 💸😒
Через месяц: 💰😏🌍
Через год: 🤑😎🌱'''
    ]
    
    import random
    meme = random.choice(memes)
    
    markup = telebot.types.InlineKeyboardMarkup()
    another = telebot.types.InlineKeyboardButton('😂 Ещё мем', callback_data='meme')
    back = telebot.types.InlineKeyboardButton('← Назад', callback_data='main_yes')
    markup.add(another, back)
    
    msg = bot.send_message(call.message.chat.id,
                         f'🌱 *Экологический мем дня:*\n\n{meme}',
                         parse_mode='Markdown',
                         reply_markup=markup)
    
    save_message_id(call.message.chat.id, msg.message_id)

# Обработка отказа
@bot.callback_query_handler(func=lambda call: call.data == 'main_no')
def say_for_no(call):
    bot.answer_callback_query(call.id)
    clear_user_messages(call.message.chat.id)
    state = get_user_state(call.message.chat.id)
    state['waiting_for_input'] = None
    
    msg = bot.send_message(call.message.chat.id, 
                         'Хорошо, нажми /start, если передумаешь! 🌍')
    
    save_message_id(call.message.chat.id, msg.message_id)

bot.polling(none_stop=True)
