from admin import admin
from flask import Flask, abort, jsonify, render_template
from models import Drivers, Events, Reports, Vehicles
from playhouse.shortcuts import model_to_dict

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = '1234567890'
app.config.from_pyfile('dev_config.py', silent=True)


@app.route('/api/drivers/')
@app.route('/api/drivers/<int:id>')
def get_drivers(id=None):
    try:
        if id is None:
            query = Drivers.select().order_by(Drivers.id)
            return jsonify([model_to_dict(row) for row in query])
        return jsonify(model_to_dict(Drivers.get_by_id(id)))
    except Drivers.DoesNotExist:
        abort(404)


@app.route('/api/events/')
@app.route('/api/events/<int:id>')
def get_events(id=None):
    try:
        if id is None:
            query = Events.select().order_by(Events.id)
            return jsonify([model_to_dict(row) for row in query])
        return jsonify(model_to_dict(Events.get_by_id(id)))
    except Events.DoesNotExist:
        abort(404)
admin.init_app(app)


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


@app.route('/api/vehicles/')
@app.route('/api/vehicles/<int:id>')
def get_vehicles(id=None):
    try:
        if id is None:
            query = Vehicles.select().order_by(Vehicles.id)
            return jsonify([model_to_dict(row) for row in query])
        return jsonify(model_to_dict(Vehicles.get_by_id(id)))
    except Vehicles.DoesNotExist:
        abort(404)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
