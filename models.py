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
            database = connect(os.getenv('DATABASE_URL'))
        except TypeError:
            print("Please set DATABASE_URL env variable")


class Drivers(BaseModel):
    class Meta:
        table_name = "drivers"

    id = AutoField()
    name = CharField(null=False)
    surname = CharField(null=False)
    birth = DateField()

    # @property
    # def serialize(self):
    #     data = {
    #         "id": self.id,
    #         "name": self.name,
    #         "surname": self.surname,
    #         "birth": self.birth,
    #     }


class Events(BaseModel):
    class Meta:
        table_name = "events"

    id = AutoField()
    description = CharField(null=False)

    # @property
    # def serialize(self):
    #     data = {
    #         "id": self.id,
    #         "description": self.description,
    #     }


class Vehicles(BaseModel):
    class Meta:
        table_name = "vehicles"

    id = AutoField()
    plate = CharField(null=False)
    description = CharField()

    # @property
    # def serialize(self):
    #     data = {
    #         "id": self.id,
    #         "plate": self.plate,
    #         "description": self.description,
    #     }


class Reports(BaseModel):
    class Meta:
        table_name = "reports"

    id = AutoField(null=False)
    driver = ForeignKeyField(Drivers, column_name="driver")
    vehicle = ForeignKeyField(Vehicles, column_name="vehicle")
    lat = FloatField()
    lon = FloatField()
    alt = FloatField()
    speed = FloatField()
    event = ForeignKeyField(Events, column_name="event")
    time = DateTimeTZField()

    # @property
    # def serialize(self):
    #     data = {
    #         "id": self.id,
    #         "driver": self.driver,
    #         "vehicle": self.vehicle,
    #         "lat": self.lat,
    #         "lon": self.lon,
    #         "alt": self.alt,
    #         "speed": self.speed,
    #         "event": self.event,
    #         "time": self.time,
    #     }
