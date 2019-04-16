from base64 import b64encode
from datetime import datetime
from manticora.models.database_functions.restaurante import (
    query_all_restaurants_with_name,
    query_ads_by_name,
    query_all_adms,
    show_closed_rests_by_city,
    show_openned_rests_by_city,
    show_all_rests_by_city,
    query_requests_by_rest,
    query_extrato_by_id,
    update_status_from_extrato,
    get_actual_rest
)
from manticora.models.database_functions.user_account import (
    query_for_user_account)

from manticora.models.database.tables import db, Usuario


def show_restaurants(name):
    adms = query_ads_by_name(name)
    rests = query_all_restaurants_with_name(adms)
    for item in rests:
        item[1].imagem = b64encode(item[1].imagem).decode('utf-8')
    return rests


def show_all_citys():
    adms = query_all_adms()
    return [item.cidade for item in adms]


def show_rests_with_filter(filter, citys):
    if filter == 'closed':
        rests = show_closed_rests_by_city(citys)
        for item in rests:
            item[1].imagem = b64encode(item[1].imagem).decode('utf-8')
        return rests

    if filter == 'open':
        rests = show_openned_rests_by_city(citys)
        for item in rests:
            item[1].imagem = b64encode(item[1].imagem).decode('utf-8')
        return rests

    rests = show_all_rests_by_city(citys)
    for item in rests:
        item[1].imagem = b64encode(item[1].imagem).decode('utf-8')
    return rests


def show_requests_to_rest(current_user):
    rest = get_actual_rest(current_user)
    date = datetime.now().date()
    requests = query_requests_by_rest(rest, date)
    return requests


def update_status_request(id_extrato):
    extrato = query_extrato_by_id(int(id_extrato))
    try:
        if extrato.status == "Aguardando Confirmação":
            update_status_from_extrato(int(id_extrato), "Confirmado")
            return "ok"
        if extrato.status == "Confirmado":
            update_status_from_extrato(int(id_extrato), "Enviado")
            return "ok"
        return "Erro"
    except Exception:
        return "Erro"
