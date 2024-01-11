import math
from fractions import *
from datetime import datetime
from django.test import TestCase
from atc_app.models import Airport, Airline, Gate, Runway, Plane
from atc_app.flightPaths import Line, Path
from atc_app import collision, flightPaths
from atc_app.collision import collisionPlane

# models.py TESTING *******************************************************

class Test_Airport(TestCase):

    def setUp(self):
        Airport.objects.create(name="GSP", x=10, y=11)
        Airport.objects.create(name="Ohare", x=13, y=73)
    
    def test_location_set_correctly(self):
        airport = Airport.objects.get(name="GSP")
        self.assertEqual(airport.x, 10)
        self.assertEqual(airport.y, 11)

        airport = Airport.objects.get(name="Ohare")
        self.assertEqual(airport.x, 13)
        self.assertEqual(airport.y, 73)

    def test_name_set_correctly(self):
        airport = Airport.objects.get(x=10, y=11)
        self.assertEqual(airport.name, 'GSP')

        airport = Airport.objects.get(x=13, y=73)
        self.assertEqual(airport.name, 'Ohare')

class Test_Airline(TestCase):
    
    def setUp(self):
        Airline.objects.create(
            airlineID = 'A01',
            name = 'American'
        )
        Airline.objects.create(
            airlineID = 'U01',
            name = 'United'
        )

    def test_airline_id(self):
        airline = Airline.objects.get(name='American')
        airline2 = Airline.objects.get(name='United')
        
        self.assertEquals(airline.airlineID, 'A01')
        self.assertEquals(airline2.airlineID, 'U01')

    def test_airline_name(self):
        airline = Airline.objects.get(airlineID='A01')
        airline2 = Airline.objects.get(airlineID='U01')
        
        self.assertEquals(airline.name, 'American')
        self.assertEquals(airline2.name, 'United')

class Test_Gate(TestCase):

    def setUp(self):
        airlineFK = Airline.objects.create(
            airlineID = 'A01',
            name = 'American'
        )

        airportFK = Airport.objects.create(
            name="GSP", 
            x=10,
            y=18
            )

        Gate.objects.create(
            gateID = 'G01',
            size = "S",
            airline = airlineFK,
            airport = airportFK
        )

    def test_gate_attributes(self):
        gate = Gate.objects.get(gateID = 'G01')

        self.assertEquals(gate.gateID, 'G01')
        self.assertEquals(gate.size, "S")

class Test_Runway(TestCase):

    def setUp(self):
        airportFK = Airport.objects.create(
            name="GSP", 
            x=10,
            y=18
        )

        Runway.objects.create(
            runwayID = 'R01',
            size = 'S',
            airport = airportFK
        )

    def test_runway_attributes(self):
        runway = Runway.objects.get(runwayID = 'R01')

        self.assertEquals(runway.runwayID, 'R01')
        self.assertEquals(runway.size, 'S')

class Test_Plane(TestCase):

    def setUp(self):
        airlineFK = Airline.objects.create(
            airlineID = 'A01',
            name = 'American'
        )

        originFK = Airport.objects.create(
            name = "GSP", 
            x=10,
            y=18
        )

        destinationFK = Airport.objects.create(
            name = 'Ohare',
            x=20,
            y=28
        )
        
        runwayFK = Runway.objects.create(
            runwayID = 'R01',
            size = 'S',
            airport = originFK
        )

        Plane.objects.create(
            planeID = 'AB01',
            size = 'S',
            capacity = 150,
            heading = 36.5,
            speed = 0,
            status = 'AG',
            arrival_time = "2023-09-28 12:00+00:00",
            landing_time = "2023-09-28 11:45+00:00",
            takeOff_time = "2023-09-28 09:30+00:00",
            airline = airlineFK,
            origin = originFK,
            destination = destinationFK,
            runway = runwayFK
        )

    def test_plane_attributes(self):
        plane = Plane.objects.get(planeID = 'AB01')

        self.assertEquals(plane.size, 'S')
        self.assertEquals(plane.capacity, 150)
        self.assertEquals(plane.heading, 36.5)
        self.assertEquals(plane.speed, 0)
        self.assertEquals(plane.status, 'AG')
        self.assertEquals(str(plane.arrival_time), '2023-09-28 12:00:00+00:00') # The extra '+00:00' is for timezone change
        self.assertEquals(str(plane.landing_time), '2023-09-28 11:45:00+00:00')
        self.assertEquals(str(plane.takeOff_time), '2023-09-28 09:30:00+00:00')

# flightPaths.py TESTING **************************************************

