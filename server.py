#!/usr/bin/python
#coding=utf-8

from flask import Flask, render_template, request, session, redirect, url_for, abort, flash

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


'''
@app.route('/addknowledge', methods=['POST'])
def enter_lecture():
    print "choose lecture success"
    if not session.get('logged_in'):
        abort(401)
    lecturename = request.form['lecture']
    print "lecturename = %s" % lecturename
    sql = "select id from lecture where lecturename = '%s'" % lecturename
    results = _query(_engine, sql)
    lecture = results.fetchone()
    if lecture:
        session['lid'] = lecture[0]
        print "~~~~~~~~~~~enter a lecture~~~~~~~~~~~~:::::%s" % session
        return redirect(url_for('show_lecture_details'))
    return render_template('show_lecture.html',)


@app.route('/lecture/<lecturename>')
def show_lecture_details():
    print 'success'
'''


@app.route('/list')
def show_lecture():
    from common.entity import Lecture
    tid = session.get('tid', 0)
    rows = db_session.query(Lecture).filter_by(tid=tid).all()
    lectures = [dict(lecturename=row.lecturename, time=row.time) for row in rows]
    return render_template('show_lecture.html', lectures=lectures)


@app.route('/addlecture', methods=['POST'])
def add_lecture():
    if not session.get('logged_in'):
        abort(401)

    from common.entity import Lecture
    lecture = Lecture(tid=session['tid'], lecturename=request.form['lecturename'], time=request.form['time'])
    db_session.add(lecture)
    db_session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_lecture'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        tid = request.form['teachername']
        pwd = request.form['password']
        sql = "select id from teacher where teachername = '%s' and password = '%s'" % (tid, pwd)
        results = _query(_engine, sql)
        teacher = results.fetchone()  # tuple return
        if teacher:
            session['logged_in'] = True
            session['tid'] = teacher[0]
            print "after login: %s" % session
            flash('You were logged in')
            return redirect(url_for('show_lecture'))
        else:
            error = "Invalid teachername or password"

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        from common.entity import Teacher
        teacher = Teacher(teachername=request.form['teachername'], password=request.form['password'])
        db_session.add(teacher)
        db_session.commit()
        return render_template('login.html', error=error)
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('uid', None)
    flash('You were logged out')
    return redirect(url_for('show_lecture'))


@app.route('/')
def hello():
    return 'Please visit /login'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
