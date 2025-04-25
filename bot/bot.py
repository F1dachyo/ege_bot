import logging
import aiohttp
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8195396386:AAEJzOefLrJU5KVWBDlPMuB3ZHC3D89LkCQ"
API_TASK_URL = "http://localhost:8080/v1/task/10"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def fetch_task():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_TASK_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)
                    # Парсим задание из структуры ответа
                    task = (
                        data.get("200", {})
                            .get("content", {})
                            .get("application/json", {})
                            .get("example")
                    )
                    print(task)
                    return data
                else:
                    return "123"
        except Exception as e:
            logging.error(f"Ошибка при запросе задания: {e}")
            return "Hello"


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я НЕУЧИ-Бот "
        "Чтобы получить задание, отправь команду /task."
    )

async def send_task(chat_id: int):
    task = await fetch_task()
    if task is None:
        await message.answer("Не удалось получить задание. Попробуйте позже.")
        return

    # Формируем строку задания по списку токенов
    tokens = task.get("tokens", [])
    task_text = "".join(
        ("__" if token.get("isBlank") else token.get("text", ""))
        for token in tokens
    )

    prompt = task.get("prompt") or ""
    message_text = (
        f"Задание #{task.get('id')}\n\n{prompt}{task_text}\n\n"
        "Выбери правильный вариант ответа:"
    )

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row_width = 2
    for answer in task.get("answers", []):
        btn_text = answer.get("text")
        callback_data = f"answer:{task.get('id')}:{answer.get('id')}:{answer.get('isCorrect')}"
        kb_builder.button(text=btn_text, callback_data=callback_data)

    kb = kb_builder.as_markup()
    await bot.send_message(chat_id, message_text, reply_markup=kb)

@dp.message(Command("task"))
async def cmd_task(message: types.Message):
    await send_task(message.chat.id)


    # kb = types.InlineKeyboardMarkup(row_width=2)
    # for answer in task.get("answers", []):
    #     btn_text = answer.get("text")
    #     # Формируем callback_data в формате "answer:{task_id}:{answer_id}:{isCorrect}"
    #     callback_data = f"answer:{task.get('id')}:{answer.get('id')}:{answer.get('isCorrect')}"
    #     kb.add(types.InlineKeyboardButton(text=btn_text, callback_data=callback_data))
    #
    # await message.answer(message_text, reply_markup=kb)


@dp.callback_query(lambda callback: callback.data and callback.data.startswith("answer:"))
async def process_answer(callback: types.CallbackQuery):
    try:
        _, task_id, answer_id, is_correct_str = callback.data.split(":")
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    is_correct = is_correct_str == "True"
    result_text = "Правильно! 🎉" if is_correct else "Неправильно! 😕"

    await callback.answer()
    await callback.message.answer(result_text)

  
    await send_task(callback.message.chat.id)

async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())