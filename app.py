from admin import admin
from api import api
from flask import Flask, abort, jsonify, render_template
from models import Reports
from playhouse.shortcuts import model_to_dict

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = '1234567890'
app.config['ERROR_404_HELP'] = False
app.config.from_pyfile('dev_config.py', silent=True)
admin.init_app(app)
api.init_app(app)


@app.route('/api/reports/')
@app.route('/api/reports/<int:id>')
def get_reports(id=None):
    try:
        if id is None:
            query = Reports.select().order_by(Reports.id)
            return jsonify([model_to_dict(row) for row in query])
        return jsonify(model_to_dict(Reports.get_by_id(id)))
    except Reports.DoesNotExist:
        abort(404)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
