from manticora.models.database.tables import Usuario, Restaurante, db


def insert_new_rest(phone, num_phone, img, adm):
    new_adm = Restaurante(telefone=num_phone + phone,
                          imagem=img.read(),
                          adm=adm)

    db.session.add(new_adm)
    db.session.commit()
    return new_adm


def query_all_adms():
    try:
        return Usuario.query.filter_by(is_adm=True).all()
    except Exception as e:
        db.session.rollback()
        raise


def query_ads_by_name(name):
    if not name:
        return query_all_adms()
    try:
        return Usuario.query.filter(Usuario.is_adm == True).filter(Usuario.nome.contains(name)).all() # NOQA
    except Exception as e:
        db.session.rollback()
        raise


def query_all_restaurants_with_name(adms):
    return [[item.nome, Restaurante.query.filter_by(adm=item).first()]
            for item in adms]
