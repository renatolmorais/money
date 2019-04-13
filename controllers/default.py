# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from functions import *
appname = 'Money Manager'

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    if auth.user:
        #if not exist_accounts(db,auth): create_accounts(db,auth)
        if not exist_accounts(): create_accounts()
        redirect(URL('expenses'))
        #return dict()
    else:
        return dict(
            form=auth.login(),
            appname=appname,
        )

@auth.requires_login()
def expenses():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    myexpenses = []
    success = True
    message = ''
    money = debit = credit = 0.0
    cur_month = int(request.vars.cur_month) if request.vars.cur_month else int(datetime.now().month)
    cur_year = int(request.vars.cur_year) if request.vars.cur_year else int(datetime.now().year)
    year_list = range(2010,int(datetime.now().year) + 1)
    cur_values = {}
    owner_id = 0
    try:
        #owner_id = db(db.auth_user.username == auth.user.username).select(db.auth_user.id)[0].id
        owner_id = auth.user.id
#        if request.vars.cur_month:
#            cur_month = int(request.vars.cur_month)
#        if request.vars.cur_year:
#            cur_year = int(request.vars.cur_year)
#        elif request.vars.is_submition:
        if request.vars.is_submition:
            e_data = request.vars.e_data
            e_month = e_data.split('-')[1]
            e_year = e_data.split('-')[0]
            e_description = request.vars.e_description
            e_type = request.vars.e_type
            e_value = request.vars.e_value
            e_payment = request.vars.e_payment
            db.expenses.insert(
                e_owner=owner_id,
                e_year=e_year,
                e_month=e_month,
                e_data=e_data,
                e_description=e_description,
                e_type=e_type,
                e_value=e_value,
                e_payment=e_payment,
            )
            update_accounts(float(e_value),e_payment,'Saida')
        myexpenses = db(db.expenses.e_owner == owner_id)(db.expenses.e_year == cur_year)(db.expenses.e_month == cur_month).select(db.expenses.ALL)
        money_list = db(db.expenses.e_owner == owner_id)(db.expenses.e_year == cur_year)(db.expenses.e_month == cur_month)(db.expenses.e_payment == 'Dinheiro').select(db.expenses.e_value)
        money = reduce(lambda x,y: x+y.e_value, money_list, 0.0)
        debit_list = db(db.expenses.e_owner == owner_id)(db.expenses.e_year == cur_year)(db.expenses.e_month == cur_month)(db.expenses.e_payment == 'Cartão de Débito').select(db.expenses.e_value)
        debit = reduce(lambda x,y: x+y.e_value, debit_list, 0.0)
        credit_list = db(db.expenses.e_owner == owner_id)(db.expenses.e_year == cur_year)(db.expenses.e_month == cur_month)(db.expenses.e_payment == 'Cartão de Crédito').select(db.expenses.e_value)
        credit = reduce(lambda x,y: x+y.e_value, credit_list, 0.0)
    except Exception as err:
        message = err.message
        success = False
    return dict(
        year_list=year_list,
        cur_year=cur_year,
        cur_month=cur_month,
        expenses=myexpenses,
        message=message,
        success=success,
        somas={'money':money,'debit':debit,'credit':credit},
#        cur_values=calculate_values(db,owner_id),
        cur_values = calculate_values(),
#        cur_values = {'wallet':0.0,'bank':0.0,'savings':0.0},
        appname=appname,
    )

@auth.requires_login()
def inout():
    expenses = []
    success = True
    message = ''
    money = debit = credit = 0.0
    cur_month = int(request.vars.cur_month) if request.vars.cur_month else int(datetime.now().month)
    cur_year = int(request.vars.cur_year) if request.vars.cur_year else int(datetime.now().year)
    year_list = range(2010,int(datetime.now().year) + 1)
    cur_values = {}
    owner_id = 0
    try:
        #owner_id = db(db.auth_user.username == auth.user.username).select(db.auth_user.id)[0].id
        owner_id = auth.user.id
#        if request.vars.cur_month:
#            cur_month = int(request.vars.cur_month)
#        if request.vars.cur_year:
#            cur_year = int(request.vars.cur_year)
#        elif request.vars.is_submition:
        if request.vars.is_submition:
            e_register = request.vars.e_register
            e_data = request.vars.e_data
            e_month = int(request.vars.e_data.split('-')[1])
            e_year = int(request.vars.e_data.split('-')[0])
            e_value = request.vars.e_value
            e_description = request.vars.e_description
            e_type = request.vars.e_type
            e_source = request.vars.e_source
            e_sink = request.vars.e_sink
            db.in_out.insert(
                e_owner=owner_id,
                e_register=e_register,
                e_year=e_year,
                e_month=e_month,
                e_data=e_data,
                e_description=e_description,
                e_type=e_type,
                e_value=e_value,
                e_source=e_source,
                e_sink=e_sink,
            )
            update_accounts(e_value,e_sink if e_register == 'Entrada' else e_source,e_register)
        expenses = db(db.in_out.e_owner == owner_id)(db.in_out.e_year == cur_year)(db.in_out.e_month == cur_month).select(db.in_out.ALL)
    except Exception as err:
        message = err.message
        success = False
    return dict(
        year_list=year_list,
        cur_year=cur_year,
        cur_month=cur_month,
        expenses=expenses,
        message=message,
        success=success,
#        cur_values=calculate_values(db,owner_id),
        cur_values = calculate_values(),
        appname=appname,
    )

