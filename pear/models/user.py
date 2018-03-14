# coding=utf-8

from datetime import datetime
from sqlalchemy import select, or_

from pear.models.tables import engine, user


class UserDao(object):
    conn = engine.connect()

    @classmethod
    def get_by_id(cls, u_id):
        sql = select([user]).where(user.c.id == u_id)
        return cls.conn.execute(sql).first()

    @classmethod
    def is_exist(cls, name=None, email=None, mobile=None):
        sql = select([user]).where(or_(
            user.c.name == name,
            user.c.email == email,
            user.c.mobile == mobile
        ))
        return cls.conn.execute(sql).first()

    @classmethod
    def get_by_args(cls, password, account=None):
        sql = select([user]).where(user.c.passwd == password)
        if account:
            sql = sql.where(
                or_(
                    user.c.name == account,
                    user.c.mobile == account,
                    user.c.email == account
                )
            )
        return cls.conn.execute(sql).first()

    @classmethod
    def create(cls, name, password, email, mobile):
        sql = user.insert().values(
            name=name,
            passwd=password,
            created=datetime.now()
        )
        if email:
            sql = sql.values(email=email)
        if mobile:
            sql = sql.values(mobile=mobile)
        return cls.conn.execute(sql).inserted_primary_key[0]
