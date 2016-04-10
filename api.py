#!/usr/bin/python
#coding=utf-8

from flask import Flask, render_template, request, session, redirect, url_for, abort, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE = '/tmp/flaskr.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def _create_engine(user, password, host, port, db, autocommit=False, pool_recycle=60):
    engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=utf8&use_unicode=1' % (
        user, password,
        host, port,
        db),
        pool_size=10,
        max_overflow=-1,
        pool_recycle=pool_recycle,
        connect_args={'connect_timeout': 1, 'autocommit': 1 if autocommit else 0})
    return engine

_engine = _create_engine("cdb_outerroot", "Wang1994", "56c406d81888d.sh.cdb.myqcloud.com", 4125, 'final_year')


def _query(engine, sql):
    connection = engine.connect()
    result = connection.execute(sql)
    connection.close()
    return result

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=_engine))
