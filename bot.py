import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

API_TOKEN = 'YOUR_API_TOKEN_HERE'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# User data storage
user_profiles = {}
user_farms = {}
user_businesses = {}
user_gardens = {}
marriages = {}
user_clans = {}

# Start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_profiles:
        user_profiles[user_id] = {"balance": 100, "properties": [], "referrals": []}
    await message.reply("Добро пожаловать в RPG Game Bot! Используйте /profile для просмотра вашего профиля.")

# Profile command
@dp.message_handler(commands=['profile'])
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    profile = user_profiles.get(user_id, {"balance": 0, "properties": [], "referrals": []})
    await message.reply(f"Баланс: {profile['balance']}\nИмущество: {', '.join(profile['properties'])}\nРефералы: {len(profile['referrals'])}")

# Referral system
@dp.message_handler(commands=['refer'])
async def refer_user(message: types.Message):
    user_id = message.from_user.id
    referral_link = f"https://t.me/your_bot_name?start={user_id}"
    await message.reply(f"Ваша реферальная ссылка: {referral_link}\nПриглашайте друзей и получайте бонусы!")

@dp.message_handler(commands=['referrals'])
async def show_referrals(message: types.Message):
    user_id = message.from_user.id
    referrals = user_profiles.get(user_id, {}).get("referrals", [])
    await message.reply(f"Ваши рефералы: {', '.join(referrals)}")

# Bank commands
@dp.message_handler(commands=['deposit'])
async def deposit_money(message: types.Message):
    user_id = message.from_user.id
    try:
        amount = int(message.get_args())
        user_profiles[user_id]['balance'] += amount
        await message.reply(f"Вы пополнили баланс на {amount}. Новый баланс: {user_profiles[user_id]['balance']}")
    except ValueError:
        await message.reply("Используйте команду так: /deposit [сумма]")

@dp.message_handler(commands=['withdraw'])
async def withdraw_money(message: types.Message):
    user_id = message.from_user.id
    try:
        amount = int(message.get_args())
        if user_profiles[user_id]['balance'] >= amount:
            user_profiles[user_id]['balance'] -= amount
            await message.reply(f"Вы сняли {amount}. Новый баланс: {user_profiles[user_id]['balance']}")
        else:
            await message.reply("Недостаточно средств на балансе.")
    except ValueError:
        await message.reply("Используйте команду так: /withdraw [сумма]")

# Crypto farm commands
@dp.message_handler(commands=['start_farm'])
async def start_farm(message: types.Message):
    user_id = message.from_user.id
    user_farms[user_id] = {"start_time": datetime.now(), "active": True}
    await message.reply("Вы начали майнинг криптовалюты. Используйте /collect_farm для сбора.")

@dp.message_handler(commands=['collect_farm'])
async def collect_farm(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_farms and user_farms[user_id]["active"]:
        start_time = user_farms[user_id]["start_time"]
        elapsed_time = (datetime.now() - start_time).seconds // 60  # Время в минутах
        earnings = elapsed_time * 10  # Примерный доход
        user_profiles[user_id]['balance'] += earnings
        await message.reply(f"Вы собрали {earnings} криптовалюты. Новый баланс: {user_profiles[user_id]['balance']}")
        user_farms[user_id]["start_time"] = datetime.now()  # Обновляем время начала
    else:
        await message.reply("У вас нет активной фермы.")

# Game commands
@dp.message_handler(commands=['spin'])
async def spin_game(message: types.Message):
    user_id = message.from_user.id
    try:
        bet = int(message.get_args())
        if user_profiles[user_id]['balance'] >= bet:
            result = random.choice(['win', 'lose'])
            if result == 'win':
                winnings = bet * 2
                user_profiles[user_id]['balance'] += winnings
                await message.reply(f"Вы выиграли {winnings}! Новый баланс: {user_profiles[user_id]['balance']}")
            else:
                user_profiles[user_id]['balance'] -= bet
                await message.reply(f"Вы проиграли {bet}. Новый баланс: {user_profiles[user_id]['balance']}")
        else:
            await message.reply("Недостаточно средств для ставки.")
    except ValueError:
        await message.reply("Используйте команду так: /spin [сумма]")

# Business commands
@dp.message_handler(commands=['my_business'])
async def my_business(message: types.Message):
    user_id = message.from_user.id
    business = user_businesses.get(user_id, "У вас нет бизнеса.")
    await message.reply(f"Ваш бизнес: {business}")

@dp.message_handler(commands=['sell_business'])
async def sell_business(message: types.Message):
    await message.reply("Эта функция временно недоступна.")

@dp.message_handler(commands=['my_generator'])
async def my_generator(message: types.Message):
    user_id = message.from_user.id
    generator = user_businesses.get(user_id, "У вас нет генератора.")
    await message.reply(f"Ваш генератор: {generator}")

@dp.message_handler(commands=['sell_generator'])
async def sell_generator(message: types.Message):
    await message.reply("Эта функция временно недоступна.")

# Garden commands
@dp.message_handler(commands=['my_garden'])
async def my_garden(message: types.Message):
    user_id = message.from_user.id
    garden = user_gardens.get(user_id, "У вас нет сада.")
    await message.reply(f"Ваш сад: {garden}")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
