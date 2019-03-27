from base64 import b64encode
from datetime import datetime
from manticora.models.database_functions.account import (
    query_user_accounts_by_user,
    query_account_by_id,
    find_all_extrato,
    query_all_account_in_rest,
    change_status)
from manticora.models.database_functions.usuario import query_user_by_id
from manticora.models.database_functions.restaurante import get_actual_rest


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
    <div class="card">
    <div class="card-body" id="addr">
    <h5 class="card-title">Restaurantes</h5>
    <table class="table">
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
    </div>
    </div>
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


def show_clients_account(current_user):
    rest = get_actual_rest(current_user)
    account = query_all_account_in_rest(rest)
    return account


def update_status_account(id_account):
    try:
        change_status(int(id_account), "Pago")
        return "ok"
    except Exception:
        return "Erro, Tente novamente mais tarde"


def mount_user_data(user_id):
    user = query_user_by_id(int(user_id))

    if user:
        html = """
        <p>Nome: {}</p>
        <p>Email: {}</p>
        <p>Cidade: {}</p>
        <p>Bairro: {}</p>
        <p>Rua: {}</p>
        <p>Numero: {}</p>
        <p>Complemento: {}</p><br>
        """.format(user.nome, user.email, user.cidade,
                   user.bairro, user.rua, user.numero, user.complemento)

        return html
    return "erro"