class Test_Line(TestCase):
    def test_line_pos_slope(self):
        x1 = 362
        y1 = 294

        x2 = 582
        y2 = 626

        line = Line(x1, y1, x2, y2)
        
        self.assertEquals(line.m, Fraction(83, 55))
        self.assertEquals(line.b, Fraction(-13876, 55))
        self.assertEquals(line.isVertical, False)

    def test_line_neg_slope(self):
        x1 = 423
        y1 = 653

        x2 = 743
        y2 = 531
        
        line = Line(x1, y1, x2, y2)

        self.assertEquals(line.m, Fraction(-61, 160))
        self.assertEquals(line.b, Fraction(130283, 160))
        self.assertEquals(line.isVertical, False)

    def test_line_hor_slope(self):
        x1 = 269
        y1 = 482

        x2 = 842
        y2 = 482

        line = Line(x1, y1, x2, y2)

        self.assertEquals(line.m, 0)
        self.assertEquals(line.b, Fraction(482, 1))
        self.assertEquals(line.isVertical, False)

    def test_line_vert_slope(self):
        x1 = 269
        y1 = 823

        x2 = 269
        y2 = 723

        line = Line(x1, y1, x2, y2)

        self.assertEquals(line.m, 0)
        self.assertEquals(line.b, Fraction(823, 1))
        self.assertEquals(line.isVertical, True)

class Test_Path(TestCase):
    def test_path(self):
        x1 = 423
        y1 = 653

        x2 = 743
        y2 = 531
        
        line = Line(x1, y1, x2, y2)
        path = Path('abc', 'def', x1, y1, x2, y2, line)

        self.assertEquals(line.m, Fraction(-61, 160))
        self.assertEquals(line.b, Fraction(130283, 160))
        self.assertEquals(line.isVertical, False)

        self.assertEquals(path.name, ('abc', 'def'))
        self.assertEquals(path.x0, x1)
        self.assertEquals(path.y0, y1)
        self.assertEquals(path.x1, x2)
        self.assertEquals(path.y1, y2)
        self.assertEquals(path.line, line)

class Test_FindIfIntersection(TestCase):
    def test_intersection(self):

        x1 = 273
        y1 = 502

        x2 = 426
        y2 = 320
        
        line = Line(x1, y1, x2, y2)
        pathA = Path('abc', 'def', x1, y1, x2, y2, line)

        x1 = 284
        y1 = 350

        x2 = 582
        y2 = 476

        line = Line(x1, y1, x2, y2)
        pathB = Path('ghi', 'jkl', x1, y1, x2, y2, line)

        a = flightPaths.findIfIntersection(pathA, pathB)

        self.assertEquals(a, True)

    def test_out_of_range_intersection(self):
        x1 = 273
        y1 = 502

        x2 = 426
        y2 = 320
        
        line = Line(x1, y1, x2, y2)
        pathA = Path('abc', 'def', x1, y1, x2, y2, line)

        x1 = 284
        y1 = 350

        x2 = 582
        y2 = 210

        line = Line(x1, y1, x2, y2)
        pathB = Path('ghi', 'jkl', x1, y1, x2, y2, line)

        a = flightPaths.findIfIntersection(pathA, pathB)

        self.assertEquals(a, False)

    def test_parallel_no_intersection(self):
        x1 = 273
        y1 = 502

        x2 = 426
        y2 = 320
        
        line = Line(x1, y1, x2, y2)
        pathA = Path('abc', 'def', x1, y1, x2, y2, line)

        x1 = 284
        y1 = 350

        x2 = 437
        y2 = 168

        line = Line(x1, y1, x2, y2)
        pathB = Path('ghi', 'jkl', x1, y1, x2, y2, line)

        a = flightPaths.findIfIntersection(pathA, pathB)

        self.assertEquals(a, False)

    def test_horizontal_intersection(self):
        x1 = 273
        y1 = 502

        x2 = 426
        y2 = 320
        
        line = Line(x1, y1, x2, y2)
        pathA = Path('abc', 'def', x1, y1, x2, y2, line)

        x1 = 284
        y1 = 350

        x2 = 499
        y2 = 350

        line = Line(x1, y1, x2, y2)
        pathB = Path('ghi', 'jkl', x1, y1, x2, y2, line)

        a = flightPaths.findIfIntersection(pathA, pathB)

        self.assertEquals(a, True)

    def test_vertical_intersection(self):
        x1 = 273
        y1 = 502

        x2 = 426
        y2 = 320
        
        line = Line(x1, y1, x2, y2)
        pathA = Path('abc', 'def', x1, y1, x2, y2, line)

        x1 = 284
        y1 = 350

        x2 = 284
        y2 = 600

        line = Line(x1, y1, x2, y2)
        pathB = Path('ghi', 'jkl', x1, y1, x2, y2, line)

        a = flightPaths.findIfIntersection(pathA, pathB)

        self.assertEquals(a, True)

