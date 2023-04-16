from sqlalchemy import *
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/vkinder")

metadata = MetaData(bind=engine)
session = Session()
print(engine)


class Users(Base):
    __table__ = Table('users', metadata, autoload=True)


class UserClient(Base):
    __table__ = Table('Users/Client', metadata, autoload=True)


class Favorite(Base):
    __table__ = Table('favoriteclients', metadata, autoload=True)


class UsersPropose(Base):
    __table__ = Table('Users/Propose', metadata, autoload=True)


users = Users
user_client = UserClient
user_prop = UsersPropose
favorite = Favorite


def ins_data(user_id, user_age, user_gender, user_city):
    conn = engine.connect()
    sel = select(Users).where(Users.user_id == user_id)
    if conn.execute(sel).fetchall():
        upd = update(Users).where(Users.user_id == user_id).values(
            user_age=user_age,
            user_gender=user_gender,
            user_city=user_city
        )
        conn.execute(upd)
    else:
        ins = insert(Users).values(
            user_id=user_id,
            user_age=user_age,
            user_gender=user_gender,
            user_city=user_city
        )
        conn.execute(ins)


def ins_fav_data(user_id, client_id, client_name, client_surname, client_link, client_photo):
    conn = engine.connect()
    sel = select(Favorite).where(Favorite.client_id == client_id)
    if conn.execute(sel).fetchall():
        return
    else:
        ins = insert(Favorite).values(
            client_id=client_id,
            client_name=client_name,
            client_surname=client_surname,
            client_link=client_link,
            client_photos=client_photo
        )
        conn.execute(ins)
        ins_user_client(user_id, client_id)
        print('add to favorite')


def ins_user_client(user_id, fav_client_id):
    conn = engine.connect()
    ins = insert(UserClient).values(
        user_id=user_id,
        favoriteclient_id=fav_client_id
    )
    conn.execute(ins)


def ins_propose_data(user_id, client_id):
    conn = engine.connect()
    sel = select(UsersPropose).where(and_(UsersPropose.prop_client_id == client_id, UsersPropose.user_id == user_id))
    if conn.execute(sel).fetchall():
        return
    else:
        ins = insert(UsersPropose).values(
            user_id=user_id,
            prop_client_id=client_id
        )
        conn.execute(ins)
        print('add to user_prop')


def sel_prop_data(user_id):
    conn = engine.connect()
    sel = select(user_prop).where(user_prop.user_id == user_id)
    res = conn.execute(sel)
    res_list = [i for i in res]
    return res_list


# Выбор запроса по пользователю
def sel_user_data(user_id):
    conn = engine.connect()
    sel = select(users).where(users.user_id == user_id)
    res = conn.execute(sel)
    res_list = ([i for i in res])
    return res_list


def select_fav_client(user_id):
    conn = engine.connect()
    sel = select(favorite).join(user_client).where(user_client.user_id == user_id)
    res = conn.execute(sel)
    res_list_fav = ([i for i in res])
    return res_list_fav
