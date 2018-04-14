import datetime
import os

from flask_login import UserMixin
from peewee import (AutoField, BooleanField, CharField, DateField, FloatField,
                    ForeignKeyField, Model)
from playhouse.db_url import connect
from playhouse.postgres_ext import DateTimeTZField
from werkzeug.security import check_password_hash, generate_password_hash

#  If it exits the dev_config module set the DATABASE_URL env variable
try:
    import dev_config
except Exception:
    pass


class BaseModel(Model):
    class Meta:
        try:
            database = connect(os.getenv('DATABASE_URL'), autorollback=True)
        except TypeError:
            print("Please set DATABASE_URL env variable")


class Company(BaseModel):
    class Meta:
        table_name = "company"

    id = AutoField()
    name = CharField(unique=True)
    location = CharField()

    def __str__(self):
        return self.name


class Role(BaseModel):
    class Meta:
        table_name = "role"

    id = AutoField()
    role = CharField(unique=True)
    description = CharField(null=True)

    def __str__(self):
        return self.role


class User(UserMixin, BaseModel):
    class Meta:
        table_name = "user"

    id = AutoField()
    name = CharField()
    surname = CharField()
    birth = DateField()
    employer = ForeignKeyField(Company, column_name="employer")
    role = ForeignKeyField(Role, column_name="role")
    username = CharField(unique=True)
    password = CharField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.username})"


class Event(BaseModel):
    class Meta:
        table_name = "event"

    id = AutoField()
    description = CharField()

    def __str__(self):
        return self.description


class Vehicle(BaseModel):
    class Meta:
        table_name = "vehicle"

    id = AutoField()
    plate = CharField()
    description = CharField()

    def __str__(self):
        return self.plate


class Trip(BaseModel):
    class Meta:
        table_name = "trip"

    id = AutoField()
    driver = ForeignKeyField(User, column_name="driver")
    vehicle = ForeignKeyField(Vehicle, column_name="vehicle")
    dest_name = CharField()
    dest_lat = FloatField()
    dest_lon = FloatField()
    dep_time = DateTimeTZField()
    ret_time = DateTimeTZField(null=True)

    def __str__(self):
        return f"{self.dest_name} {self.dep_time}"


class Report(BaseModel):
    class Meta:
        table_name = "report"

    id = AutoField()
    trip = ForeignKeyField(Trip, column_name="trip")
    lat = FloatField()
    lon = FloatField()
    alt = FloatField()
    speed = FloatField()
    event = ForeignKeyField(Event, column_name="event")
    time = DateTimeTZField(default=datetime.datetime.now())


class Message(BaseModel):
    class Meta:
        table_name = "message"

    id = AutoField()
    vehicle = ForeignKeyField(Vehicle, column_name="vehicle")
    company = ForeignKeyField(Company, column_name="company")
    to_vehicle = BooleanField()
    message = CharField()
    time = DateTimeTZField(default=datetime.datetime.now())

    def __str__(self):
        return f"{self.message} {self.time}"