# collisionPlane.py TESTING ***********************************************

class Test_Collison(TestCase):
    def test_cpInit(self):
        cPlane = collisionPlane(293, 734, 843, 948, datetime(2023, 1, 15, 10, 0, 0), datetime(2023, 1, 15, 11, 0, 0))
        self.assertEquals(cPlane.x0, 293)
        self.assertEquals(cPlane.y0, 734)
        self.assertEquals(cPlane.x1, 843)
        self.assertEquals(cPlane.y1, 948)
        self.assertEquals(cPlane.t0, datetime(2023, 1, 15, 10, 0, 0))
        self.assertEquals(cPlane.t1, datetime(2023, 1, 15, 11, 0, 0))
        self.assertEquals(cPlane.deltaT.total_seconds(), 3600)
        self.assertEquals(cPlane.distance, math.sqrt(348296))

    def test_findIntersection(self):
        x1 = 273
        y1 = 502

        x2 = 426
        y2 = 320
        
        lineA = Line(x1, y1, x2, y2)

        x1 = 284
        y1 = 350

        x2 = 582
        y2 = 476

        lineB = Line(x1, y1, x2, y2)
        ix, iy = collision.findIntersection(lineA, lineB)
        self.assertEquals(round(ix), 370)
        self.assertEquals(round(iy), 386)

    def test_findCollisions_collision(self):
        ax0, ay0, ax1, ay1 = 293, 734, 843, 948
        bx0, by0, bx1, by1 = 132, 324, 843, 948
        planeA = collisionPlane(ax0, ay0, ax1, ay1, datetime(2023, 1, 15, 10, 0, 0), datetime(2023, 1, 15, 11, 0, 0))
        planeB = collisionPlane(bx0, by0, bx1, by1, datetime(2023, 1, 15, 10, 0, 0), datetime(2023, 1, 15, 11, 0, 0))
        lineA = Line(ax0, ay0, ax1, ay1)
        lineB = Line(bx0, by0, bx1, by1)
        result = collision.findCollision(planeA, planeB, lineA, lineB)
        self.assertEquals(result, True)

    def test_findCollisions_no_collision(self):
        ax0, ay0, ax1, ay1 = 100, 100, 10, 15
        bx0, by0, bx1, by1 = 132, 324, 843, 948
        planeA = collisionPlane(ax0, ay0, ax1, ay1, datetime(2023, 1, 15, 10, 0, 0), datetime(2023, 1, 15, 11, 0, 0))
        planeB = collisionPlane(bx0, by0, bx1, by1, datetime(2023, 1, 15, 10, 0, 0), datetime(2023, 1, 15, 11, 0, 0))
        lineA = Line(ax0, ay0, ax1, ay1)
        lineB = Line(bx0, by0, bx1, by1)
        result = collision.findCollision(planeA, planeB, lineA, lineB)
        self.assertEquals(result, False)

    def test_cp_calcDistI(self):
        ax0, ay0, ax1, ay1 = 293, 734, 843, 948
        bx0, by0, bx1, by1 = 132, 324, 843, 948
        planeA = collisionPlane(ax0, ay0, ax1, ay1, datetime(2023, 1, 15, 10, 0, 0), datetime(2023, 1, 15, 11, 0, 0))
        planeB = collisionPlane(bx0, by0, bx1, by1, datetime(2023, 1, 15, 10, 0, 0), datetime(2023, 1, 15, 11, 0, 0))
        lineA = Line(ax0, ay0, ax1, ay1)
        lineB = Line(bx0, by0, bx1, by1)

        ix, iy = collision.findIntersection(lineA, lineB)
        planeA.calcDistI(ix, iy)
        planeB.calcDistI(ix, iy)

        print("Distance A", planeA.distance)
        print("Distance B", planeB.distance)

        testIX = float((lineB.b - lineA.b) / (lineA.m - lineB.m))
        testIY = float((lineA.m * ((lineB.b - lineA.b) / (lineA.m - lineB.m))) + lineA.b)

        testDistA = math.sqrt(((testIX - planeA.x0) ** 2) + ((testIY - planeA.y0)**2))
        testDistB = math.sqrt(((testIX - planeB.x0) ** 2) + ((testIY - planeB.y0)**2))

        self.assertEquals(planeA.distance, testDistA)
        self.assertEquals(planeB.distance, testDistB)

