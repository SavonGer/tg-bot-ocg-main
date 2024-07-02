import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Filter
from aiogram.filters import CommandStart
from aiogram.types import Message, LinkPreviewOptions, FSInputFile, KeyboardButton, ReplyKeyboardMarkup

TOKEN = "6768737174:AAFIVNAzdlY-z5CY91uysjTr4fLhQuLpOyE"

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

kb = [
    [KeyboardButton(text="Статья 📃")],
    [KeyboardButton(text="Контакты ✉")]
]

keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Жми на кнопки! ☺")


class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    cap = f"Приветствую, {html.bold(message.from_user.full_name)}! Это бот на тему:\n " \
          f"<i>\"Как оценить надежность и качество онлайн-магазинов перед совершением покупки\"</i>\n\n" \
          f"Доступные команды (кликабельно):\n" \
          f"1. /start - стартовое сообщение\n" \
          f"2. /info - получить информацию по теме\n" \
          f"3. /contacts - список людей, работавших над проектом\n\n" \
          f"Продолжим? ☺"
    await message.answer_photo(photo=FSInputFile("img/start.jpg"), caption=cap, reply_markup=keyboard)


@dp.message(MyFilter("/info"))
@dp.message(MyFilter("Статья 📃"))
async def echo_handler(message: Message) -> None:
    cap = "Рекомендации о том, как оценить надежность интернет магазина, занимают <b>слишком много</b> места 🙌 " \
          "поэтому предлагаю вам перейти по ссылке на соответствующую статью 📄:\n\n" \
          "<a href=\"https://telegra.ph/Kak-ocenit-nadezhnost-internet-magazina-pered-pokupkoj-06-24\">Перейти к " \
          "статье ✅</a> "
    link = LinkPreviewOptions(url="https://telegra.ph/Kak-ocenit-nadezhnost-internet-magazina-pered-pokupkoj-06-24",
                              prefer_large_media=True)
    await message.answer(text=cap, LinkPreviewOptions=link, reply_markup=keyboard)


@dp.message(MyFilter("/contacts"))
@dp.message(MyFilter("Контакты ✉"))
async def echo_handler(message: Message) -> None:
    cap = "Над ботом работал Герман Савелий Б5123-58.03.01 😉\n" \
          "Связаться со мной: german.sv@students.dvfu.ru"
    await message.answer_photo(photo=FSInputFile("img/contacts.jpg"), caption=cap, reply_markup=keyboard)


@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer(text="Используйте только разрешенные команды ❌!\nПерейти в меню: /start")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
