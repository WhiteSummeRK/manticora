from flask import abort
from sqlalchemy.orm.exc import UnmappedInstanceError
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
from manticora.models.database_functions.default_menus import (
    query_card_default_by_day
)
from manticora.models.database_functions.restaurante import (query_rest_by_id,
                                                             get_actual_rest)

from datetime import datetime
from time import strptime, strftime


def save_menu(item, kind, day, preco_item, current_user):
    item_kind = {
        "main_plate": "Prato Principal",
        "acomp": "Acompanhamento",
        "drink": "Bebida",
        "deserve": "Sobremesa",
        "snack": "Lanche",
        "pizza": "Pizza",
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
    rest = get_actual_rest(current_user)
    week_day = datetime.today().weekday()
    weekday_num = {
        0: "Segunda-Feira",
        1: "Terça-Feira",
        2: "Quarta-Feira",
        3: "Quinta-Feira",
        4: "Sexta-Feira",
        5: "Sábado",
        6: "Domingo"
    }
    weekday = {
        "Monday": "Segunda-Feira",
        "Tuesday": "Terça-Feira",
        "Wednesday": "Quarta-Feira",
        "Thursday": "Quinta-Feira",
        "Friday": "Sexta-Feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    try:
        if not day:
            default_cards = query_card_default_by_day(weekday_num[week_day], rest)
            all_cards = change_datetime(query_all_menus(current_user))
            return default_cards + all_cards
        _day = strftime("%A", strptime(day, "%m/%d/%Y"))
        weekday_filter = query_card_default_by_day(weekday[_day], rest)
        return weekday_filter + change_datetime(query_menus_by_day(day, current_user))
    except Exception:
        abort(400)


def build_html_for_menu(menu, marmitas, msg):
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
    <h5 class="card-title">{}</h5>
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
    """.format(msg, marmitas_html)
    html_end = """
        </tbody>
    </table>
    <button type="submit" onclick="confirm_dialog()" class="btn login_btn mb-2">Realizar Pedido</button>
    <button type="button" id="go_back" class="btn login_btn mb-2">Voltar</button>
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


def show_card_by_rest_id(id, tipo):
    today = datetime.now().date()
    week_day = datetime.today().weekday()
    rest = query_rest_by_id(int(id))
    weekday_num = {
        0: "Segunda-Feira",
        1: "Terça-Feira",
        2: "Quarta-Feira",
        3: "Quinta-Feira",
        4: "Sexta-Feira",
        5: "Sábado",
        6: "Domingo"
    }
    marmita = ['Adicional', 'Acompanhamento', 'Prato Principal', 'Bebida', 'Sobremesa']
    lanche = ['Lanche', 'Bebida', 'Sobremesa']
    pizza = ['Pizza', 'Bebida', 'Sobremesa']
    other = ['Outro']

    marmitas = query_all_marmitas_by_rest_id(id)

    default_day_menu = query_card_default_by_day(weekday_num[week_day], rest)
    menu_for_today = query_menu_by_rest_id(id, today)

    menu = default_day_menu + menu_for_today

    marm_menu = [item for item in menu if item.tipo in marmita]
    lanche_menu = [item for item in menu if item.tipo in lanche]
    pizza_menu = [item for item in menu if item.tipo in pizza]
    other_menu = [item for item in menu if item.tipo in other]

    if tipo == 'marmita':
        if not marm_menu or not marmitas:
            return "no_card"
        return build_html_for_menu(marm_menu,
                                   marmitas,
                                   "Monte sua marmita ^^")

    if tipo == 'lanche':
        if not lanche_menu:
            return "no_card"
        return build_html_for_menu(lanche_menu, [],
                                   'Escolha seu lanche, também leve uma bebidinha :D')

    if tipo == 'pizza':
        if not pizza_menu:
            return "no_card"
        return build_html_for_menu(pizza_menu, [],
                                   'Hmmmmm, essas pizzas parecem saborosas :3')

    if tipo == 'other':
        if not other_menu:
            return "no_card"
        return build_html_for_menu(other_menu, [],
                                   'Relaxe, temos de tudo pra você! (:')

    if tipo == 'rest_data':
        return build_html_with_rest_data(id)


def build_html_with_rest_data(id):
    rest = query_rest_by_id(int(id))
    html = """
    <div class="card">
    <div class="card-body">
    <h5 class="card-title">Restaurante {}</h5>
    <div class="container" id="address">
          <p>Email: {}</p>
          <p>Telefone: {}</p>
          <p>Horário de Abertura: {}</p>
          <p>Horário de Fechamento: {}</p>
          <br>
          <h5>Endereço</h5>
          <br>
          <p>Cidade: {}</p>
          <p>Bairro: {}</p>
          <p>Rua: {}</p>
          <p>Numero: {}</p>
          <p>Complemento: {}</p>
    </div>
    </div>
    </div>
    """.format(
        rest.adm.nome,
        rest.adm.email,
        rest.telefone,
        rest.abertura,
        rest.fechamento,
        rest.adm.cidade,
        rest.adm.bairro,
        rest.adm.rua,
        rest.adm.numero,
        rest.adm.complemento
    )
    return html


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

    if marmita_id:
        marmita = query_marmita_by_id(marmita_id)
        valor += marmita.preco
        item = "{} - {}".format(marmita.tamanho, sorted([item[0] for item in itens]))
    else:
        item = "{}".format(sorted([item[0] for item in itens]))

    return insert_into_user_extrato(item, valor,
                                    current_user, rest_id)


def update_bill(current_user, marmita_id, rest_id, foods):
    valor = 0
    menu = query_itens_from_menu(foods)
    for item in menu:
        if item[1]:
            valor += item[1]

    if marmita_id:
        marmita = query_marmita_by_id(marmita_id)
        valor += marmita.preco

    if query_bill(current_user, rest_id):
        return update_user_bill(valor, current_user, rest_id)
    return create_user_account(valor, current_user, rest_id)


def del_item_from_menu(id_to_del):
    try:
        delete_item_from_menu_db(int(id_to_del))
        return "ok"
    except UnmappedInstanceError:
        return "only_full_card"
    except Exception:
        return "error"

def del_marm_size(id_to_del):
    try:
        delete_marm_from_db(int(id_to_del))
        return "ok"
    except Exception:
        return "error"
