from datetime import datetime
from manticora.models.database.tables import (Restaurante,
                                              Extrato, UsuarioConta, db)
from manticora.models.database_functions.menu import query_marmita_by_size


def query_for_user_account(current_user):
    return UsuarioConta.query.filter_by(id=int(current_user.id)).first()


def query_user_account_by_id(id_user, id_rest):
    return UsuarioConta.query.filter_by(id_usuario=id_user). \
        filter_by(id_restaurante=id_rest).first()


def insert_into_user_extrato(item, preco, current_user, rest_id):
    new_request = Extrato(
        conta=query_user_account_by_id(int(current_user.id), int(rest_id)),
        itens=item,
        data=datetime.now().date(),
        valor=float(preco)
        )
    try:
        db.session.add(new_request)
        db.session.commit()
    except Exception:
        db.session.rollback()
    return new_request


def update_user_bill(preco, current_user, rest_id):
    rest = Restaurante.query.filter_by(id=int(rest_id)).first()
    bill = UsuarioConta.query.filter_by(usuario=current_user). \
        filter_by(restaurante=rest).first()
    try:
        bill.conta += float(preco)
        bill.status = "Aguardando Pagamento"
        db.session.commit()

        return bill
    except Exception:
        db.session.rollback()


def create_user_account(preco, current_user, rest_id):
    rest = Restaurante.query.filter_by(id=int(rest_id)).first()
    try:
        bill = UsuarioConta(
            usuario=current_user,
            restaurante=rest,
            conta=float(preco),
            status="Aguardando Pagamento"
        )
        db.session.add(bill)
        db.session.commit()
        return bill
    except Exception:
        db.session.rollback()
        return "erro"


def query_bill(current_user, rest_id):
    rest = Restaurante.query.filter_by(id=int(rest_id)).first()
    return UsuarioConta.query.filter_by(usuario=current_user). \
        filter_by(restaurante=rest).first()
