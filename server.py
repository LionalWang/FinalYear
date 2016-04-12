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


@app.route('/student', methods=['GET'])
def show_student():
    from common.entity import Student
    rows = db_session.query(Student).all()
    students = [dict(student_number=row.studentname) for row in rows]
    return render_template('show_student.html', students=students)


@app.route('/addstudent', methods=['POST'])
def add_student():
    from common.entity import Student
    print request.form['student_number']
    student = Student(studentname=request.form['student_number'], password=request.form['student_number'])
    db_session.add(student)
    db_session.commit()
    return redirect(url_for('show_student'))


@app.route('/knowledge/<id>/<lecturename>', methods=['GET'])
def show_knowledge(id, lecturename):
    from common.entity import Knowledge
    session['lid'] = id
    session['lname'] = lecturename
    rows = db_session.query(Knowledge).filter_by(lid=id).all()
    knowledges = [dict(kid=row.id, kname=row.text, yes_count=row.yes_count, no_count=row.no_count) for row in rows]
    return render_template('add_knowledge.html', lecture=lecturename, knowledges=knowledges)


@app.route('/addknowledge', methods=['POST'])
def add_knowledge():
    from common.entity import Knowledge
    knowledge = Knowledge(lid=session['lid'], text=request.form['knowledgename'], yes_count=0, no_count=0, is_send=0)
    db_session.add(knowledge)
    db_session.commit()
    return redirect(url_for('show_knowledge', id=session['lid'], lecturename=session['lname']))


@app.route('/list')
def show_lecture():
    from common.entity import Lecture
    tid = session.get('tid', 0)
    rows = db_session.query(Lecture).filter_by(tid=tid).all()
    lectures = [dict(id=row.id, lecturename=row.lecturename, time=row.time) for row in rows]
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


'''


This part is interface


'''


@app.route('/api/login/teacher/<teachername>/<password>', methods=['GET'])
def teacherlogin(teachername, password):
    sql = "select id from teacher where teachername = '%s' and password = '%s'" % (teachername, password)
    results = _query(_engine, sql)
    teacher = results.fetchone()  # tuple return
    if teacher:
        result = [
            {
                'status': 1,
                'tid': teacher[0]
            }
        ]
    else:
        result = [
            {
                'status': 0,
                'tid': 0
            }
        ]
    return jsonify({'result': result})


@app.route('/api/lecture/<tid>', methods=['GET'])
def checklecture(tid):
    from common.entity import Lecture
    rows = db_session.query(Lecture).filter_by(tid=tid).all()
    result = []
    for row in rows:
        lecture = {'id': row.id,
                   'lecturename': row.lecturename,
                   'time': row.time}
        result.append(lecture)
    return jsonify({'result': result})


@app.route('/api/knowledge/<lid>', methods=['GET'])
def checkknowledge(lid):
    from common.entity import Knowledge
    rows = db_session.query(Knowledge).filter_by(lid=lid).all()
    result = []
    for row in rows:
        knowledge = {'id': row.id,
                     'text': row.text,
                     'yes_count': row.yes_count,
                     'no_count': row.no_count}
        result.append(knowledge)
    return jsonify({'result': result})


@app.route('/api/kdetail/<kid>', methods=['GET'])
def checkknowledgedetail(kid):
    from common.entity import Knowledge
    rows = db_session.query(Knowledge).filter_by(id=kid).all()
    result = []
    for row in rows:
        knowledge = {'id': row.id,
                     'text': row.text,
                     'yes_count': row.yes_count,
                     'no_count': row.no_count,
                     'is_send': row.is_send}
        result.append(knowledge)
    return jsonify({'result': result})


@app.route('/api/knowledge/update/<kid>', methods=['GET'])
def knowledge_update(kid):
    from common.entity import Knowledge
    rows = db_session.query(Knowledge).filter_by(id=kid).all()
    result = []
    for row in rows:

        if row.is_send == 1:
            row.is_send = 0
            db_session.commit()
            knowledge = {'id': row.id,
                         'text': row.text,
                         'yes_count': row.yes_count,
                         'no_count': row.no_count,
                         'is_send': row.is_send}
            result.append(knowledge)
        else:
            row.is_send = 1
            db_session.commit()
            knowledge = {'id': row.id,
                         'text': row.text,
                         'yes_count': row.yes_count,
                         'no_count': row.no_count,
                         'is_send': row.is_send}
            result.append(knowledge)

    return jsonify({'result': result})


@app.route('/api/knowledge/end/<kid>', methods=['GET'])
def knowledge_end(kid):
    from common.entity import Knowledge
    rows = db_session.query(Knowledge).filter_by(id=kid).all()
    result = []
    for row in rows:
        row.is_send = 0
        db_session.commit()
        knowledge = {'status': 1}
        result.append(knowledge)
    return jsonify({'result': result})


@app.route('/api/login/student/<studentname>/<password>', methods=['GET'])
def studentlogin(studentname, password):
    sql = "select id from student where studentname = '%s' and password = '%s'" % (studentname, password)
    results = _query(_engine, sql)
    student = results.fetchone()  # tuple return
    if student:
        result = [
            {
                'status': 1,
                'sid': student[0]
            }
        ]
    else:
        result = [
            {
                'status': 0,
                'sid': 0
            }
        ]
    return jsonify({'result': result})


@app.route('/api/student/choose/check', methods=['GET'])
def student_choose():
    from common.entity import Knowledge
    rows = db_session.query(Knowledge).filter_by(is_send=1).all()
    result = []
    for row in rows:
        knowledge = {'id': row.id,
                     'text': row.text,
                     'yes_count': row.yes_count,
                     'no_count': row.no_count,
                     'is_send': row.is_send}
        result.append(knowledge)
    return jsonify({'result': result})


@app.route('/api/student/commit/<kid>/<understand>', methods=['GET'])
def student_commit(kid, understand):
    from common.entity import Knowledge
    rows = db_session.query(Knowledge).filter_by(id=kid).all()
    print kid + "        " + understand

    result = []

    for row in rows:
        if understand == "true":
            row.yes_count=row.yes_count+1
            db_session.commit()
            status = {'status': 1}
            result.append(status)
        else:
            row.no_count = row.no_count+1
            db_session.commit()
            status = {'status': 0}
            result.append(status)

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
