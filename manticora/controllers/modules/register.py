from manticora.models.database_functions.usuario import (
    insert_new_user_account,
    check_for_existing_mail,
    check_for_existing_name
    )
from manticora.models.database_functions.restaurante import (
    insert_new_rest
)


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


def register_rest(phone, num_phone, img, adm):
    """Faz as verificações e insere novo adm."""
    try:
        insert_new_rest(phone, num_phone, img, adm)
    except Exception as e:
        return 'Algo deu errado, tente novamente.'
    return 'ok'
