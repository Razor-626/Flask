import sqlite3, os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm, RegistrForm
from admin.admin import admin

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'whrvbwjvwevhbrewjhuewfewjhb23jb23jb4jdbjbj'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

app.register_blueprint(admin, url_prefix='/admin')

login_manager = LoginManager(app)
login_manager.login_view = 'auth'
login_manager.login_message = 'Авторизируйтесь для доступа к данной странице.'


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)

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

dbase = None
@app.before_request
def before_request():
    """Соединение с БД"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.route('/')
@app.route('/index')
def index():
    return render_template('includes/index.html', menu=dbase.getMenu())

@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/posts')
def posts():
    '''Выводим посты'''
    return render_template('includes/posts.html', menu=dbase.getMenu(), posts=dbase.getPosts())

@app.route('/add_post', methods=['POST', "GET"])
def add_post():

    if request.method == "POST":
        if len(request.form['title']) > 4 and len(request.form['description']) > 8 and len(request.form['url']) > 1:
            res = dbase.addPost(request.form['title'], request.form['url'], request.form['description'])
            if not res:
                flash('Ошибка добавления стать.')
            else:
                flash('Статья добавлена успешно.')
        else:
            flash('Ошибка добавления статьи.')
    return render_template('includes/add_post.html', menu = dbase.getMenu())

@app.route('/post/<alias>')
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('includes/post.html', menu=dbase.getMenu(), title=title, post=post)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('includes/page404.html', menu=dbase.getMenu())

@app.route('/reg', methods=['POST', 'GET'])
def reg():

    if request.method == 'POST':
        if len(request.form['username']) > 6 and len(request.form['password']) > 8:
            res = dbase.addUser(request.form['username'], request.form['password'])
            if not res:
                flash('Оши бка регистрации.')
            else:
                flash('Регистрация прошла успешно.')
        else:
            flash('Ошибка регистрации.')

    return render_template('includes/form.html', menu=dbase.getMenu())

@app.route('/auth', methods=['POST', 'GET'])
def auth():

    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['password'], form.password.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))

        flash('Неверный логин или пароль')

    """if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('rememberme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))

        flash('Неверный логин или пароль')
        """
    return render_template('includes/authorization.html', menu=dbase.getMenu(), form = form)

@app.route('/registr', methods=['POST', 'GET'])
def registr():

    form = RegistrForm()
    if form.validate_on_submit():
        hash = generate_password_hash(request.form['password'])
        res = dbase.addUser(request.form['username'], request.form['email'], hash)
        if res:
            flash('Регистрация прошла успешно.')
            return redirect(url_for('auth'))
        else:
            flash('Ошибка регистрации.')
    return render_template('includes/registration.html', menu = dbase.getMenu(), form = form)

@app.route('/profile')
def profile():
    return render_template('includes/profile.html', menu= dbase.getMenu())

@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.')
    return redirect(url_for('auth'))

@app.route('/upload', methods = ['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash('Ошибка обновления аватара.')

                flash('Аватар обновлен')
            except FileNotFoundError as e:
                flash('Ошибка чтения файла' + str(e))
        else:
            flash('Ошибка обновления аватара.')

    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)