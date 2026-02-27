import telebot
import requests

TOKEN = "8581787981:AAGyhvRO-iWyQ38fFjbnDWTZk8cDIActOPQ"
API_KEY = "657a2c5e5eb06d506c034369a63386d9"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🌍 Напиши название города\nПример: Navoi, Tashkent, London"
    )

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text.strip()

    # Используем глобальный поиск по миру
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            bot.send_message(message.chat.id, "❌ Город не найден. Попробуй на английском.")
            return

        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        weather_text = (
            f"🌍 {city_name}, {country}\n\n"
            f"🌡 Температура: {temp}°C\n"
            f"🤔 Ощущается: {feels}°C\n"
            f"☁️ Погода: {description}\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind} м/с"
        )

        bot.send_message(message.chat.id, weather_text)

    except Exception as e:
        bot.send_message(message.chat.id, "⚠ Ошибка соединения с сервером.")

bot.infinity_polling()