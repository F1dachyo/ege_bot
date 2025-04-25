import logging
import asyncio
import os
import random

import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурационные переменные (замените на свои)
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_API_URL = "http://api:8080"  # Базовый URL вашего API

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def init_user(telegram_id: int):
    """
    Инициализация пользователя.
    Выполняет POST запрос на /v1/user/init/{telegram_id}
    """
    url = f"{BASE_API_URL}/v1/user/init/{telegram_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)
                    logging.info(f"User init response: {data}")
                    return data
                else:
                    logging.error(f"Ошибка инициализации (status {response.status})")
                    return None
        except Exception as e:
            logging.error(f"Exception в init_user: {e}")
            return None


async def get_task_by_ex(ex_id: int, tg_id: int = -1):
    """
    Запрашивает задание для упражнения с номером ex_id: GET /v1/task/{ex_id}.
    Предполагается, что API возвращает JSON с описанием задания.
    """
    if ex_id == 13:
        url = f"{BASE_API_URL}/v1/task/mistake/{tg_id}"
    else:
        url = f"{BASE_API_URL}/v1/task/{ex_id}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Если API возвращает данные с вложенной структурой, можно делать:
                    # task = data.get("200", {}).get("content", {}).get("application/json", {}).get("example")
                    # При необходимости заменим на data, если структура другая:
                    return data
                else:
                    if tg_id != -1:
                        return "OK"
                    logging.error(f"Ошибка запроса задания (status {resp.status})")
                    return None
        except Exception as e:
            logging.error(f"Exception в get_task_by_ex: {e}")
            return None


async def report_mistake(tg_id: int, task_id: int, task_type: int):
    """
    Сохраняет ошибку пользователя.
    Выполняется POST запрос на /v1/task/mistake/{tg_id}/{task_id}/{task_type}
    """
    url = f"{BASE_API_URL}/v1/task/mistake/{tg_id}/{task_id}/{task_type}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url) as resp:
                if resp.status == 204:
                    data = await resp.json()
                    logging.info(f"Ошибка сохранена: {data}")
                    return data
                else:
                    logging.error(f"Ошибка сохранения ошибки (status {resp.status})")
                    return None
        except Exception as e:
            logging.error(f"Exception в report_mistake: {e}")
            return None

async def update_statistic(tg_id: int, status_answer: bool):
    url = f"{BASE_API_URL}/v1/user/update.statistic/{tg_id}/{status_answer}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url) as resp:
                if resp.status == 204:
                    logging.info(f"Обновлена статистика для пользователя: {tg_id}")
                else:
                    logging.error(f"Не удалось изменить статистику пользователя {tg_id}: {resp.status}")
                    return None
        except Exception as e:
            logging.error(f"Exception: {e}")
            return None


async def get_stat(tg_id: int):
    url = f"{BASE_API_URL}/v1/user/statistic/{tg_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    return None
        except Exception as e:
            logging.error(f"Exception в report_mistake: {e}")
            return None


async def send_task_by_ex(chat_id: int, ex_id: int, tg_id:int):
    """
    Получает задание для выбранного упражнения (ex_id) и отправляет задание пользователю.
    Формирует текст задания и инлайн-клавиатуру с вариантами ответа.
    В callback_data включаются:
      "answer:{ex_id}:{task_id}:{answer_id}:{isCorrect}:{task_type}"
    """
    task = await get_task_by_ex(ex_id, tg_id)
    if isinstance(task, list):
        task = task[random.randint(0, len(task) - 1)]
    if isinstance(task, str):
        await bot.send_message(chat_id, "Практика завершена. Все ошибки проработаны. ДЛя выхода в главное меню"
                                        "пропишите /start")
    if task is None:
        await bot.send_message(chat_id, "Не удалось получить задание. Попробуйте позже.")
        return

    # Формирование текста задания:
    # Если задание содержит список токенов, выводим "____" вместо пропусков.
    tokens = task.get("tokens", [])
    task_text = "".join("____" if token.get("isBlank") else token.get("text", "") for token in tokens)
    prompt = task.get("prompt") or ""
    message_text = (
        f"Задание #{task.get('id')}\n\n{prompt}{task_text}\n\n"
        "Выбери правильный вариант ответа:"
    )
    global message_count, ad_target
    message_count += 1  # Увеличиваем счётчик при каждом полученном сообщении
    print("MESSAGES", message_count, ad_target)
    # Если достигли порога, отправляем рекламное сообщение
    if message_count >= ad_target:
        index = random.randint(0, 1)
        ad_text = [ "> Получи грант на обучение до 2\\.8 млн ₽\\.\n>[Подробнее](https://centraluniversity\\.ru/)",
                    "Стань востребованным специалистом, поступай в ВШЭ"][index]
        ad_picture = ["https://static31.tgcnt.ru/posts/_0/3d/3dbe5b222d677ba4c693da8490b531b1.jpg",
                      "https://irposakha14.ru/wp-content/uploads/2022/08/niu-vshe.jpg"][index]

        await bot.send_message(chat_id, ad_text, link_preview_options=types.LinkPreviewOptions(
                url=ad_picture),
            parse_mode="MarkdownV2")

        # Сбрасываем счётчик и выбираем новый случайный порог
        message_count = 0
        ad_target = random.randint(5, 10)

    # Построение клавиатуры для вариантов ответа
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row_width = 2
    kb_builder.adjust(1)
    task_type = task.get("type", "unknown")
    for answer in task.get("answers", []):
        btn_text = answer.get("text", "")
        # Формируем callback_data с информацией о выбранном упражнении и задании
        callback_data = f"answer:{ex_id}:{task.get('id')}:{answer.get('id')}:{answer.get('isCorrect')}:{task_type}"
        kb_builder.button(text=btn_text, callback_data=callback_data)
    kb = kb_builder.as_markup()
    await bot.send_message(chat_id, message_text, reply_markup=kb)

