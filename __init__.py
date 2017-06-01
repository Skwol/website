# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from dbconnect import connection
from additions import login_required

TOPIC_DICT = Content()

app = Flask(__name__)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Regexp(r'^[A-Za-z0-9_-]{4,20}$', message=u'Неподходящее имя (используйте только латинские буквы или цифры)')])
    email = TextField('Email Address', [validators.Regexp(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', message=u'Неподходящий адрес (используйте только латинские буквы или цифры)')])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm', message=u'Пароли не совпадают!')])
    confirm = PasswordField('Repeat Password')
    acceptence = 'I accept the <a href="/tos/">Terms of Service</a> and the <a href="/privacy/">Privacy Notice.</a>'
    accept_tos = BooleanField(acceptence, [validators.Required()])


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        return login_page()
    return render_template('main.html')


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html', TOPIC_DICT=TOPIC_DICT)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_found(error):
    return render_template('405.html')


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == 'POST':
            data = c.execute('SELECT * FROM users WHERE username = (%s)', thwart(request.form['username']))
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash(u'Вы успешно зашли')
                return redirect(url_for('dashboard'))
            else:
                error = u'Не удалось войти, проверьте введенные данные и попытайтесь снова.'

        gc.collect()

        return render_template('login.html', error=error)

    except Exception as e:
        #  flash(e)
        error = u'Не удалось войти, проверьте введенные данные и попытайтесь снова.'
        return render_template('login.html', error=error)


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash(u'Вы вышли из системы!')
    gc.collect()
    return redirect(url_for('dashboard'))


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute('SELECT * FROM users WHERE username = (%s)', thwart(username))

            if int(x) > 0:
                flash('That username is already taken, please choose another')
                return render_template('register.html', form=form)
            else:
                c.execute('INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)',
                          (thwart(username), thwart(password), thwart(email), thwart('/step-1-ide/')))
                conn.commit()

                flash(u'Вы успешно зарегистрировались!')
                c.close()
                conn.close()

                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template('register.html', form=form)

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
