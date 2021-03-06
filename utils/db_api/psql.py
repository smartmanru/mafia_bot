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

    return (b)


def select_psql(select):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(select)
    row = cursor.fetchall()
    cursor.close()
    conn.close()

    return row


def db_reg_upd(tg_id: int, fio: str, city: str, age: int, mf_nn: str, proof: str, dohod: str, ph_num: int, gender: str, photoid: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE mafiabot.user set fi_reg=%s, city=%s, age=%s, nickname_mafia=%s, proffesion=%s, dohod=%s, phone_number=%s, photo_id=%s, gender=%s WHERE telegram_id=%s',
        (fio, city, age, mf_nn, proof, dohod, ph_num, photoid, gender, tg_id,))
    conn.commit()
    cursor.close()
    conn.close()


def db_reg_new(tg_id: int, tg_nick: str, tg_fio: str, ):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO mafiabot.user (telegram_id, telegram_nickname, fi_tg) VALUES(%s, %s, %s)',
        (tg_id, tg_nick, tg_fio))
    conn.commit()
    cursor.close()
    conn.close()


def db_reg_sel_user(tg_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "select telegram_id from mafiabot.user where mafiabot.user.telegram_id = %s;", (tg_id,))
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    return row


def db_reg_sel_all_user(tg_id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        "select telegram_nickname,fi_reg,gender,age,proffesion,dohod,phone_number,nickname_mafia from mafiabot.user where mafiabot.user.telegram_id = %s;", (tg_id,))
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    return row

def db_user_sel_all(id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'select * from user where telegram_id = (%s)', (id,))
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    return row


def db_af_new(dates: datetime, location: str, decription: str, count: str, name: str, photoid: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO mafiabot.afisha (date, location, decription,max_count,name,photoid) VALUES(%s, %s, %s, %s, %s, %s)',
        (dates, location, decription, count, name, photoid))
    conn.commit()
    cursor.close()
    conn.close()


# def afisha_update
# def afisha select
# def subscribe


def db_af_sel():
    b = select_psql(
        'select  id, name, decription, max_count, location, date,photoid from mafiabot.afisha where "date" > now() order by  "date" asc')
    return (b)
# getallvagons=


def db_af_sel_id(id: int):
    b = select_psql(
        'select  name, date from mafiabot.afisha where id='+str(id)+";")
    return (b)


def db_idu_sel_count(id):
    c = select_psql(
        # 'select count(*) from mafiabot.idushie where "id_afisha" =' + str(id) + ' and "payed"=True;')
        'select sum(vagons), count(*) FROM mafiabot.idushie WHERE id_afisha = '+str(id) + ' and "payed"=True;')
    if c[0][0] == None:
        i = 0
    else:
        i = c[0][0]
    k = c[0][1]
    u = i+k
    return (str(u))


def db_idu_chk_reg(id: int, page: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'select * from mafiabot.idushie where ("id_users"=%s and "id_afisha"=%s)', (id, page))
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    return row


def db_idu_new_zap(id: int, page: int, vagons: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO mafiabot.idushie (id_users, id_afisha,vagons,reserv) VALUES(%s, %s,%s,TRUE)', (int(id), int(page), int(vagons)))
    conn.commit()
    cursor.close()
    conn.close()


def db_idu_upd_pay(id: int, page: int, pae=bool):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'Update  mafiabot.idushie set payed=True where  ("id_users"= %s and "id_afisha"= %s)', (int(id), int(page)))
    conn.commit()
    cursor.close()
    conn.close()


def db_idu_del(id: int):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM mafiabot.idushie WHERE id_afisha=(%s)', (id,))
    conn.commit()
    cursor.close()
    conn.close()




def db_log_upd(msg, state, callback):
    if not msg:
        msg = "NULL"
    if not state:
        state = "NULL"
    if not callback:
        callback = "NULL"
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO mafiabot.logs (message, callback,state) VALUES(%s, %s,%s)', (str(msg), str(callback), str(state)))
    conn.commit()
    cursor.close()
    conn.close()
