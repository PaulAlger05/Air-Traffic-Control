from rest_framework import serializers
from .models import *

class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        db_table = 'atc_app_airport'
        model = Airport 
        fields = ['name', 'x','y']
class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = 'atc_app_airline'
        model = Airline
        fields = ('airlineID','name')
class GateSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = 'atc_app_gate'
        model = Gate
        fields = ('size', 'gateID')


class RunwaySerializer(serializers.ModelSerializer):
    class Meta:
        db_table = 'atc_app_runway'
        model = Runway
        fields = ('runwayID', 'size')


class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = 'atc_app_plane'
        model = Plane
        fields = ('planeID', 'size', 'capacity', 'heading', 'speed', 'status', 'arrival_time', 'landing_time', 'takeOff_time')
  