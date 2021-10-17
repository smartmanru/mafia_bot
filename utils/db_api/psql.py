# import aiosqlite

#     b = []
#     async with aiosqlite.connect("./database.db") as db:
#         async with db.execute(select) as cursor:
#             rows = await cursor.fetchall()
#             if len(rows) > 0:
#                 for i in rows:
#                     b.append(i[0])
#                 await cursor.close()
#     return b


# from marshmallow.fields import Date
from datetime import datetime
import psycopg2
from data.config import DATABASE_URL


# def get_text_messages(message):
# us_id = message.from_user.id
# us_name = message.from_user.first_name
# us_sname = message.from_user.last_name
# username = message.from_user.username
#     time_msg = [str(message.date.year), str(message.date.month), str(message.date.day), str(message.date.hour),
#                 str(message.date.minute), str(message.date.second)]
#     time = "-".join(time_msg)
#     referal = message.get_args()
#     db_table_val(user_id=str(us_id), user_name=us_name, user_surname=us_sname, username=username, time=time,
#                  referal=referal)


# def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, time: str, referal: int):
#     conn = psycopg2.connect(DATABASE_URL)
#     cursor = conn.cursor()
#     cursor = conn.cursor()
#     cursor.execute(
#         'INSERT INTO public.active_user (user_id, user_name, user_surname, username, date_time,referel_id) VALUES (%s, %s, %s, %s, %s, %s)',
#         (user_id, user_name, user_surname, username, time, referal))
#     conn.commit()
#     cursor.close()
#     conn.close()

# t_id=message.from_user.id
# t_nickname=message.from_user.username
# t_fn=message.from_user.first_name
# t_sn=message.from_user.last_name
# "subscriber_channel" bool,
#     "FIO" text,
#     "city" text,
#     "age" text,
#     "nickname_mafia" text,
#     "proffesion" text,
#     "dohod" text,
#     "phone_number" text,

def select_sq3(select):

    b = []
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(select)
    row = cursor.fetchall()
    if len(row) > 0:
        for i in row:
            b.append(i[0])
    cursor.close()
    conn.close()

    return(b)


def select_psql(select):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(select)
    row = cursor.fetchall()
    cursor.close()
    conn.close()

    return row


def db_reg(tg_id: int, fio: str, city: str, age: int, mf_nn: str, proof: str, dohod: str, ph_num: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE mafiabot.user set fi_reg=%s, city=%s, age=%s, nickname_mafia=%s, proffesion=%s, dohod=%s, phone_number=%s WHERE telegram_id=%s', (fio, city, age, mf_nn, proof, dohod, ph_num, tg_id))
    conn.commit()
    cursor.close()
    conn.close()


def db_first(tg_id: int, tg_nick: str, tg_fio: str,):

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO mafiabot.user (telegram_id, telegram_nickname, fi_tg) VALUES(%s, %s, %s)', (tg_id, tg_nick, tg_fio))
    conn.commit()
    cursor.close()
    conn.close()


def db_user(tg_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "select telegram_id from mafiabot.user where mafiabot.user.telegram_id = %s;", (tg_id,))
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    return row


def afisha_new(dates: datetime, location: str, decription: str, count: str, name: str, photoid: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO mafiabot.afisha (date, location, decription,max_count,name,photoid) VALUES(%s, %s, %s, %s, %s, %s)', (dates, location, decription, count, name, photoid))
    conn.commit()
    cursor.close()
    conn.close()

# def afisha_update
# def afisha select
# def subscribe


def get_afisha():
    b = select_psql(
        'select  id, name, decription, max_count, location, date,photoid from mafiabot.afisha where "date" > now() order by  "date" asc')
    return(b)

def get_count(id):
    c=select_psql('select count(*) from mafiabot.idushie where "id_afisha" ='+str(id)+';')
    return(c)