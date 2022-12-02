import logging
from aiogram import Bot, Dispatcher, executor, types
import exceptions
import expenses
from button import button_client
from categories import Categories


logging.basicConfig(level=logging.INFO)

API_TOKEN ='5618822636:AAGqAjIuf9PkvkCjPdFB2atNTOa1q6--Mzk'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(lambda m: m.text in ['/start', 'start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: Например, напиши 15 магазин\n"
        "Сегодняшняя статистика: /today\n"
        "За текущий месяц: /month\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories", reply_markup= button_client)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Все, удалил"
    await message.answer(answer_message)


@dp.message_handler(lambda m: m.text in ['/categories', 'categories'])
async def categories_list(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(lambda m: m.text in ['/today', 'today'])
async def today_statistics(message: types.Message):
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(lambda m: m.text in ['/month', 'month'])
async def month_statistics(message: types.Message):
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(lambda m: m.text in ['/expenses', 'expenses'])
async def list_expenses(message: types.Message):
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* "\
            .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)