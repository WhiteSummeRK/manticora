"""Modulo de login"""
from manticora.models.database_functions.cliente import query_user_and_pwd


def login(user, pwd):
    suposed_user = query_user_and_pwd(user, pwd)
    return bool(suposed_user)