@dp.message(Command("profile"))
async def get_profile(message: types.Message):
    profile_data = await get_stat(message.from_user.id)
    streak = profile_data.get("streak")
    all_answers = profile_data.get("all_answers")
    right_answers = profile_data.get("right_answers")
    await message.answer(f"Статистика профиля:\nСерия побед:{streak}\nРешено заданий:{all_answers}\nРешено верно:{right_answers}")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start.
    Инициализирует пользователя и предлагает выбор задания ("9 задание" или "10 задание").
    """
    telegram_id = message.from_user.id
    print("not init")
    await init_user(telegram_id)
    print("int")

    # Формируем клавиатуру с кнопками для выбора номера задания
    kb_builder = InlineKeyboardBuilder()

    # При нажатии, callback_data в формате "ex:{ex_id}"
    kb_builder.button(text="4 задание", callback_data="ex:4")
    kb_builder.button(text="9 задание", callback_data="ex:9")
    kb_builder.button(text="10 задание", callback_data="ex:10")
    kb_builder.button(text="11 задание", callback_data="ex:11")
    kb_builder.button(text="12 задание", callback_data="ex:12")
    kb_builder.button(text="Работа над ошибками", callback_data="ex:13")
    kb_builder.adjust(1)
    kb = kb_builder.as_markup()

    await message.answer("Выберите задание:", reply_markup=kb)


@dp.callback_query(lambda q: q.data and q.data.startswith("ex:"))
async def ex_selection(callback: types.CallbackQuery):
    """
    Обработчик выбора упражнения (9 или 10).
    После нажатия на кнопку происходит запрос задания по выбранному ex_id.
    """
    try:
        _, ex_id_str = callback.data.split(":")
        ex_id = int(ex_id_str)
    except Exception as e:
        await callback.answer("Ошибка при выборе задания.", show_alert=True)
        return

    await callback.answer()  # Убираем "часики"
    await send_task_by_ex(callback.message.chat.id, ex_id, callback.from_user.id)


@dp.callback_query(lambda q: q.data and q.data.startswith("answer:"))
async def process_answer(callback: types.CallbackQuery):
    """
    Обработка ответа пользователя.
    Callback_data имеет формат:
      "answer:{ex_id}:{task_id}:{answer_id}:{isCorrect}:{task_type}"
    Если ответ неверный – сохраняем ошибку через POST запрос.
    Затем отправляем ответ (результат) и сразу запрашиваем новое задание по тому же ex_id.
    """
    try:
        parts = callback.data.split(":")
        if len(parts) < 6:
            raise ValueError("Неверный формат данных.")
        # Распаковываем значения
        _, ex_id_str, task_id_str, answer_id_str, is_correct_str, task_type = parts
        ex_id = int(ex_id_str)
        task_id = int(task_id_str)
        is_correct = is_correct_str == "True"
    except Exception as e:
        await callback.answer("Некорректные данные.", show_alert=True)
        return


    if is_correct:
        result_text = "Правильно! 🎉"
        await update_statistic(callback.from_user.id, True)
    else:
        result_text = "Неправильно! 😕"
        await update_statistic(callback.from_user.id, False)
        # Сохраняем ошибку: POST /v1/task/mistake/{tg_id}/{task_id}/{task_type}
        await report_mistake(callback.from_user.id, task_id, ex_id)

    await callback.answer()  # Убираем "часики" после нажатия
    await callback.message.answer(result_text)


    await send_task_by_ex(callback.message.chat.id, ex_id, callback.from_user.id)


ad_target = random.randint(5, 10)
message_count = 0


if __name__ == "__main__":
    from asyncio import run
    run(dp.start_polling(bot))