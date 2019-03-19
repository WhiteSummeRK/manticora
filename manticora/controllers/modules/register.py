from manticora.models.database_functions.usuario import (
    insert_new_user_account,
    check_for_existing_mail,
    check_for_existing_name,
    update_user_from_db
    )
from manticora.models.database_functions.restaurante import (
    insert_new_rest
)
from datetime import datetime


def register_user(nome, senha,
                  email, bairro,
                  cidade, rua,
                  numero, comp, is_adm=False,
                  return_entity=False):
    """Faz as verificações adequadas e insere os dados no banco."""
    if check_for_existing_name(nome):
        return 'Esse nome já existe.'
    if check_for_existing_mail(email):
        return 'Esse email já existe.'
    try:
        act = insert_new_user_account(nome, senha,
                                      email, bairro,
                                      cidade, rua,
                                      numero, comp, is_adm)
    except Exception:
        return 'Algo deu errado, tente novamente.'
    if return_entity:
        return act
    return 'Usuário inserido com sucesso.'


def register_rest(phone, num_phone, img, open, closed, adm):
    """Faz as verificações e insere novo adm."""
    openned = datetime.strptime(open, '%H:%M').time()
    closed = datetime.strptime(closed, '%H:%M').time()
    if openned == closed:
        return "Desculpe, não é possivel utilizar um estabelecimento 24hrs"
    try:
        insert_new_rest(phone, num_phone, img, openned, closed, adm)
    except Exception as e:
        return 'Algo deu errado, tente novamente.'
    return 'ok'


def update_user(city, neigh, street, num, complement, current_user):
    try:
        update_user_from_db(city, neigh, street, num, complement, current_user)
        return "ok"
    except Exception:
        return "Algo deu errado, tente novamente."
