from django.test import TestCase
from req_handler.models import *
import json

# Create your tests here.


class RequestTestCase(TestCase):
    def setUp(self):
        #Request.objects.create(json_data='{ "plane": "AE01", "passenger_count": 45 }')
        pass
    
    def test_plane_set_correctly(self):
        dict = {"plane" : "AE01", "passenger_count" : 45}
        dict = json.dumps(dict)
        req = Request(dict)
        self.assertEqual("AE01", req.plane)
        self.assertEqual(45, req.passenger_count)
        
    def test_json_parsed_and_set_correctly(self):
        dict = { "plane" : "AE01", "gate" : "G01", "runway" : "R01", "arrive_at_time" : "2019-10-29 08:00"}
        dict = json.dumps(dict)
        req = Request(dict)
        
        self.assertEqual("AE01", req.plane)
        self.assertEqual("R01", req.runway)
