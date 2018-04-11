from flask import current_app, redirect, request, session, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.peewee import ModelView
from flask_admin.form import SecureForm
from flask_login.utils import current_user
from flask_wtf.csrf import _FlaskFormCSRF
from models import Event, Message, Report, Role, Trip, User, Vehicle, Company
from werkzeug.security import generate_password_hash
from wtforms.meta import DefaultMeta


class FleetManagementIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super(FleetManagementIndexView, self).index()


admin = Admin(
    name='Fleet Management',
    index_view=FleetManagementIndexView(),
    template_mode='bootstrap3')


class FleetManagementView(ModelView):
    can_export = True
    can_view_details = True

    class CustomSecureForm(SecureForm):
        # https://github.com/flask-admin/flask-admin/issues/858#issuecomment-354927745
        class Meta(DefaultMeta):
            csrf_class = _FlaskFormCSRF
            csrf_context = session

            @property
            def csrf_secret(self):
                return current_app.config.get('SECRET_KEY',
                                              current_app.secret_key)

    form_base_class = CustomSecureForm

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class CompanyView(FleetManagementView):
    column_editable_list = ('name', 'location')
    column_sortable_list = ('id', 'name', 'location')


class UserView(FleetManagementView):
    column_editable_list = ('name', 'surname', 'birth', 'role', 'username', 'employer')
    column_exclude_list = ('password')
    column_sortable_list = ('id', 'name', 'surname', 'birth', 'role',
                            'username', 'employer')

    def on_model_change(self, form, User, is_created):
        User.password = generate_password_hash(User.password)


class RoleView(FleetManagementView):
    column_editable_list = ('role', 'description')
    column_sortable_list = ('id', 'role', 'description')


class EventView(FleetManagementView):
    column_editable_list = ('description')
    column_sortable_list = ('id', 'description')


class ReportView(FleetManagementView):
    column_editable_list = ('trip', 'lat', 'lon', 'alt', 'speed', 'event',
                            'time')
    column_sortable_list = ('id', 'trip', 'lat', 'lon', 'alt', 'speed',
                            'event', 'time')


class TripView(FleetManagementView):
    column_editable_list = ('driver', 'vehicle', 'dest_name', 'dest_lat',
                            'dest_lon', 'dep_time', 'ret_time')
    column_sortable_list = ('id', 'driver', 'vehicle', 'dest_name', 'dest_lat',
                            'dest_lon', 'dep_time', 'ret_time')


class VehicleView(FleetManagementView):
    column_editable_list = ('plate', 'description')
    column_sortable_list = ('id', 'plate', 'description')


class MessageView(FleetManagementView):
    column_editable_list = ('vehicle', 'company', 'to_vehicle', 'message',
                            'time')
    column_sortable_list = ('id', 'vehicle', 'company', 'to_vehicle',
                            'message', 'time')


admin.add_view(CompanyView(Company))
admin.add_view(UserView(User))
admin.add_view(RoleView(Role))
admin.add_view(EventView(Event))
admin.add_view(ReportView(Report))
admin.add_view(TripView(Trip))
admin.add_view(VehicleView(Vehicle))
admin.add_view(MessageView(Message))
