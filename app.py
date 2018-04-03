from admin import admin
from api import api
from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = '1234567890'
app.config['ERROR_404_HELP'] = False
app.config.from_pyfile('dev_config.py', silent=True)
admin.init_app(app)
api.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
