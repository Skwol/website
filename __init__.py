from flask import Flask, render_template
from content_management import Content

TOPIC_DICT = Content()

app = Flask(__name__)


@app.route('/')
def homepage():
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
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
