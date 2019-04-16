from manticora.models.database_functions.default_menus import (
    default_card_insert,
    query_all_menus
)
from manticora.models.database_functions.restaurante import (
    get_actual_rest
)


def insert_default_card(dia, tipo, item, preco, user):
    availabe_days = {
        "monday": "Segunda-Feira",
        "tuesday": "Terça-Feira",
        "wednesday": "Quarta-Feira",
        "thursday": "Quinta-Feira",
        "friday": "exta-Feira",
        "saturday": "Sábado",
        "sunday": "Domingo"
    }

    availabe_types = {
        "acomp": "Acompanhamento (Marmitas)",
        "add": "Adicional (Marmitas)",
        "drink": "Bebida",
        "snack": "Lanche",
        "pizza": "Pizza",
        "main_plate": "Prato Principal (Marmitas)",
        "other": "Outro",
        "deserve": "Sobremesa"
    }
    try:
        default_card_insert(availabe_days[dia],
                            availabe_types[tipo],
                            item,
                            preco,
                            get_actual_rest(user))
        return "ok"
    except Exception:
        return "error"


def show_default_menus(user):
    return query_all_menus(get_actual_rest(user))
