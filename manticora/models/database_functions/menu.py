from manticora.models.database.tables import (Usuario, Restaurante,
                                              Cardapio, TamanhosPrecos, db)
from manticora.models.database_functions.restaurante import get_actual_rest
from sqlalchemy import or_, and_
from datetime import datetime


def insert_menu(item, kind, day, current_user):
    new_day = datetime.strptime(day, "%m/%d/%Y").date()
    try:
        rest = get_actual_rest(current_user)
        card = Cardapio(
            dia=day,
            prato=item,
            tipo=kind,
            rest=rest
        )
        db.session.add(card)
        db.session.commit()
        return 'Cardápio Inserido com sucesso!'
    except Exception as e:
        db.session.rollback()
        raise


def query_all_menus(current_user):
    rest = get_actual_rest(current_user)
    return Cardapio.query.filter_by(rest=rest).order_by(Cardapio.tipo). \
        limit(50).all()


def query_menus_by_day(day, current_user):
    rest = get_actual_rest(current_user)
    return Cardapio.query.filter_by(rest=rest).filter(Cardapio.dia == day). \
        order_by(Cardapio.tipo).limit(50).all()


def query_menu_by_rest_id(id, date):
    rest = Restaurante.query.filter_by(id=id).first()
    return Cardapio.query.filter_by(rest=rest).filter(Cardapio.dia == date). \
        order_by(Cardapio.tipo).limit(50).all()


def query_marmita_by_size(size):
    return TamanhosPrecos.query.filter_by(tamanho=size).all()


def insert_new_marmita(size, price, current_user):
    rest = get_actual_rest(current_user)
    try:
        marmita = TamanhosPrecos(
            tamanho=size,
            preco=float(price),
            rest=rest
        )
        db.session.add(marmita)
        db.session.commit()
        return "Marmita Criada com sucesso!"
    except Exception:
        return "Erro"


def query_itens_from_menu(items):
    all_itens = []
    for item in items:
        plate = Cardapio.query.filter_by(id=int(item)).first()
        all_itens.append(plate.prato)
    return all_itens


def query_all_marmitas(current_user):
    rest = get_actual_rest(current_user)
    return TamanhosPrecos.query.filter_by(rest=rest).all()


def query_all_marmitas_by_rest_id(id):
    rest = Restaurante.query.filter_by(id=id).first()
    return TamanhosPrecos.query.filter_by(rest=rest).all()


def query_marmita_by_id(id):
    return TamanhosPrecos.query.filter_by(id=int(id)).first()