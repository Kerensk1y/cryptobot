import telebot
from telebot import types
import config
import requests
import json
import random
import time

print('in progress...')
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    sticker = open('sticks/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    
    #keybord
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Что ты умеешь?")

    markup.add(item1)
    
    bot.send_message(message.chat.id,"Приветствую, {0.first_name}! Позвольте представиться.\nМеня зовут {1.first_name}. С превеликим удовольствием готов вам помочь 👨‍💻".format(message.from_user,bot.get_me()),
    parse_mode='html', reply_markup=markup)
        
@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Что ты умеешь?':
            
            markup=types.InlineKeyboardMarkup(row_width=2)
            item1=types.InlineKeyboardButton("Хорошо! Можешь начинать", callback_data='on')
            item2=types.InlineKeyboardButton("Пока не нужно ", callback_data='off')
            
            markup.add(item1,item2)
            
            bot.send_message(message.chat.id, 'Умею подсказывать курс крипты каждый час. Предлагаю начать! 🤠', reply_markup=markup)
          
        else: bot.send_message(message.chat.id, 'Не знаю что и ответить 😅')
 
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'on':
    
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1=types.KeyboardButton("Я сплю, не присылай 😴", callback_data='off')
                item2=types.KeyboardButton("Актуальный курс ⏱")
                item3=types.KeyboardButton("Настройки ⚙️")   
                
                markup.add(item1,item2,item3)
                while call.data == 'off':
                    b = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd').text
                    b = json.loads(b)
                    btc = int (b['bitcoin']['usd'])

                    e = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd').text
                    e = json.loads(e)
                    eth = int (e['ethereum']['usd'])
                    bot.send_message(call.message.chat.id,'Bitcoin: ' + str(btc) + ' usd\nEthereum: ' + str(eth) + ' usd', reply_markup=markup)
                    time.sleep(3600) 
                bot.send_message(message.chat.id, 'Ок, замолкаю. Напишете, как понадоблюсь 🤐')
                                  
            elif call.data == 'off':
                    
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1=types.KeyboardButton("Актуальный курс ⏱")
                item2=types.KeyboardButton("Просыпайся, пора работать 😎")
                markup.add(item1, item2)
                bot.send_message(call.message.chat.id,'Хорошо, не будем спешить', reply_markup=markup)
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Умею подсказывать курс крипты каждый час.",
                reply_markup=None)
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
 
    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)

 #sti = open('sticks/sticker1.webp', 'rb')
           #     bot.send_sticker(message.chat.id, sti)

           #sticker = open('sticks/sticker3.webp', 'rb')
                #bot.send_sticker(message.chat.id, sticker)
                
                
