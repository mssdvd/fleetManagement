import datetime
import os

from peewee import (AutoField, CharField, DateField, FloatField,
                    ForeignKeyField, Model)
from playhouse.db_url import connect
from playhouse.postgres_ext import DateTimeTZField

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


class Roles(BaseModel):
    class Meta:
        table_name = "roles"

    id = AutoField()
    role = CharField()

    def __str__(self):
        return self.role


class Users(BaseModel):
    class Meta:
        table_name = "users"

    id = AutoField()
    name = CharField()
    surname = CharField()
    birth = DateField()
    role = ForeignKeyField(
        Roles,
        column_name="role",
    )

    def __str__(self):
        return f"{self.name} {self.surname}"


class Events(BaseModel):
    class Meta:
        table_name = "events"

    id = AutoField()
    description = CharField()

    def __str__(self):
        return self.description


class Vehicles(BaseModel):
    class Meta:
        table_name = "vehicles"

    id = AutoField()
    plate = CharField()
    description = CharField()

    def __str__(self):
        return self.plate


class Reports(BaseModel):
    class Meta:
        table_name = "reports"

    id = AutoField()
    driver = ForeignKeyField(Users, column_name="driver")
    vehicle = ForeignKeyField(Vehicles, column_name="vehicle")
    lat = FloatField()
    lon = FloatField()
    alt = FloatField()
    speed = FloatField()
    event = ForeignKeyField(Events, column_name="event")
    time = DateTimeTZField(datetime.datetime.now())
