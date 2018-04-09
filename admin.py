from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from models import Event, Report, Role, User, Vehicle

admin = Admin(name='Fleet Management', template_mode='bootstrap3')


class FleetManagementView(ModelView):
    can_export = True
    can_view_details = True


class UserView(FleetManagementView):
    column_editable_list = ('name', 'surname', 'birth', 'role')
    column_sortable_list = ('id', 'name', 'surname', 'birth', 'role')


class RoleView(FleetManagementView):
    column_editable_list = ('role')
    column_sortable_list = ('id', 'role')


class EventView(FleetManagementView):
    column_editable_list = ('description')
    column_sortable_list = ('id', 'description')


class ReportView(FleetManagementView):
    column_editable_list = ('driver', 'vehicle', 'lat', 'lon', 'alt', 'speed',
                            'event', 'time')
    column_sortable_list = ('id', 'driver', 'vehicle', 'lat', 'lon', 'alt',
                            'speed', 'event', 'time')


class VehicleView(FleetManagementView):
    column_editable_list = ('plate', 'description')
    column_sortable_list = ('id', 'plate', 'description')


admin.add_view(UserView(User))
admin.add_view(RoleView(Role))
admin.add_view(EventView(Event))
admin.add_view(ReportView(Report))
admin.add_view(VehicleView(Vehicle))
