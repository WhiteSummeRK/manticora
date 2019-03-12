from manticora.models.database_functions.cliente import (
    insert_new_user_account,
    insert_new_adm_account,
    check_for_existing_mail,
    check_for_existing_name,
    check_for_existing_name_adm,
    check_for_existing_mail_adm
    )


def register_common_user(nome, senha,
                         email, bairro,
                         cidade, rua,
                         numero, comp):
    """Faz as verificações adequadas e insere os dados no banco."""
    if check_for_existing_name(nome):
        return 'Esse nome já existe.'
    if check_for_existing_mail(email):
        return 'Esse email já existe.'
    try:
        insert_new_user_account(nome, senha,
                                email, bairro,
                                cidade, rua,
                                numero, comp)
    except Exception:
        return 'Algo deu errado, tente novamente.'
    return 'Usuário inserido com sucesso.'


def register_adm(name, email,
                 phone, num_phone,
                 pwd, neigh,
                 city, street,
                 num_street, comp, img):
    """Faz as verificações e insere novo adm."""
    if check_for_existing_mail_adm(email):
        return 'Esse email já existe.'
    if check_for_existing_name_adm(name):
        return 'Esse nome já existe.'
    try:
        insert_new_adm_account(
            name, email,
            phone, num_phone,
            pwd, neigh,
            city, street,
            num_street, comp, img
        )
    except Exception as e:
        return 'Algo deu errado, tente novamente.'
    return 'ok'
