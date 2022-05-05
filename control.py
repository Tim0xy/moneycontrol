#money controll by 0xy, ver-0.1
import locale
import json
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, CallbackQuery
from aiogram.types import (
	ReplyKeyboardMarkup,
	KeyboardButton,
	InlineKeyboardButton,
	InlineKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, Dispatcher, types, executor
from keyboard import *
from config import *

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

print("Bot start")

class controller(StatesGroup):
	coin = State()
	coin_m = State()
	coin_d = State()

money = 0
dream = False

##################################
debug = False
##################################

if debug:
	data = [0, 0, False]
	with open("data.json", "w") as file:
		file.write(json.dumps(data, indent=4))

@dp.message_handler(commands=['start'])
async def starter(msg: types.Message):
	await bot.send_sticker(chat_id=msg.from_user.id, sticker = r"CAACAgIAAxkBAAEEQxtiPe2MidgpQVxLm9NU3X30AAGEpm4AAgMBAAJWnb0KAuXReIfl-k8jBA")
	await msg.answer('Привет, тут ты можешь контролировать расходы.', reply_markup= menu())

@dp.message_handler(text="ℹ️ Инфо")
async def starter(msg: types.Message):
	with open("data.json", "r", encoding="utf-8") as file:
		money = json.load(file)
	dream = money[2]
	if dream:
		await msg.answer(f"💰Сейчас у вас есть: <b>{money[0]}</b> руб.\nЦель: <b>{money[1]}</b> руб.", reply_markup=info())
	else:
		await msg.answer(f"💰Сейчас у вас есть: <b>{money[0]}</b> руб.", reply_markup= info())

@dp.message_handler(Text(equals="✖️ Отмена"), state="*")
async def menu_button(message: types.Message, state: FSMContext):
	await state.finish()
	await bot.send_message(
		message.chat.id, "Операция отменена", reply_markup=menu()
	)

# Сброс накопления
@dp.message_handler(commands=['clear0088'])
async def starter(msg: types.Message):
	with open("data.json", "r", encoding="utf-8") as file:
		money = json.load(file)
	print(f"Сброшено: {money[0]}")
	money[0] = 0
	with open("data.json", "w") as file:
		file.write(json.dumps(money, indent=4))
	await msg.answer(f"🗑Накопления очищены")
	with open("data.json", "r", encoding="utf-8") as file:
		money = json.load(file)
	if dream:
		await msg.answer(f"💰Сейчас у вас есть: <b>{money[0]}</b> руб.\nЦель: <b>{money[1]}</b> руб.")
	else:
		await msg.answer(f"💰Сейчас у вас есть: <b>{money[0]}</b> руб.")
	

# Добавление в сумму
@dp.message_handler(Text(equals="➕ Добавить"), state="*")
async def coin(message: types.Message, state: FSMContext):
	print("0 state")
	await message.answer(f"Введите сумму для добавления:", reply_markup=cancel())
	await controller.coin.set()
@dp.message_handler(state=controller.coin, content_types=types.ContentTypes.TEXT)
async def all_coin(message: types.Message, state: FSMContext):
	money = float(message.text.replace(",", "."))
	print(money)
	print("1 state")
	with open("data.json", "r", encoding="utf-8") as file:
		saved_money = json.load(file)
	upd_money = money + saved_money[0]
	saved_money[0] = upd_money
	with open("data.json", "w") as file:
		file.write(json.dumps(saved_money, indent=4))
		print(upd_money)
	await message.answer(f"💵Вы добавили <b>{money}</b> руб.\n\n На данный момент накоплено: <b>{upd_money}</b> руб.", reply_markup= menu())
	await state.update_data(name=money)
	await state.finish()

@dp.message_handler(Text(equals="✖️ Отмена"), state="*")
async def menu_button(message: types.Message, state: FSMContext):
	await state.finish()
	await bot.send_message(
		message.chat.id, "Операция отменена", reply_markup=menu()
	)

# Вычитание из суммы
@dp.message_handler(Text(equals="➖ Вычесть"), state="*")
async def coin(message: types.Message, state: FSMContext):
	print("0 state-")
	await message.answer(f"Введите сумму для вычитания:", reply_markup=cancel())
	await controller.coin_m.set()
@dp.message_handler(state=controller.coin_m, content_types=types.ContentTypes.TEXT)
async def all_coin(message: types.Message, state: FSMContext):
	saved_money = 0
	money = float(message.text.replace(",", "."))
	print(money)
	print("1 state-")
	with open("data.json", "r", encoding="utf-8") as file:
		saved_money = json.load(file)
	upd_money = saved_money[0] - money
	saved_money[0] = upd_money
	with open("data.json", "w") as file:
		file.write(json.dumps(saved_money, indent=4))
		print(upd_money)
	await message.answer(f"💶Вы потратили: <b>{money}</b> руб.\n\n На данный момент накоплено: <b>{upd_money}</b> руб.", reply_markup= menu())
	await state.update_data(name=money)
	await state.finish()

# Кнопка назад
@dp.message_handler(text="Назад")
async def starter(msg: types.Message):
	await msg.answer('Возвращение',reply_markup=menu())

# Цель
@dp.message_handler(text="Цель")
async def starter(msg: types.Message):
	with open("data.json", "r", encoding="utf-8") as file:
		money = json.load(file)
	dream = money[2]
	if dream:
		if money[1] > money[0]:
			await msg.answer(f"Накопленно: <b>{money[0]}</b> из <b>{money[1]}</b>\nОсталось накопить: <b>{money[1] - money[0]}</b>")
		else:
			await msg.answer(f"Вы накопили больше чем вам нужно!\nНакопленно: <b>{money[0]}</b> из <b>{money[1]}</b>\nОстаток: <b>{money[0] - money[1]}</b>")
	else:
		await msg.answer(f"У вас не установленна цель!\nУстоновка цели: /target")

# Установка цели
@dp.message_handler(commands=['target'], state="*")
async def coin(message: types.Message, state: FSMContext):
	print("0 state_dream")
	await message.answer(f"Введите сумму которую хотите накопить:", reply_markup=cancel())
	await controller.coin_d.set()
@dp.message_handler(state=controller.coin_d, content_types=types.ContentTypes.TEXT)
async def all_coin(message: types.Message, state: FSMContext):

	if message.text == "✖️ Отмена":
		await state.finish()
		await bot.send_message(message.chat.id, "Операция отменена", reply_markup=menu())
	money = float(message.text.replace(",", "."))
	print(money)
	print("1 state_dream")
	dream = True
	with open("data.json", "r", encoding="utf-8") as file:
		dream_money = json.load(file)
	dream_money[1] = money
	dream_money[2] = dream
	with open("data.json", "w") as file:
		file.write(json.dumps(dream_money, indent=4))
	await message.answer(f"Вы установили цель: <b>{dream_money[1]}</b> руб.", reply_markup= menu())
	print(dream)
	await state.update_data(name=money)
	await state.finish()



if __name__ == "__main__":
	#main()

	while True:
		try:
			executor.start_polling(dp)
		except Exception as e:
			print('Ошибка -', e)