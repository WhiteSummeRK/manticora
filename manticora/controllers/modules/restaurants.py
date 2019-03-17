from base64 import b64encode
from manticora.models.database_functions.restaurante import (
    query_all_restaurants_with_name,
    query_ads_by_name,
    query_all_adms,
    show_closed_rests_by_city,
    show_openned_rests_by_city,
    show_all_rests_by_city
)
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
