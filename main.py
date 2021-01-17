from flask import Flask, url_for, render_template, request, flash, session, redirect, abort

app = Flask(__name__)

app.secret_key = "super secret key"
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

menu = [{'name': 'Главная', 'url': 'index'},
        {'name': 'О Нас', 'url': 'about'},
        {'name': 'Каталог', 'url': 'catalog'},
        {'name': 'Корзина', 'url': 'cart'},
        {'name': 'Войти', 'url': 'auth'}]

@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    return render_template('includes/index.html', menu = menu)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if len(request.form['login']) > 5 and len(request.form['password']) > 8:
            flash('Вход выполнен успешно')
        else:
            flash('Ошибка авторизации')

    return render_template('includes/form.html', menu=menu)

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'pavlik007' and request.form['password'] == 'Razor_007':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('includes/form.html', menu=menu)

@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль пользователя: {username}"

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('includes/page404.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)
    @app.after_request
    def add_header(response):
        response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response