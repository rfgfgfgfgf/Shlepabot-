import telebot
import requests
from  config import token, weather_api_key
from random import choice

print("бот готов")
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Шлепа бот. Мой создатель - rfgfgfgfgf. Мои команды: /help, /start, /coin, /weather")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Привет, проверь мои команды: /help, /start, /coin, /weather')
    

@bot.message_handler(commands=['weather'])
def weather_handler(message):

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Пожалуйста укажите город в одном сообщение после команды.")
        return
    city = ' '.join(args[1:])
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=ru"
    
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] != 200:
        bot.reply_to(message, f"Не удалось найти город {city}. Пожалуйста проверьте название и попробуйте снова.")
        return
    
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    
    weather_info = (
        f"Погода в городе {city}:\n"
        f"Температура: {temperature}°C\n"
        f"Влажность: {humidity}%\n"
        f"Скорость ветра: {wind_speed} м/с"
    )
    
    bot.reply_to(message, weather_info)

@bot.message_handler(commands=['coin'])
def coin_handler(message):
    msg = bot.reply_to(message, "Какую монету вы выбираете: ОРЕЛ или РЕШКА?")
    bot.register_next_step_handler(msg, process_coin_choice)


def process_coin_choice(message):
    user_choice = message.text.strip().upper()

    if user_choice not in ["ОРЕЛ", "РЕШКА"]:
        bot.reply_to(message, "Пожалуйста, выберите: ОРЕЛ или РЕШКА.")
        return
    
    result = choice(["ОРЕЛ", "РЕШКА"])
    
    if result == user_choice:
        bot.reply_to(message, f"Вы выбрали {user_choice}, и выпал {result}! Вы угадали!")
    else:
        bot.reply_to(message, f"Вы выбрали {user_choice}, а выпал {result}. Не угадали!")   

bot.infinity_polling()
