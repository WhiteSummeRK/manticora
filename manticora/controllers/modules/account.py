from base64 import b64encode
from datetime import datetime
from manticora.models.database_functions.account import (
    query_user_accounts_by_user,
    query_account_by_id,
    find_all_extrato)


def show_rests_accounts(current_user):
    accounts = query_user_accounts_by_user(current_user)
    rests = [[item.restaurante.adm.nome,
              item.restaurante,
              item.conta,
              item.status,
              item.id]
             for item in accounts]
    for item in rests:
        item[1].imagem = b64encode(item[1].imagem).decode('utf-8')
    return rests


def query_account_and_build_html(id):
    account = query_account_by_id(id)
    extrato = find_all_extrato(account)
    html_head = """
    <h3>Extrato de {} (Ultimos 30 pedidos)</h3>
    <table class="table table-dark">
        <thead>
            <tr>
            <th scope="col">Data</th>
            <th scope="col">Itens</th>
            <th scope="col">Valor</th>
          </tr>
        </thead>
            <tbody>
    """.format(account.restaurante.adm.nome)
    html_end = """
        </tbody>
    </table>
    """
    html_middle = ""
    for item in extrato:
        html_middle += """
            <tr>
              <td>{}</td>
              <td>{}</td>
              <td class="red">{}</td>
            </tr>
        """.format(item.data.date(), item.itens.replace('[', '').replace(']', '').replace('\'', ''), item.valor) #NOQA
    return html_head + html_middle + html_end
