from aiogram.utils import executor
from bot import dp
from aiogram import types
from data_base import rekruter_data



async def on_startup(_):
	print('Бот запущен')
	rekruter_data.sql_lead()



from handlers import rekrut
from markups import inline, keyboards


rekrut.register_handlers_models(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)