import sys,os
import sqlite3
import random

#despesas = [
#	{
#	'id': 20,
#	'e_year': 2010,
#	'e_month': 10,
#	'e_data': '2010-10-08',
#	'e_description': 'Boliche Del-Rey',
#	'e_type': 'Diversao',
#	'e_value': 80.0,
#	'e_payment': 'Cartao de Debito'
#	}
#]

def get_type():
	type = ['Empr&eacute;stimo','Doa&ccedil;&atilde;o','Cart&atilde;o de Cr&eacute;dito','Celular','Condo&iacute;nio','Energia','Telefone']
	random.seed()
	return random.choice(type)

def get_register():
	random.seed()
	return random.choice(['Entrada','Sa&iacute;da'])

def get_source_sink():
	source = ['BB','Poupan&ccedil;a BB','Carteira','Nuvem']
	sink = ['BB','Poupan&ccedil;a BB','Carteira','Pagamento']
	random.seed()
	r_source = random.choice(source)
	r_sink = random.choice(sink)
	type = 'Entrada' if r_source == 'Nuvem' and not r_sink =='Pagamento' else 'Sa&iacute;da'
	type = 'Sa&iacuteda;' if not r_source == 'Nuvem' and r_sink == 'Pagamento' else 'Entrada'
	return r_source,r_sink,type

def get_description():
	description = {
		'Guarim': 'Supermercado',
		'Restaurante Origem': 'Almoco',
		'Araujo': 'Farmacia',
		'Pacheco': 'Farmacia',
		'Carrefour': 'Supermercado',
		'Outback': 'Jantar',
		'Si Senor': 'Jantar',
		'Extra': 'Supermercado',
		'Eddies': 'Lanche',
		'Chocolates': 'Guloseimas',
		'Boliche': 'Diversao',
		'A Granel': 'Almoco',
		'Dona Margherita': 'Almoco',
		}
	random.seed()
	in_list = description.keys()
	key = random.choice(in_list)
	return (key,description[key])

def get_payment():
	payment = ['Cartao de Credito','Cartao de Debito','Dinheiro']
	random.seed()
	return random.choice(payment)

def get_year():
	years = range(2010,2016)
	random.seed()
	return random.choice(years)

def get_month():
	months = {
		'Janeiro': 1,
		'Fevereiro': 2,
		'Marco': 3,
		'Abril': 4,
		'Maio': 5,
		'Junho': 6,
		'Julho': 7,
		'Agosto': 8,
		'Setembro': 9,
		'Outubro': 10,
		'Novembro': 11,
		'Dezembro': 12
		}
	month_days = {
		'Janeiro': 31,
		'Fevereiro': 28,
		'Marco': 31,
		'Abril': 30,
		'Maio': 31,
		'Junho': 30,
		'Julho': 31,
		'Agosto': 31,
		'Setembro': 30,
		'Outubro': 31,
		'Novembro': 30,
		'Dezembro': 31,
		}
	random.seed()
	months_list = months.keys()
	month = random.choice(months_list)
	day = random.randrange(1,month_days[month])
	return months[month],day

def get_value():
	random.seed()
	return float(random.randrange(0,5000))

def format_expenses_query():
	query = ''
	year = get_year()
	month,day = get_month()
	data = '%d-%d-%d'%(year,month,day)
	description,type = get_description()
	value = get_value()
	payment = get_payment()
	return 'insert into expenses (e_year,e_month,e_data,e_description,e_type,e_value,e_payment) values (?,?,?,?,?,?,?)'%(year,month,data,description,type,value,payment)
	
def format_inout_query():
	query = ''
	year = get_year()
	month,day = get_month()
	data = '%d-%d-%d'%(year,month,day)
	description,type = get_description()
	source,sink,register = get_source_sink()
	value = get_value()
	return 'insert into in_out (e_year,e_month,e_register,e_data,e_description,e_type,e_value,e_source,e_sink) values (?,?,?,?,?,?,?,?,?)'%(year,month,register,data,description,type,value,source,sink)

def format_planning_query():
	query = ''
	year = get_year()
	month,day = get_month()
	register = get_register()
	description,type = get_description()
	value = get_value()
	return 'insert into planning (e_year,e_month,e_register,e_description,e_value) values (?,?,?,?,?)'%(year,month,register,description,value)	

def update_day():
	query = 'select id,e_data from expenses'
	database_path = 'C:\\Users\\suporte_renato\\Downloads\\web2py\\applications\\money\\databases\\storage.sqlite'
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	rows = c.execute(query)
	
	d = conn.cursor()
	for row in rows:
		day = row[1].split('-')[2]
		id = row[0]
		print id,day
		d.execute('update expenses set e_day = ? where id = ?',(int(day),id))
		conn.commit()
	conn.close()
		
if __name__ == '__main__':

	#update_day()
	database_path = 'C:\\Users\\suporte_renato\\Downloads\\web2py\\applications\\money\\databases\\storage.sqlite'
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	
	#for i in range(1,1001):
		#expenses_query = format_expenses_query()
		#inout_query = format_inout_query()
		#planning_query = format_planning_query()
		#print query
		#c.execute(expenses_query)
		#conn.commit()
		#c.execute(inout_query)
		#conn.commit()
		#c.execute(planning_query)
		#conn.commit()

	#conn.close()