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

async def cancel(message: types.Message, state : FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()

async def name_lead(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
	await FSMlead.next()
	await message.reply("В наш дружный коллектив, требуются будущие и действующие модели. Если опыта работы у тебя нет, ничего страшного.Мы хотим научить тебя и даже заплатим за обучение (по условиям работы позже).\nЕсли тебе интересно, уточни из какого ты города?")	

async def town_lead(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['town'] = message.text
	if 	message.text == 'Казань' or message.text == 'Москва':
			await FSMlead.next()
			await message.reply("Мы рады всем, но в свою команду рассматриваем кандидатов от 18 до 25 лет. Пожалуйста, подскажи сколько тебе полных лет?")	
	else:
		await message.reply("К сожалению мы ещё не работаем в вашем городе.")
		await state.finish()	

async def age_lead(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['age'] = message.text
	if message.text == '18' or message.text == '19' or message.text == '20' or message.text == '21' or message.text == '22' or message.text == '23' or message.text == '24' or message.text == '25':
			await FSMlead.next()
			await message.reply("Очень рад, что ты решила с нами познакомиться. Ниже, ты можешь ознакомится с обязанностями и условиями работы.")
			await asyncio.sleep(2)
			await bot.send_message(message.from_user.id, "В твои обязанности, как модели, входит участие в фотосессиях и создании видеоматериалов для рекламы различных шоурумов или интернет-магазинов.")
			await asyncio.sleep(6)
			await bot.send_message(message.from_user.id, "Твой график работы в твоих руках. Для нас важно, чтоб была выполнена норма часов, а именно, 6 часов в день и 30 часов в неделю. Все остальное решаешь ты.\nТвоя зарплата формируется исходя из количества отработанных часов + бонус за выполненные проекты в месяц.\nМы рады новым моделям и поэтому предусмотрели обучение. Длится оно 5 дней. И, отмечу, что обучение оплачивается каждый день, в конце рабочего дня.")	
			await asyncio.sleep(10)
			await bot.send_message(message.from_user.id, "Если вакансия заинтересовала, напиши или поделись с нами номером телефона.")
	else:
		await bot.send_message(message.from_user.id, "К сожалению вы нам не подходите.")
		await state.finish()		
	

async def phone_lead(message : types.Contact, state : FSMContext):
	async with state.proxy() as data:
		data['phone'] = message.text 	
	await rekruter_data.sql_leads_add(state)
	await state.finish()
	await bot.send_message(message.from_user.id, "Благодарю за интерес к нашей вакансии. Мы свяжемся с тобой в ближайшее время.", reply_markup = keyboards.endsbutton)	


@dp.message_handler(commands=['О компании', 'Наш сайт'])
async def buttons(message : types.Message):
	if message == "О компании":
		await message.delete()
		await bot.send_message(message.from_user.id, "Наш дружный коллектив работает с 2014 года, быстро и успешно завоевал доверие профессиональных моделей и брендов.")
	elif message == "Наш сайт":
	 	await message.delete()
	 	await bot.send_message(message.from_user.id, "http://style-models.ru")

def register_handlers_models(dp : Dispatcher):
	dp.register_message_handler(firs_event, commands=['start'],state=None)
	dp.register_message_handler(name_lead, state=FSMlead.name)
	dp.register_message_handler(town_lead, state=FSMlead.town)
	dp.register_message_handler(age_lead, state=FSMlead.age)
	#dp.callback_query_handler(duty, text="red")
	#dp.callback_query_handler(conditions, text="blue")
	dp.register_message_handler(phone_lead, state=FSMlead.phone) # content_types=['contact'],
	
	

