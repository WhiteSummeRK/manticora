from manticora.models.database_functions.menu import (insert_menu,
                                                      query_all_menus,
                                                      query_menus_by_day,
                                                      query_menu_by_rest_id,
                                                      insert_new_marmita,
                                                      query_all_marmitas,
                                                      query_all_marmitas_by_rest_id,
                                                      query_marmita_by_size,
                                                      query_marmita_by_id,
                                                      query_itens_from_menu,
                                                      delete_item_from_menu_db,
                                                      delete_marm_from_db) # NOQA
from manticora.models.database_functions.user_account import (insert_into_user_extrato, #NOQA
                                                              update_user_bill,
                                                              create_user_account,
                                                              query_bill) #NOQA

from datetime import datetime


def save_menu(item, kind, day, preco_item, current_user):
    item_kind = {
        "main_plate": "Prato Principal",
        "acomp": "Acompanhamento",
        "drink": "Bebida",
        "deserve": "Sobremesa",
        "snack": "Lanche",
        "add": "Adicional",
        "other": "Outro"
    }
    if kind not in item_kind.keys():
        return "acha que foi inserido mas nem foi ein"
    if not preco_item:
        return insert_menu(item, item_kind[kind], day, None, current_user)
    return insert_menu(item, item_kind[kind], day, float(preco_item.replace(',', '.')), current_user) # NOQA


def change_datetime(menus):
    for item in menus:
        item.dia = datetime.strptime(item.dia.strftime("%d-%m-%Y"), "%d-%m-%Y").date() #NOQA
    return menus


def show_menu_by_day(day, current_user):
    if not day:
        return change_datetime(query_all_menus(current_user))
    return change_datetime(query_menus_by_day(day, current_user))


def build_html_for_menu(menu, marmitas):
    menu_id = menu[0].id_rest
    marmitas_html = ""
    for item in marmitas:
        marmitas_html += """
        <div class="form-check-inline">
          <label class="form-check-label">
            <input type="radio" class="form-check-input card-text" value={} name="marmitas" required>{} (R${})
          </label>
        </div>
        """.format(item.id, item.tamanho, item.preco) #NOQA
    html_head = """

    <div class="card">
    <div class="card-body">
    <h5 class="card-title">Escolha o Tamanho</h5>
    <form id='meu_form' action='/restaurants/make_request/' method="POST">
    {}
    <div class="table-wrapper-scroll-y my-custom-scrollbar">
    <table class="table">
        <thead>
            <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo</th>
            <th scope="col">Preço Por Item</th>
            <th scope="col">Pedido</th>
          </tr>
        </thead>
            <tbody>
    """.format(marmitas_html)
    html_end = """
        </tbody>
    </table>
    <button type="submit" onclick="confirm_dialog()" class="btn login_btn mb-2">Realizar Pedido</button>
    </div>
    """
    html_middle = ""
    for item in menu:
        preco = "" if not item.preco else f"R$ {item.preco}" #NOQA
        html_middle += """
            <tr>
              <td>{}</td>
              <td>{}</td>
              <td>{}</td>
              <td>
                  <div class="form-check">
            <input class="form-check-input" type="checkbox" value="{}" name="input_box" id="{}">
            <input type="hidden" name="btn_req" value={}>
                  </div>
              </td>
            </tr>
        """.format(item.prato, item.tipo, preco, item.id, item.id, menu_id) #NOQA

    html_btn = """
    </form>
    </div>
    </div>
    """
    return html_head + html_middle + html_end + html_btn


def show_card_by_rest_id(id):
    today = datetime.now().date()
    menu = query_menu_by_rest_id(id, today)
    marmitas = query_all_marmitas_by_rest_id(id)
    if not menu or not marmitas:
        return "no_card"
    return build_html_for_menu(menu, marmitas)


def save_new_marmita(size, price, current_user):
    if query_marmita_by_size(size, current_user):
        return "Erro"
    return insert_new_marmita(size, price, current_user)


def show_all_marmitas(current_user):
    return query_all_marmitas(current_user)


def register_user_request(marmita_id, current_user, rest_id, foods):
    valor = 0
    itens = query_itens_from_menu(foods)
    for foods in itens:
        if foods[1]:
            valor += foods[1]

    marmita = query_marmita_by_id(marmita_id)
    valor += marmita.preco
    item = "{} - {}".format(marmita.tamanho, sorted([item[0] for item in itens]))

    return insert_into_user_extrato(item, valor,
                                    current_user, rest_id)


def update_bill(current_user, marmita_id, rest_id, foods):
    valor = 0
    menu = query_itens_from_menu(foods)
    for item in menu:
        if item[1]:
            valor += item[1]

    marmita = query_marmita_by_id(marmita_id)
    valor += marmita.preco

    if query_bill(current_user, rest_id):
        return update_user_bill(valor, current_user, rest_id)
    return create_user_account(valor, current_user, rest_id)


def del_item_from_menu(id_to_del):
    try:
        delete_item_from_menu_db(int(id_to_del))
        return "ok"
    except Exception:
        return "error"

def del_marm_size(id_to_del):
    try:
        delete_marm_from_db(int(id_to_del))
        return "ok"
    except Exception:
        return "error"
