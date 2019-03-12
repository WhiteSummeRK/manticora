from manticora.models.database.tables import Usuario, Restaurante, db


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


def insert_new_rest(phone, num_phone, img, adm):
    new_adm = Restaurante(telefone=num_phone + phone,
                          imagem=img.read(),
                          adm=adm)

    db.session.add(new_adm)
    db.session.commit()
    return new_adm


def check_for_existing_mail(mail):
    return len(Usuario.query.filter_by(email=mail).all()) > 0


def check_for_existing_name(nome):
    return len(Usuario.query.filter_by(nome=nome).all()) > 0


def query_user_and_pwd(user, pwd):
    return Usuario.query.filter_by(nome=user, senha=pwd).first()
