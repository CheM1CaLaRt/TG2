import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from translate import Translator
from config import TOKEN
from aiogram.types import Message, FSInputFile
# Замените 'YOUR_API_TOKEN' на токен вашего Telegram-бота
API_TOKEN = TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаем папку img, если её нет
if not os.path.exists('img'):
    os.makedirs('img')

# Инициализация переводчика
translator = Translator(from_lang="russian", to_lang="english")

@dp.message(F.photo)
async def react_photo(message: Message):
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.reply("Фото сохранено!")


@dp.message(Command('send_voice'))
async def send_voice_message(message: Message):
    audio = FSInputFile("voice/1.ogg")
    await bot.send_voice(chat_id=message.chat.id, voice=audio)

@dp.message(Command('translate'))
async def translate_text(message: Message):
    text_to_translate = message.text[len('/translate '):]
    if not text_to_translate.strip():
        await message.reply("Вы не ввели текст для перевода.")
        return

    translated = translator.translate(text_to_translate)
    await message.reply(translated)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
