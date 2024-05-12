import sqlite3

con = sqlite3.connect("dosirak.sqlite")
cur = con.cursor()
cur.execute('''
    CREATE TABLE user (
        USER_ID TEXT PRIMARY KEY,
        PWD TEXT NOT NULL,
        DUID TEXT NOT NULL,
        DUID_NM TEXT NOT NULL,
        RGSN_DTTM TEXT NOT NULL,
        USER_NM TEXT NOT NULL
    );
''')

cur.execute('''
    CREATE TABLE naver_spell (
        REG_DT TEXT PRIMARY KEY,
        PASSPORT_KEY TEXT NOT NULL
    );
''')

cur.close()
con.close()