from manticora.models.database.tables import Cliente, Restaurante, db


def insert_new_user_account(nome, senha,
                            email, bairro,
                            cidade, rua,
                            numero, complemento):
    new_client = Cliente(
        nome=nome,
        senha=senha,
        email=email,
        bairro=bairro,
        cidade=cidade,
        rua=rua,
        numero=numero,
        complemento=complemento)

    db.session.add(new_client)
    db.session.commit()
    return new_client


def insert_new_adm_account(name, email,
                           phone, num_phone,
                           pwd, neigh,
                           city, street,
                           num_street, comp, img):
    new_adm = Restaurante(nome=name, senha=pwd,
                          telefone=num_phone + phone,
                          email=email, bairro=neigh,
                          cidade=city, rua=street,
                          numero=num_street, complemento=comp,
                          imagem=img.read())

    db.session.add(new_adm)
    db.session.commit()
    return new_adm


def check_for_existing_mail_adm(mail):
    return len(Restaurante.query.filter_by(email=mail).all()) > 0


def check_for_existing_mail(mail):
    return len(Cliente.query.filter_by(email=mail).all()) > 0


def check_for_existing_name(nome):
    return len(Cliente.query.filter_by(nome=nome).all()) > 0


def check_for_existing_name_adm(nome):
    return len(Restaurante.query.filter_by(nome=nome).all()) > 0


def query_user_and_pwd(user, pwd):
    return Cliente.query.filter_by(nome=user, senha=pwd).first()
