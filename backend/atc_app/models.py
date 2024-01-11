from django.db import models
import math
from datetime import datetime
from fractions import *
from atc_app import flightPaths
import csv

class Airport(models.Model):
    name = models.CharField(
        max_length=3,
        primary_key=True,
        unique=True,
        null=False
        )     # Approved airport names to pull from?
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    #y.default=0
    #x.default=0

class Airline(models.Model):
    airlineID = models.CharField(
        max_length=5, 
        primary_key=True,
        unique=True, 
        null=False,
        )

class Gate(models.Model):
    GATE_SIZES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large")
    ]

    gateID = models.CharField(
        max_length=10, 
        primary_key=True,
        unique=True,
        null=False,
        )
    size = models.CharField(max_length=1, choices=GATE_SIZES)

    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, null=True)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True)

class Runway(models.Model):
    RUNWAY_SIZES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large")
    ]

    runwayID = models.CharField(
        max_length=10,
        primary_key=True,
        unique=True, 
        null=False,
    )
    # TODO: change null to False when id allocating system is in place ^^
    size = models.CharField(max_length=1, choices=RUNWAY_SIZES)

    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True)

class Plane(models.Model):
    PLANE_SIZES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large")
    ]
    STATUS_CHOICES = [
        ("AG", "At Gate"),
        ("OR", "On Runway"),
        ("IF", "In Flight")
    ]

    planeID = models.CharField(
        max_length=10, 
        primary_key=True,
        unique=True, 
        null=False,)
    size = models.CharField(max_length=1, choices=PLANE_SIZES)
    capacity = models.IntegerField()
    pass_count = models.IntegerField(default=0)
    heading = models.FloatField(3, null=True)
    speed = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="AG")
    arrival_time = models.DateTimeField(null=True) # Arrival time at gate
    landing_time = models.DateTimeField(null=True)
    takeOff_time = models.DateTimeField(null=True)

    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, null=True)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='plane_origin', null=True) 
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='plane_dest', null=True) 
    runway = models.ForeignKey(Runway, on_delete=models.CASCADE, null=True)
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, null=True)


# STARTING DATA ***************************************************************************************************
ready = True
if ready:   # when changing model
    
    # Starting Airports *******************************************
    with open('startingData/airport.csv', 'r') as f:
        start_airport_data = list(csv.reader(f))
        start_airport_data.pop(0)
    f.close()

    airportNames = [airport.name for airport in list(Airport.objects.all())]
    for s in start_airport_data:
        if s[0] not in airportNames:
            Airport.objects.create(name=s[0], x=s[1], y=s[2])

    flightPaths.base(Airport.objects.all())
    # *************************************************************

    # Starting Airlines *******************************************
    with open('startingData/airline.csv', 'r') as f:
        start_airline_data = list(csv.reader(f))
        start_airline_data.pop(0)
    f.close()
    airlineNames = [airline.airlineID for airline in list(Airline.objects.all())]
    for s in start_airline_data:
        if s[0] not in airlineNames:
            Airline.objects.create(airlineID=s[0])
    # *************************************************************

    # Starting Airport_Airline ************************************
    start_airport_airline_data = {}
    with open('startingData/airport_airline.csv', 'r') as f:
        file = list(csv.reader(f))
        for i in range(1, len(file)):
            start_airport_airline_data[file[i][0]] = file[i][1]
    f.close()
    # *************************************************************

    # Starting Gates **********************************************
    with open('startingData/gate.csv', 'r') as f:
        start_gate_data = list(csv.reader(f))
        start_gate_data.pop(0)
    f.close()

    gateIDs = [gate.gateID for gate in list(Gate.objects.all())]
    for s in start_gate_data:
        if s[0] not in gateIDs:
            airlineInstance = Airline.objects.get(airlineID=start_airport_airline_data[s[0]])
            airportInstance = Airport.objects.get(name=s[1])
            Gate.objects.create(gateID=s[0], size=s[2][0], airline=airlineInstance, airport=airportInstance)
    # *************************************************************

    # Starting Runways ********************************************
    with open('startingData/runway.csv', 'r') as f:
        start_runway_data = list(csv.reader(f))
        start_runway_data.pop(0)
    f.close()

    runwayIDs = [runway.runwayID for runway in list(Runway.objects.all())]
    for s in start_runway_data:
        if s[0] not in runwayIDs:
            airportInstance = Airport.objects.get(name=s[1])
            Runway.objects.create(runwayID=s[0], size=s[2][0], airport=airportInstance)
    # *************************************************************

    # Starting Planes  ********************************************
    with open('startingData/plane.csv', 'r') as f:
        start_plane_data = list(csv.reader(f))
        start_plane_data.pop(0)
    f.close()

    planeIDs = [plane.planeID for plane in list(Plane.objects.all())]
    for s in start_plane_data:
        if s[0] not in planeIDs:
            airlineInstance = Airline.objects.get(airlineID=s[1])
            exampleAP = (Airport.objects.all())
            Plane.objects.create(planeID=s[0], size=s[2][0], airline=airlineInstance, capacity=s[3], origin=exampleAP[0], destination=exampleAP[1])
    # *************************************************************
