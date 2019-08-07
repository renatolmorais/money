# -*- coding: utf-8 -*-
from datetime import datetime
from md5 import new
from gluon import current

#def exist_accounts(db,auth):
def exist_accounts():
    db = current.db
    auth = current.auth
    if db(db.accounts.account_owner == auth.user.id).select(db.accounts.ALL): return True
    return False

#def create_accounts(db,auth):
def create_accounts():
    db = current.db
    auth = current.auth
    db.accounts.insert(
        account_owner=auth.user.id,
        account_name='wallet',
        )
    db.accounts.insert(
        account_owner=auth.user.id,
        account_name='bank',
        )
    db.accounts.insert(
        account_owner=auth.user.id,
        account_name='savings',
        )

def calculate_hash():
    ms = datetime.now().microsecond
    md5ms = new(str(ms))
    word = md5ms.hexdigest()
    return word[0:8] + '-' + word[9:13] + '-' + word[14:18] + '-' + word[19:]

def update_accounts(value,payment,ptype):
    db = current.db
    auth = current.auth
    accounts = {
        'Carteira': 'wallet',
        'Dinheiro': 'wallet',
        'BB':'bank',
        'Débito em Conta':'bank',
        'Cartão de Débito':'bank',
        'Poupança BB':'savings'
    }
    account = accounts.get(payment,'')
    cur_value = db(db.accounts.account_owner == auth.user.id)(db.accounts.account_name == account).select(db.accounts.account_value)[0].account_value
    if ptype == 'Entrada': cur_value += value # entrou dinheiro
    else: cur_value -= value# saiu dinheiro
    db(db.accounts.account_owner == auth.user.id)(db.accounts.account_name == account).update(account_value=cur_value)

def update_accounts_deprecated(owner_id):
    db = current.db
    auth = current.auth
    money_list = db(db.accounts.account_owner == auth.user.id)(db.expenses.e_payment == 'Dinheiro').select(db.expenses.e_value)
    money_spent = reduce(lambda x,y: x+y.e_value, money_list, 0.0)

    debit_list = db(db.accounts.account_owner == auth.user.id)(db.expenses.e_payment == 'Cartão de Débito').select(db.expenses.e_value)
    debit_spent = reduce(lambda x,y: x+y.e_value, debit_list, 0.0)

    wallet_income = db(db.accounts.account_owner == auth.user.id)(db.in_out.e_sink == 'Carteira').select(db.in_out.ALL)
    bank_income = db(db.accounts.account_owner == auth.user.id)(db.in_out.e_sink == 'BB').select(db.in_out.ALL)
    savings_income = db(db.accounts.account_owner == auth.user.id)(db.in_out.e_sink == 'Poupança BB').select(db.in_out.ALL)

    wallet_outgoing = db(db.accounts.account_owner == auth.user.id)(db.in_out.e_source == 'Carteira').select(db.in_out.ALL)
    bank_outgoing = db(db.accounts.account_owner == auth.user.id)(db.in_out.e_source == 'BB').select(db.in_out.ALL)
    savings_outgoing = db(db.accounts.account_owner == auth.user.id)(db.in_out.e_source == 'Poupança BB').select(db.in_out.ALL)

    wallet_total = reduce(lambda x,y: x+y.e_value, wallet_income, 0.0) - (money_spent + reduce(lambda x,y: x+y.e_value, wallet_outgoing, 0.0))
    bank_total = reduce(lambda x,y: x+y.e_value, bank_income, 0.0) - (debit_spent + reduce(lambda x,y: x+y.e_value, bank_outgoing, 0.0))
    savings_total = reduce(lambda x,y: x+y.e_value, savings_income, 0.0) - reduce(lambda x,y: x+y.e_value, savings_outgoing, 0.0)

#def calculate_values(db,owner_id):
def calculate_values():
    db = current.db
    auth = current.auth
    # get accounts values
    wallet_value = db(db.accounts.account_owner == auth.user.id)(db.accounts.account_name == 'wallet').select(db.accounts.account_value)[0].account_value
    bank_value = db(db.accounts.account_owner == auth.user.id)(db.accounts.account_name == 'bank').select(db.accounts.account_value)[0].account_value
    savings_value = db(db.accounts.account_owner == auth.user.id)(db.accounts.account_name == 'savings').select(db.accounts.account_value)[0].account_value

    return {'wallet': wallet_value, 'bank': bank_value, 'savings': savings_value}
