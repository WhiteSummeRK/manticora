from datetime import datetime
from manticora.models.database.tables import (UsuarioConta,
                                              Usuario,
                                              Restaurante,
                                              Extrato,
                                              db)


def query_user_accounts_by_user(user):
    return UsuarioConta.query.filter_by(usuario=user).all()


def query_account_by_id(id):
    return UsuarioConta.query.filter_by(id=id).first()


def find_all_extrato(account):
    return Extrato.query.filter_by(conta=account).limit(30).all()


def query_all_account_in_rest(rest):
    return UsuarioConta.query.filter_by(restaurante=rest).all()


def change_status(id_account, status):
    try:
        account = UsuarioConta.query.filter_by(id=int(id_account)).first()
        account.conta = 0.00
        account.status = status
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def query_all_requests_from_user(id, date):
    return Extrato.query.join(UsuarioConta).join(Usuario) \
        .filter(Usuario.id == id) \
        .filter(Extrato.data == date) \
        .order_by(Extrato.status).all()
