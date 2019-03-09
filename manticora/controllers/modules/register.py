from manticora.models.database_functions.cliente import (
    insert_new_user_account,
    check_for_existing_mail,
    check_for_existing_name
    )


def register_common_user(nome, senha,
                         email, bairro,
                         cidade, rua,
                         numero, comp):
    """Faz as verificações adequadas e insere os dados no banco"""
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
