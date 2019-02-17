"""Modulo de login"""
from manticora.models.database_functions.account import (insert_new_user_account,
                                                         check_for_existing_mail,
                                                         check_for_existing_name)

def register_common_user(name, email, pwd):
    """Faz as verificações adequadas e insere os dados no banco"""
    if check_for_existing_name(name):
        return 'Esse nome já existe.'
    if check_for_existing_mail(email):
        return 'Esse email já existe.'

    insert_new_user_account(name, email, pwd)
    return 'Usuário inserido com sucesso.'
