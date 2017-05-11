from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Any text'


if __name__ == '__main__':
    app.run()
