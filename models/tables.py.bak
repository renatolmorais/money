import datetime

# -*- coding: utf-8 -*-
#########################################################################
## Define your tables below for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('expenses',
                Field('e_owner',db.auth_user),
                Field('e_year','integer'),
                Field('e_month','integer'),
                Field('e_day','integer'),
                Field('e_data','string',default=str(datetime.date.today())),
                Field('e_description','string'),
                Field('e_type','string'),
                Field('e_value','double'),
                Field('e_payment','string'),
                Field('e_quant','integer',default=1),
                format = "%(e_description)s"
               )

db.expenses.e_year.requires = IS_NOT_EMPTY()
db.expenses.e_month.requires = IS_NOT_EMPTY()
db.expenses.e_day.requires = IS_NOT_EMPTY()
db.expenses.e_data.requires = IS_NOT_EMPTY()
db.expenses.e_description.requires = IS_NOT_EMPTY()
db.expenses.e_type.requires = IS_NOT_EMPTY()
db.expenses.e_value.requires = IS_NOT_EMPTY()
db.expenses.e_payment.requires = IS_NOT_EMPTY()
db.expenses.e_quant.requires = IS_NOT_EMPTY()

db.define_table('in_out',
                Field('e_owner',db.auth_user),
                Field('e_year','integer'),
                Field('e_month','integer'),
                Field('e_register','string'),
                Field('e_data','string',default=str(datetime.date.today())),
                Field('e_description','string'),
                Field('e_type','string'),
                Field('e_value','double'),
                Field('e_source','string'),
                Field('e_sink','string'),
                format = "%(e_description)s"
                )

db.in_out.e_year.requires = IS_NOT_EMPTY()
db.in_out.e_month.requires = IS_NOT_EMPTY()
db.in_out.e_register.requires = IS_NOT_EMPTY()
db.in_out.e_data.requires = IS_NOT_EMPTY()
db.in_out.e_description.requires = IS_NOT_EMPTY()
db.in_out.e_type.requires = IS_NOT_EMPTY()
db.in_out.e_value.requires = IS_NOT_EMPTY()
db.in_out.e_source.requires = IS_NOT_EMPTY()
db.in_out.e_sink.requires = IS_NOT_EMPTY()

db.define_table('planning',
                Field('e_owner',db.auth_user),
                Field('e_year','integer'),
                Field('e_month','integer'),
                Field('e_register','string'),
                Field('e_description','string'),
                Field('e_value','double'),
#                Field('e_status','string'),
                format = "%(e_description)s"
                )

db.planning.e_year.requires = IS_NOT_EMPTY()
db.planning.e_month.requires = IS_NOT_EMPTY()
db.planning.e_register.requires = IS_NOT_EMPTY()
db.planning.e_description.requires = IS_NOT_EMPTY()
db.planning.e_value.requires = IS_NOT_EMPTY()
#db.planning.e_status.requires = IS_NOT_EMPTY()

db.define_table('accounts',
                Field('account_owner',db.auth_user),
                Field('account_name','string'),
                Field('account_value','double',default=0.0),
                Field('is_written','boolean'),
                format = "%(account_name)s",
                )

db.accounts.account_name.requires = IS_NOT_EMPTY()
db.accounts.account_value.requires = IS_NOT_EMPTY()
