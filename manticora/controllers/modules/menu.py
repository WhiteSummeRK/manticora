from manticora.models.database_functions.menu import (insert_menu,
                                                      query_all_menus,
                                                      query_menus_by_day,
                                                      query_menu_by_rest_id)
from datetime import datetime


def save_menu(item, kind, day, current_user):
    return insert_menu(item, kind, day, current_user)


def change_datetime(menus):
    for item in menus:
        item.dia = datetime.strptime(item.dia.strftime("%d-%m-%Y"), "%d-%m-%Y").date() #NOQA
    return menus


def show_menu_by_day(day, current_user):
    if not day:
        return change_datetime(query_all_menus(current_user))
    return change_datetime(query_menus_by_day(day, current_user))


def build_html_for_menu(menu):
    html_head = """
    <table class="table table-dark">
        <thead>
            <tr>
            <th scope="col">Nome</th>
            <th scope="col">Tipo</th>
            <th scope="col">Pedido</th>
          </tr>
        </thead>
            <tbody>
    """
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
            <input class="form-check-input" type="checkbox" value="{}" id="{}">
                  </div>
              </td>
            </tr>
        """.format(item.prato, item.tipo, item.id, item.id) #NOQA

    html_btn = """
    <button type="submit" class="btn btn-primary mb-2">Realizar Pedido</button>
    """ # NOQA

    return html_head + html_middle + html_end + html_btn


def show_card_by_rest_id(id):
    today = datetime.now().date()
    menu = query_menu_by_rest_id(id, today)
    if not menu:
        return "no_card"
    return build_html_for_menu(menu)
