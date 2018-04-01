from flask import Flask, abort, jsonify, render_template
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from models import Drivers, Events, Reports, Vehicles
from playhouse.shortcuts import model_to_dict

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = '1234567890'
app.config.from_pyfile('dev_config.py', silent=True)
admin = Admin(app, name='Fleet Management', template_mode='bootstrap3')


class FleetManagementView(ModelView):
    can_export = True
    can_view_details = True


class DriversView(FleetManagementView):
    column_editable_list = ('name', 'surname', 'birth')
    column_sortable_list = ('id', 'name', 'surname', 'birth')


class EventsView(FleetManagementView):
    column_editable_list = ('description')
    column_sortable_list = ('id', 'description')


class ReportsView(FleetManagementView):
    column_editable_list = ('driver', 'vehicle', 'lat', 'lon', 'alt', 'speed',
                            'event', 'time')
    column_sortable_list = ('id', 'driver', 'vehicle', 'lat', 'lon', 'alt',
                            'speed', 'event', 'time')


class VehiclesView(FleetManagementView):
    column_editable_list = ('plate', 'description')
    column_sortable_list = ('id', 'plate', 'description')


admin.add_view(DriversView(Drivers))
admin.add_view(EventsView(Events))
admin.add_view(ReportsView(Reports))
admin.add_view(VehiclesView(Vehicles))


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
