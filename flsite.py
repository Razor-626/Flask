import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort
from FDataBase import FDataBase

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'whrvbwjvwevhbrewjhuewfewjhb23jb23jb4jdbjbj'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    '''Вспомогательная функция для создания БД'''
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.route('/')
@app.route('/index')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('includes/index.html', menu=dbase.getMenu())

@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/posts')
def posts():
    '''Выводим посты'''
    db = get_db()
    dbase = FDataBase(db)
    return render_template('includes/posts.html', menu=dbase.getMenu(), posts=dbase.getPosts())

@app.route('/add_post', methods=['POST', "GET"])
def add_post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['title']) > 4 and len(request.form['description']) > 8:
            res = dbase.addPost(request.form['title'], request.form['description'])
            if not res:
                flash('Ошибка добавления стать.')
            else:
                flash('Статья добавлена успешно.')
        else:
            flash('Ошибка добавления статьи.')
    return render_template('includes/add_post.html', menu = dbase.getMenu())

@app.route('/post/<int:id_post>')
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)

    return render_template('includes/post.html', menu=dbase.getMenu(), title=title, post=post)

@app.errorhandler(404)
def pageNotFound(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template('includes/page404.html', menu=dbase.getMenu())

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['username']) > 6 and len(request.form['password']) > 8:
            res = dbase.addUser(request.form['username'], request.form['password'])
            if not res:
                flash('Ошибка регистрации.')
            else:
                flash('Регистрация прошла успешно.')
        else:
            flash('Ошибка регистрации.')

    return render_template('includes/form.html', menu=dbase.getMenu())

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        res = dbase.authorization(request.form['username'], request.form['password'])
        if res:
            flash('Авторизация прошла успешно.')
        else:
            flash('Ошибка авторизации 2')

    return render_template('includes/authorization.html', menu=dbase.getMenu())

if __name__ == '__main__':
    app.run(debug=True)