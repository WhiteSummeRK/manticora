from manticora.models.database.tables import Usuario, Restaurante, db


def insert_new_rest(phone, num_phone, img, adm):
    new_adm = Restaurante(telefone=num_phone + phone,
                          imagem=img.read(),
                          adm=adm)

    db.session.add(new_adm)
    db.session.commit()
    return new_adm
