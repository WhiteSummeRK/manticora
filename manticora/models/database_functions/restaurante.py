from datetime import datetime
from manticora.models.database.tables import Usuario, Restaurante, db
from sqlalchemy import or_, and_


def get_actual_rest(curr_user):
    user = Usuario.query.filter(Usuario.id == curr_user.id).first()
    return Restaurante.query.filter_by(adm=user).first()


def insert_new_rest(phone, num_phone, img, open, closed, adm):
    new_adm = Restaurante(telefone=num_phone + phone,
                          imagem=img.read(),
                          abertura=open,
                          fechamento=closed,
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
    open = get_open_rests(adms)
    closed = get_closed_rests(adms)
    return open + closed


def get_closed_rests(adm):
    now = get_time_now()
    result = []

    for item in adm:
        rest = Restaurante.query.filter(
            or_(Restaurante.fechamento < now,
                Restaurante.abertura > now)).filter_by(adm=item).first()

        if rest:
            result.append([item.nome, rest, 'Aberto'])

    return result


def get_open_rests(adm):
    now = get_time_now()
    result = []

    for item in adm:
        rests = Restaurante.query.filter(
                and_(Restaurante.fechamento > now,
                     Restaurante.abertura < now)).filter_by(adm=item).first()

        if rests:
            result.append([item.nome, rests, 'Aberto'])

    return result


def query_adm_by_city(city):
    if city == 'todos' or not city:
        return query_all_adms()
    return Usuario.query.filter(Usuario.cidade == city). \
        filter(Usuario.is_adm == True).all() #NOQA


def get_time_now():
    now_ = datetime.now().strftime('%H:%M')
    return datetime.strptime(now_, '%H:%M').time()


def show_closed_rests_by_city(city):
    adm = query_adm_by_city(city)
    return get_closed_rests(adm)


def show_openned_rests_by_city(city):
    adm = query_adm_by_city(city)
    return get_open_rests(adm)


def show_all_rests_by_city(city):
    rests_open = show_openned_rests_by_city(city)
    rests_closed = show_closed_rests_by_city(city)

    return rests_open + rests_closed
