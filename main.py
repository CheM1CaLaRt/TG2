import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, Weather_API

# Замените 'YOUR_API_TOKEN' на токен вашего Telegram-бота
API_TOKEN = TOKEN
# Замените 'YOUR_OPENWEATHERMAP_API_KEY' на ваш ключ API OpenWeatherMap
WEATHER_API_KEY = Weather_API

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привет! Я бот для получения прогноза погоды. Введите /help для получения списка доступных команд.")

# Обработчик команды /help
@dp.message(Command(commands=['help']))
async def send_help(message: Message):
    await message.reply("Доступные команды:\n/start - Запуск бота\n/help - Список команд\n/weather <город> - Прогноз погоды для указанного города")

# Обработчик команды /weather
@dp.message(Command(commands=['weather']))
async def get_weather(message: Message):
    try:
        # Получаем название города из сообщения
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Пожалуйста, укажите город после команды /weather")
            return
        city = args[1]

        # Формируем URL для запроса к API OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            await message.reply(f"Не удалось получить данные для города {city}. Пожалуйста, проверьте название города.")
            return

        # Извлекаем данные из ответа
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Формируем и отправляем сообщение с прогнозом погоды
        weather_message = (
            f"Погода в городе {city_name}:\n"
            f"Температура: {temp}°C\n"
            f"Описание: {weather_description}\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        await message.reply(weather_message)
    except Exception as e:
        logging.exception(e)
        await message.reply("Произошла ошибка при получении данных о погоде. Пожалуйста, попробуйте еще раз позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
