from manticora.models.database.tables import db, CardapioPadrao


def default_card_insert(dia, tipo, item, preco, rest):
    try:
        new_card = CardapioPadrao(
            dia=dia,
            prato=item,
            tipo=tipo,
            preco=preco,
            rest=rest
        )
        db.session.add(new_card)
        db.session.commit()
    except Exception:
        db.session.rollback()
        db.session.remove()
        raise


def query_all_menus(rest):
    try:
        return CardapioPadrao.query.filter_by(rest=rest).all()
    except Exception:
        db.session.rollback()
        db.session.remove()
        raise
