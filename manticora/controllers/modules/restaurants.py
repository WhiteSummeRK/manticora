from base64 import b64encode
from manticora.models.database_functions.restaurante import (
    query_all_restaurants_with_name,
    query_all_adms
)


def show_restaurants():
    adms = query_all_adms()
    rests = query_all_restaurants_with_name(adms)
    for item in rests:
        item[1].imagem = b64encode(item[1].imagem).decode('utf-8')
    return rests


def show_all_citys():
    adms = query_all_adms()
    return [item.cidade for item in adms]