@auth.requires_login()
def planning():
    expenses = []
    success = True
    message = ''
    money = debit = credit = 0.0
    cur_month = int(request.vars.cur_month) if request.vars.cur_month else int(datetime.now().month)
    cur_year = int(request.vars.cur_year) if request.vars.cur_year else int(datetime.now().year)
    year_list = range(2010,int(datetime.now().year) + 1)
    cur_values = {}
    owner_id = 0
    try:
        #owner_id = db(db.auth_user.username == auth.user.username).select(db.auth_user.id)[0].id
        owner_id = auth.user.id
#        if request.vars.cur_month:
#            cur_month = int(request.vars.cur_month)
#        if request.vars.cur_year:
#            cur_year = int(request.vars.cur_year)
#        elif request.vars.is_submition:
        if request.vars.is_submition:
            e_register = request.vars.e_register
            e_description = request.vars.e_description
            e_type = request.vars.e_type
            e_value = request.vars.e_value
            db.planning.insert(
                e_owner=owner_id,
                e_year=cur_year,
                e_month=cur_month,
                e_register=e_register,
                e_description=e_description,
                e_value=e_value,
            )
        expenses = db(db.planning.e_owner == owner_id)(db.planning.e_year == cur_year)(db.planning.e_month == cur_month).select(db.planning.ALL)
    except Exception as err:
        message = err.message
        success = False
    return dict(
        year_list=year_list,
        cur_year=cur_year,
        cur_month=cur_month,
        expenses=expenses,
        message=message,
        success=success,
#        cur_values=calculate_values(db,owner_id),
        cur_values = calculate_values(),
        appname=appname,
    )

@auth.requires_login()
def credit():
    expenses = []
    parc = {}
    success = True
    message = ''
    money = debit = credit = 0.0
    cur_month = int(request.vars.cur_month) if request.vars.cur_month else int(datetime.now().month)
    cur_year = int(request.vars.cur_year) if request.vars.cur_year else int(datetime.now().year)
    year_list = range(2010,int(datetime.now().year) + 1)
    cur_values = {}
    owner_id = 0
    total_credit = 0.0
    num = 0
    try:
        #owner_id = db(db.auth_user.username == auth.user.username).select(db.auth_user.id)[0].id
        owner_id = auth.user.id
#        if request.vars.cur_month:
#            cur_month = int(request.vars.cur_month)
#        if request.vars.cur_year:
#            cur_year = int(request.vars.cur_year)
        credit_expenses = db(db.expenses.e_owner==owner_id,db.expenses.e_payment == 'Cartão de Crédito').select(db.expenses.ALL)
        expenses = []
        for credit_expense in credit_expenses:
            uid = credit_expense.id
            year = credit_expense.e_year
            month = credit_expense.e_month
            quant = credit_expense.e_quant
            n_months = 12*(cur_year - year) + (cur_month - month)
            if n_months > quant: continue
            day = credit_expense.e_day
            if not ( (year <= cur_year) and (month <= (12*(cur_year - year) + (cur_month - 1))) and (day <= 26) ): continue
            num = n_months if n_months <= quant else 0
            month = credit_expense.e_month + 1 if day <= 26 else credit_expense.e_month + 2
            month += quant
            while month > 12:
                month -= 12
                year += 1
            if year > cur_year or month >= cur_month:
                credit_expense.e_value /= quant
                credit_expense.e_quant = num
                expenses.append(credit_expense)
                parc[uid] = '%d/%d'%(num,quant)
        total_credit = reduce(lambda x,y: x+y.e_value, expenses, 0.0)
    except Exception as err:
        message = err.message
        success = False
    return dict(
        year_list=year_list,
        cur_year=cur_year,
        cur_month=cur_month,
        expenses=expenses,
        message=message,
        parc=parc,
        success=success,
        total_credit=total_credit,
#        cur_values=calculate_values(db,owner_id),
        cur_values = calculate_values(),
        appname=appname,
    )

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(
        form=auth(),
        appname=appname,
    )

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
