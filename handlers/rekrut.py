from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher, asyncio
from bot import dp, bot
from aiogram.dispatcher.filters import Text
from markups import inline, keyboards
from data_base import rekruter_data



class FSMlead(StatesGroup):
	name = State()
	town = State()
	age = State()
	phone = State()


async def firs_event(message : types.Message):
	await FSMlead.name.set()
	await message.reply("Привет, меня зовут Артём, я представляю компанию Style-models, хочу познакомить тебя с нашей вакансией.\nКак я могу к тебе обращаться?")


async def name_lead(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
	await FSMlead.next()
	await message.reply("В наш дружный коллектив, требуются будущие и действующие модели. Если опыта работы у тебя нет, ничего страшного.Мы хотим научить тебя и даже заплатим за обучение (по условиям работы позже).\nЕсли тебе интересно, уточни из какого ты города?")	

async def town_lead(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['town'] = message.text
	await FSMlead.next()
	await message.reply("Мы рады всем, но в свою команду рассматриваем кандидатов от 18 до 25 лет. Пожалуйста, подскажи сколько тебе полных лет?")	

async def age_lead(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['age'] = message.text
	await FSMlead.next()
	await message.reply("Отлично, продолжим.", reply_markup=inline.pillskb)	
		
@dp.callback_query_handler(text="red")
async def duty(callback : types.CallbackQuery):
	await callback.message.answer("В твои обязанности, как модели, входит участие в фотосессиях и создании видеоматериалов для рекламы различных шоурумов или интернет-магазинов.")
	await callback.answer()
	await asyncio.sleep(2)
	await bot.send_message("Если вакансия заинтересовала, напиши или поделись с нами номером телефона", reply_markup=keyboards.requsetbutton)
	
dp.callback_query_handler(text="blue")
async def conditions(callback : types.CallbackQuery):
	await callback.message.answer("Твой график работы в твоих руках. Для нас важно, чтоб была выполнена норма часов, а именно, 6 часов в день и 30 часов в неделю. Все остальное решаешь ты.\nТвоя зарплата формируется исходя из количества отработанных часов + бонус за выполненные проекты в месяц.\nМы рады новым моделям и поэтому предусмотрели обучение. Длится оно 5 дней. И, отмечу, что обучение оплачивается каждый день, в конце рабочего дня.")
	await callback.answer()
	await asyncio.sleep(5)
	await bot.send_message("Если вакансия заинтересовала, напиши или поделись с нами номером телефона", reply_markup=keyboards.requsetbutton)
	

async def phone_lead(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['phone'] = message.contact		
	await rekruter_data.sql_leads_add(state)
	await state.finish()
	await message.reply("Очень рад, что ты решила познакомиться с нами. Мы обязательно свяжемся с тобой в ближайшее время.", reply_markup=keyboards.endsbutton)	
	
async def about_company(message : types.Message):
	await bot.send_message("Наш дружный коллектив работает с 2014 года, быстро и успешно завоевал доверие профессиональных моделей и брендов.")

async def URL(message : types.Message):
	await bot.send_message("http://style-models.ru")

def register_handlers_models(dp : Dispatcher):
	dp.register_message_handler(firs_event, commands=['start'],state=None)
	dp.register_message_handler(name_lead, state=FSMlead.name)
	dp.register_message_handler(town_lead, state=FSMlead.town)
	dp.register_message_handler(age_lead, state=FSMlead.age)
	dp.callback_query_handler(duty, text="red")
	dp.callback_query_handler(conditions, text="blue")
	dp.register_message_handler(phone_lead, state=FSMlead.phone)
	dp.register_message_handler(about_company, commands=['О компании'])
	dp.register_message_handler(URL, commands=['Наш сайт'])

