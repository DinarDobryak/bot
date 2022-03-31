import sqlite3 as sq


def sql_lead():
	global base, cur
	base = sq.connect('lead_base.db')
	cur = base.cursor()
	if base:
		print("База данных Лидов подключена")
	base.execute('CREATE TABLE IF NOT EXISTS leads(name TEXT, town TEXT, age TEXT, phone)')
	base.commit()


async def sql_leads_add(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO leads VALUES (?, ?, ?, ?)', tuple(data.values()))
		base.commit()