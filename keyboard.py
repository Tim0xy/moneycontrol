from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def menu():
	add_button = KeyboardButton('➕ Добавить')
	lose_button = KeyboardButton('➖ Вычесть')
	info_button = KeyboardButton('ℹ️ Инфо')
	back_info_button = KeyboardButton('Назад')
	menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	menu_kb.add(info_button)
	menu_kb.row(add_button, lose_button)

	return menu_kb

	print(menu_kb)
def info():
	back_info_button = KeyboardButton('Назад')
	dream_button = KeyboardButton('Цель')
	info_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	info_menu.row(dream_button, back_info_button)

	return info_menu
def cancel():
	cansel_button = KeyboardButton('✖️ Отмена')
	cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	cancel_menu.add(cansel_button)

	return cancel_menu
