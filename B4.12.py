import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.Float)

class Athelete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.Integer, primary_key=True)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.TEXT)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    session = sessionmaker(engine)
    return session()

def request_data():
    print("Привет! Я запишу твои данные!")
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    gender = input("Введи свой пол: ")
    birthdate = input("Введи свою дату рождения: ")
    height = input("Введи свой рост: ")
    user = User(

        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        birthdate=birthdate,
        height=height,
    )
    return user

def find_user(id_find, session):
    """
    Производит поиск пользователя в таблице User по заданному идентификатору id_find
    """
    # нахдим все записи в таблице User, у которых поле User.id совпадает с парарметром id_find
    query = session.query(User).filter(User.id == id_find)
    # составляем список идентификаторов всех найденных пользователей
    user_ids = [user.id for user in query.all()]
    user_birthdate = [user.birthdate for user in query.all()]
    user_height = [user.height for user in query.all()]

    return (user_ids, user_birthdate,user_height )

def find_athelete(user_height,user_birthdate, session):
    """
    Производит поиск всех атлетов в таблице Athelete
    """

    query1 = session.query(Athelete).filter(Athelete.height == user_height)
    query2 = session.query(Athelete).filter(Athelete.birthdate == user_birthdate)
    # составляем список идентификаторов всех найденных пользователей
    athelete_height = {Athelete.name:Athelete.height for Athelete in query1[0:1]}
    athelete_birthdate = {Athelete.name:Athelete.birthdate for Athelete in query2[0:1]}
    return (athelete_height,athelete_birthdate)

def print_users_list(user_ids, user_birthdate,user_height ,athelete_height,athelete_birthdate):
    """
    Выводит на экран найденного пользователя, его имя и фамилию и данные найденного атлета.
    Если передан пустой идентификатор, выводит сообщение о том, что пользователя не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if user_ids:
        # если список не пуст, распечатываем найденного пользователя и атлета
        print("Найден пользователь id-{} д.р.{} рост {}".format(user_ids, user_birthdate, user_height ))
        if athelete_height:
            print("Найден атлет №1 с соответствующим ростом{}".format(athelete_height))
        else:
            print("Не найден атлет с соответствующим ростом")
        if athelete_birthdate:
            print("Найден атлет №2 соответствующей д.р.{}".format(athelete_birthdate))
        else:
            print("Не найден атлет с соответствующей датой рождения")

def main():
    session = connect_db()
    mode = input("Выбери режим.\n1 - найти пользователя по идентификатору\n2 - ввести данные нового пользователя\n")

    if mode == "1":
        id_find = input("Введите идентификатор пользователя")
        user_ids, user_birthdate, user_height = find_user(id_find, session)
        if user_height and user_birthdate:
            user_height = float(user_height[0])
            user_birthdate = str(user_birthdate[0])
            athelete_height, athelete_birthdate = find_athelete(user_height,user_birthdate, session)
            print_users_list(user_ids, user_birthdate, user_height, athelete_height,athelete_birthdate)
        else:
            # если список оказался пустым, выводим сообщение об этом
            print("Пользователя с таким идентификатором нет.")
    elif mode == "2":
        user = request_data()
        session.add(user)
        print(user)
        session.commit()
        print("Спасибо, данные сохранены!")

if __name__ == "__main__":
    main()
