from manticora.models.database_functions.usuario import (
    insert_new_user_account,
    check_for_existing_mail,
    check_for_existing_name,
    update_user_from_db
    )
from manticora.models.database_functions.restaurante import (
    insert_new_rest,
    get_actual_rest,
    update_rest_from_db
)
from manticora.models.database.tables import db
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
        db.session.rollback()
        db.session.remove()
        return "Desculpe, não é possivel utilizar um estabelecimento 24hrs"
    try:
        insert_new_rest(phone, num_phone, img, openned, closed, adm)
    except Exception:
        db.session.rollback()
        db.session.remove()
        return 'Algo deu errado, tente novamente.'
    return 'ok'


def update_user(city, neigh, street, num, complement, current_user):
    try:
        update_user_from_db(city, neigh, street, num, complement, current_user)
        return "ok"
    except Exception:
        return "Algo deu errado, tente novamente."


def update_rest(phone, hora_aber, hora_fech, current_user):
    rest = get_actual_rest(current_user)
    db_hora_aber = datetime.strptime(hora_aber, "%H:%M").time()
    db_hora_fech = datetime.strptime(hora_fech, "%H:%M").time()
    try:
        update_rest_from_db(phone, db_hora_aber, db_hora_fech, None, rest)
        return "ok"
    except Exception:
        return "Algo deu errado, tente novamente."


def update_rest_img(imagem, current_user):
    rest = get_actual_rest(current_user)
    try:
        update_rest_from_db(False, False, False, imagem, rest)
        return "ok"
    except Exception:
        return "Algo deu errado, tente novamente."
