from manticora.models.database.tables import Usuario, db


def insert_new_user_account(nome, senha,
                            email, bairro,
                            cidade, rua,
                            numero, complemento, is_adm):
    new_client = Usuario(
        nome=nome,
        senha=senha,
        email=email,
        bairro=bairro,
        cidade=cidade,
        rua=rua,
        numero=numero,
        complemento=complemento,
        is_adm=is_adm)

    db.session.add(new_client)
    db.session.commit()
    return new_client


def check_for_existing_mail(mail):
    return len(Usuario.query.filter_by(email=mail).all()) > 0


def check_for_existing_name(nome):
    return len(Usuario.query.filter_by(nome=nome).all()) > 0


def query_user_and_pwd(user, pwd):
    return Usuario.query.filter_by(nome=user, senha=pwd).first()


def update_user_from_db(city, neigh, street, num, complement, current_user):
    user = Usuario.query.filter_by(id=current_user.id).first()
    user.cidade = city if city else user.cidade
    user.bairro = neigh if neigh else user.bairro
    user.rua = street if street else user.rua
    user.numero = num if num else user.numero
    user.complemento = complement if complement else user.complemento

    db.session.commit()
