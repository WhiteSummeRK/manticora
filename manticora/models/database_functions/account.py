from manticora.models.database.tables import Account, db

def insert_new_user_account(name, email, pwd):
    new_account = Account(name=name, email=email, pwd=pwd, is_adm=False)
    db.session.add(new_account)
    db.session.commit()
    return new_account

def check_for_existing_mail(mail):
    return len(Account.query.filter_by(email=mail).all()) > 0

def check_for_existing_name(name):
    return len(Account.query.filter_by(name=name).all()) > 0

def query_user_and_pwd(user, pwd):
    return Account.query.filter_by(name=user, pwd=pwd).first()
