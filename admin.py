from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from models import Events, Reports, Roles, Users, Vehicles

admin = Admin(name='Fleet Management', template_mode='bootstrap3')


class FleetManagementView(ModelView):
    can_export = True
    can_view_details = True


class UsersView(FleetManagementView):
    column_editable_list = ('name', 'surname', 'birth', 'role')
    column_sortable_list = ('id', 'name', 'surname', 'birth', 'role')


class RolesView(FleetManagementView):
    column_editable_list = ('role')
    column_sortable_list = ('id', 'role')


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


admin.add_view(UsersView(Users))
admin.add_view(RolesView(Roles))
admin.add_view(EventsView(Events))
admin.add_view(ReportsView(Reports))
admin.add_view(VehiclesView(Vehicles))
