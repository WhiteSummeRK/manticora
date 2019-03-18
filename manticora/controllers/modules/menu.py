from manticora.models.database_functions.menu import (insert_menu,
                                                      query_all_menus,
                                                      query_menus_by_day)


def save_menu(item, kind, day, current_user):
    return insert_menu(item, kind, day, current_user)


def show_menu_by_day(day, current_user):
    if not day:
        return query_all_menus(current_user)
    return query_menus_by_day(day, current_user)
