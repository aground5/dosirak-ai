import sqlite3

global_conn = sqlite3.connect("dosirak.sqlite")


def get_cursor():
    return global_conn.cursor()
