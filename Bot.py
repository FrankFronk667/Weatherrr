import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from weather import get_weather


TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("weather"))
async def weather_command(message: types.Message):
    text = message.text.replace("/weather", "").strip()

    if not text:
        await message.answer(
            "Напиши город после команды.\n\n"
            "Пример:\n/weather Нытва\n/weather Пермь"
        )
        return

    result = await get_weather(text)

    await message.answer(result)


@dp.message()
async def help_message(message: types.Message):
    await message.answer(
        "🌦 Погодный бот\n\n"
        "Используй:\n"
        "/weather Город\n\n"
        "Пример:\n"
        "/weather Нытва"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
