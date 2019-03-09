from manticora.models.database.tables import Cliente, db


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


def check_for_existing_mail(mail):
    return len(Cliente.query.filter_by(email=mail).all()) > 0


def check_for_existing_name(nome):
    return len(Cliente.query.filter_by(nome=nome).all()) > 0


def query_user_and_pwd(user, pwd):
    return Cliente.query.filter_by(nome=user, senha=pwd).first()
