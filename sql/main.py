import sqlite3

conn = sqlite3.connect("task.sql")
with conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS USERS_DATA (
    first_name TEXT,
    last_name TEXT,
    patronymic TEXT,
    date_of_birth TEXT,
    year_from_school INTEGER,
    year_to_univer INTEGER,
    phone TEXT,
    operator TEXT
);
""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS DIARY (
    last_name TEXT,
    math INTEGER,
    dmath INTEGER,
    prog INTEGER,
    ncml INTEGER
    );
    """)


def create_users():
    from mimesis.builtins import RussiaSpecProvider
    from mimesis.locales import Locale
    from mimesis import Person, Gender
    from random import choice, randint
    op = ['T2', 'Beeline', 'MTS', 'Yota']
    ru_spec = RussiaSpecProvider()
    for _ in range(10):
        person = Person(Locale.RU)
        name, last_name, pat = person.first_name(Gender.MALE), person.last_name(Gender.MALE), ru_spec.patronymic(Gender.MALE)
        data_birth = person.birthdate()
        phone = person.phone_number()
        operator = choice(op)
        conn.execute("""
        INSERT INTO USERS_DATA (first_name, last_name, patronymic, date_of_birth, year_from_school, year_to_univer, phone, operator) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, last_name, pat, str(data_birth), choice([2024, 2023, 2022]), choice([2024, 2023]), phone, operator,))
        conn.execute("""
        INSERT INTO DIARY (last_name, math, dmath, prog, ncml) VALUES (?, ?, ?, ?, ?)
        """, (last_name, randint(1, 10), randint(1, 10),randint(1, 10),randint(1, 10), ))
        conn.commit()

def sort_last_name():
    u = conn.execute("""
    SELECT * FROM USERS_DATA ORDER BY last_name ASC;
    """).fetchall()
    d = conn.execute("""
    SELECT * FROM DIARY ORDER BY last_name ASC;
    """).fetchall()
    return u, d

def get_users_to_operator(op):
    u = conn.execute(f"""
    SELECT * FROM USERS_DATA WHERE operator = '{op}';
    """).fetchall()
    return u
def get_users_to_names(names):
    u = conn.execute(f"""
    SELECT * FROM USERS_DATA WHERE first_name IN {tuple(names)};
    """).fetchall()
    return u

def get_users_to_bdate(month):
    u = conn.execute(f"""
    SELECT * FROM USERS_DATA WHERE strftime('%m', date_of_birth) = '{month}';
    """).fetchall()
    return u

def get_users_to_year(yy=2024):
    u = conn.execute(f"""
    SELECT * FROM USERS_DATA WHERE year_from_school = {yy} AND year_to_univer == {yy};
    """).fetchall()
    return u

def get_users_to_balls(ball=15):
    u = conn.execute(f"""
    SELECT last_name FROM DIARY WHERE math + dmath + prog + ncml >= {ball};
    """).fetchall()
    return u

def get_bad_users(ball=15):
    u = [ item[0] for i, item in enumerate(conn.execute(f""" SELECT last_name FROM DIARY WHERE math + dmath + prog + ncml <= {ball}; """).fetchall())]

    users = conn.execute(f"""
    SELECT phone FROM USERS_DATA WHERE last_name IN {tuple(u)};
    """).fetchall()

    u = [(item, users[i][0]) for i, item in enumerate(u)]
    return u

def get_users_to_mid(b = 20):
    u = conn.execute(f"""
    SELECT last_name FROM DIARY WHERE (math + dmath + prog + ncml) / 4 >= {b};
    """).fetchall()
    return u
# create_users()
print(sort_last_name()[0])
#a
print(get_users_to_operator('Yota'))
#b
print(get_users_to_year())
#c
print(get_users_to_names(['Вавила', 'Влас']))
#d
print(get_users_to_bdate('05'))
#e
print(get_users_to_balls())
#f
print(get_users_to_balls(25))
#g
print(get_bad_users())
#h
print(get_users_to_mid(7))
