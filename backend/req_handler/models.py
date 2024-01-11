from django.db import models
import datetime
import json

from atc_app import collision
from atc_app.models import *

# Create your models here.

# Main request class
class Request():
    req_type = ""
    
    plane = ""
    
    # Take off request variables
    direction = -1
    speed = -1
    origin = ""
    destination = ""
    landing_time = ""
    take_off_time = ""

    # Gate/runway request variables
    gate = ""
    runway = ""
    arrive_at_time = ""
    
    # Passenger count request variables
    passenger_count = -1


    def __init__(self, json_object, req_type):
        self.req_type = req_type
        self.parse_json_data(json_object) # Initialize instance variables with the Json data 
    
    
    def parse_json_data(self, json_object):
        # Receive JSON object and parse it
        # Plug values into request
        req = json.loads(json_object)
        
        self.plane = req['plane']

        if self.req_type == 'takeoff':
            # Take off request
            self.direction = int(req['direction'])
            self.speed = int(req['speed'])
            self.origin = req['origin']
            self.destination = req['destination']
            self.landing_time = req['landing_time']
            self.take_off_time = req['take_off_time']
        elif self.req_type == 'gate':
            # Gate/runway request
            self.gate = req['gate']
            self.runway = req['runway']
            self.arrive_at_time = req['arrive_at_time']
        elif self.req_type == 'pass_count':
            # Passenger count request
            self.passenger_count = int(req['passenger_count'])
        else:
            # TODO: if other request???
            raise Exception("Bad Request")      
        
    
    # check for gate conflicts 
    # return true if conflict exists
    def duplicate_gate(self) -> bool:        
        new_plane = Plane.objects.get(planeID = self.plane)
        new_gate = Gate.objects.get(gateID = self.gate)
        
        for plane in list(Plane.objects.all()):
            if plane.destination.name == new_gate.airport.name and plane.gate.gateID == self.gate:
                if plane.arrival_time == datetime.strptime(self.arrive_at_time, "%Y-%m-%d %H:%M:%S").date(): # TODO: within 60 seconds of each other??
                    return True # Gate conflict does exists
        return False
    
    # check for gate size
    def gate_is_too_small(self) -> bool:
        sizeWeight = {'S':0, 'M':1, 'L':2}
        new_plane = Plane.objects.get(planeID = self.plane)
        new_gate = Gate.objects.get(gateID = self.gate)

        if sizeWeight[new_plane.size] > sizeWeight[new_gate.size]:
            return True # plane is too big
        return False
    
    
    # check for runway conflicts
    # return true if conflict exists
    def duplicate_runway(self) -> bool:
        new_plane = Plane.objects.get(planeID = self.plane)
        new_runway = Runway.objects.get(runwayID = self.runway)
        for plane in list(Plane.objects.all()):
            if plane.destination.name == new_runway.airport.name and plane.runway.runwayID == self.runway:
                if plane.landing_time == new_plane.landing_time:
                    return True # conflict on runway
        return False
                
    # check for runway size
    def runway_is_too_small(self) -> bool:
        sizeWeight = {'S':0, 'M':1, 'L':2}
        new_plane = Plane.objects.get(planeID = self.plane)
        new_runway = Runway.objects.get(runwayID = self.runway)

        if sizeWeight[new_plane.size] > sizeWeight[new_runway.size]:
            return True # plane is too big
        return False       
        
        
    # insert new gate/runway data
    def insert_new_gate_data(self):
        plane = Plane.objects.get(planeID = self.plane)
        plane.gate = Gate.objects.get(gateID = self.gate)
        plane.runway = Runway.objects.get(runwayID = self.runway)
        plane.arrival_time = datetime.strptime(self.arrive_at_time, "%Y-%m-%d %H:%M:%S").date()  
    
    
    # check for passenger conflicts
    # return true if conflict exists
    def too_many_passengers(self) -> bool:
        for plane in list(Plane.objects.all()):
            if plane.capacity < self.passenger_count: # too many new passengers
                return True
        return False
    
    def insert_new_passenger_data(self):
        plane = Plane.objects.get(planeID = self.plane)
        plane.pass_count = self.passenger_count
    
    
    
    # check for plane conflicts
    # return true if conflict exists
    def collision_imminent(self) -> bool:
        # Check db for conflicts using instance variables
        originAP = Airport.objects.get(name=self.origin)
        originX, originY = (originAP.x, originAP.y)     # Check database for the x and y value of this airport
        destAP = Airport.objects.get(name=self.destination)
        destX, destY = (destAP.x, destAP.y)          # Check database for the x and y value of this airport
        return collision.noCollisions(self.origin, self.destination, originX, originY, destX, destY, self.take_off_time, self.landing_time)
    
    # insert new plane data
    def insert_new_plane_data(self):
        # insert data into db model based on instance variables
        plane = Plane.objects.get(planeID = self.plane)
        plane.heading = float(self.direction)
        plane.speed = int(self.speed)
        plane.origin = Airport.objects.get(name=self.origin)
        plane.destination = Airport.objects.get(name=self.destination)
        plane.landing_time = datetime.strptime(self.landing_time, "%Y-%m-%d %H:%M:%S").date()
        plane.takeOff_time = datetime.strptime(self.take_off_time, "%Y-%m-%d %H:%M:%S").date()



