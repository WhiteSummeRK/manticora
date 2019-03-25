from manticora.models.database_functions.menu import (insert_menu,
                                                      query_all_menus,
                                                      query_menus_by_day,
                                                      query_menu_by_rest_id,
                                                      insert_new_marmita,
                                                      query_all_marmitas,
                                                      query_all_marmitas_by_rest_id,
                                                      query_marmita_by_size,
                                                      query_marmita_by_id,
                                                      query_itens_from_menu) # NOQA
from manticora.models.database_functions.user_account import (insert_into_user_extrato, #NOQA
                                                              update_user_bill,
                                                              create_user_account,
                                                              query_bill) #NOQA

from datetime import datetime


def save_menu(item, kind, day, current_user):
    item_kind = {
        "main_plate": "Prato Principal",
        "acomp": "Acompanhamento",
        "drink": "Bebida",
        "deserve": "Sobremesa",
        "other": "Outro"
    }
    if kind not in item_kind.keys():
        return "acha que foi inserido mas nem foi ein"
    return insert_menu(item, item_kind[kind], day, current_user)


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
    marmitas_html = "<p>Escolha o Tamanho</p>"
    for item in marmitas:
        marmitas_html += """
        <div class="form-check-inline">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" value={} name="marmitas" required>{} (R${})
          </label>
        </div>
        """.format(item.id, item.tamanho, item.preco) #NOQA
    html_head = """
    <form id='meu_form' action='/restaurants/make_request/' method="POST">
    {}
    <table class="table table-dark">
        <thead>
            <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo</th>
            <th scope="col">Pedido</th>
          </tr>
        </thead>
            <tbody>
    """.format(marmitas_html)
    html_end = """
        </tbody>
    </table>
    """
    html_middle = ""
    for item in menu:
        html_middle += """
            <tr>
              <td>{}</td>
              <td>{}</td>
              <td>
                  <div class="form-check">
            <input class="form-check-input" type="checkbox" value="{}" name="input_box" id="{}">
            <input type="hidden" name="btn_req" value={}>
                  </div>
              </td>
            </tr>
        """.format(item.prato, item.tipo, item.id, item.id, menu_id) #NOQA

    html_btn = """
    <button type="submit" onclick="confirm_dialog()" class="btn btn-primary mb-2">Realizar Pedido</button>
    </form>
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
    marmita = query_marmita_by_id(marmita_id)
    itens = query_itens_from_menu(foods)
    item = "{} - {}".format(marmita.tamanho, sorted(itens))

    return insert_into_user_extrato(item, marmita.preco,
                                    current_user, rest_id)


def update_bill(current_user, marmita_id, rest_id):
    marmita = query_marmita_by_id(marmita_id)
    if query_bill(current_user, rest_id):
        return update_user_bill(marmita.preco, current_user, rest_id)
    return create_user_account(marmita.preco, current_user, rest_id)
