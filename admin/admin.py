from flask import Blueprint, request, redirect,render_template, url_for, flash, session, g
import sqlite3
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
    session['admin_logged'] = 1

def is_logged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

menu = [
    {'title': 'Панель', 'url': '.index'},
    {'title': 'Список пользователей', 'url': '.list_users'},
    {'title': 'Список статей', 'url': '.listpubs'},
    {'title': 'Выйти', 'url': '.logout'}
]

db = None
@admin.before_request
def before_request():
    global db
    db = g.get('link_db')

@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request

@admin.route('/')
def index():
    if  not is_logged():
        return redirect(url_for('.login'))

    return render_template('admin/includes/index.html', menu = menu, title = 'Панель администратора')

@admin.route('/login', methods=['POST', 'GET'])
def login():
    if is_logged():
        return redirect(url_for('.index'))
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '12345':
            login_admin()
            return redirect(url_for('.index'))

        else:
            flash('Incorrect login or password')

    return render_template('admin/includes/login.html', title= 'Панель администратора')

@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    if not is_logged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))

@admin.route('/list_pubs')
def listpubs():
    if not is_logged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, description, url FROM posts")
            list = cur.fetchall()

        except sqlite3.Error as e:
                print('Ошибка  получения статей из БД ' + str(e))

    return render_template('admin/includes/listpubs.html', title='Список статей', menu=menu, list=list)

@admin.route('/list_users')
def list_users():
    if not is_logged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT username, email FROM users ORDER BY time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print('Ошибка получения пользователей из БД ' + str(e))

    return render_template('admin/includes/listusers.html', title = 'Пользователи', menu = menu, list = list)