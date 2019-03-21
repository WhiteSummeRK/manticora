from datetime import datetime
from manticora.models.database.tables import (UsuarioConta,
                                              Restaurante,
                                              Extrato,
                                              db)


def query_user_accounts_by_user(user):
    return UsuarioConta.query.filter_by(usuario=user).all()


def query_account_by_id(id):
    return UsuarioConta.query.filter_by(id=id).first()


def find_all_extrato(account):
    return Extrato.query.filter_by(conta=account).limit(30).all()
