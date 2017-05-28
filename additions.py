# -*- coding: utf-8 -*-
from flask import flash, url_for, redirect, session
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash(u'Необходимо сначала войти')
            return redirect(url_for('login_page'))
    return wrap

