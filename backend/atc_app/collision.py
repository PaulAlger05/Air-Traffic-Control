import math
from datetime import datetime
from fractions import *
from atc_app import flightPaths
from .models import *

class collisionPlane():
    def __init__(self, x0: int, y0: int, x1: int, y1: int, t0: datetime, t1: datetime):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.t0 = t0
        self.t1 = t1
        self.deltaT = t1 - t0
        self.distance = math.sqrt(((x1 - x0)**2) + ((y1 - y0)**2))
        self.distanceI = -1     # To be made later by CalcDistI

    def calcDistI(self, ix, iy):
        self.distanceI = math.sqrt(((ix - self.x0)**2) + ((iy - self.y0)**2))


def findIntersection(a:flightPaths.Line, b:flightPaths.Line) -> (float, float):
    ix = float((b.b - a.b) / (a.m - b.m))
    iy = float((a.m * ((b.b - a.b) / (a.m - b.m))) + a.b)
    return (ix, iy)

def inRange(planePath:collisionPlane, ix, iy) -> bool:
    def isBetween(a1, a2, a3) -> bool:
        lowA = min(a1, a2)
        highA = max(a1, a2)
        return lowA <= a3 and highA >= a3
    return isBetween(planePath.x0, planePath.x1, ix) and isBetween(planePath.y0, planePath.y1, iy)


# def findCollision(ax1, ay1, ax2, ay2, atime0, atime1, bx1, by1, bx2, by2, btime0, btime1) -> bool:
def findCollision(planeA, planeB, LineA, LineB) -> bool:

    # planeA = collisionPlane(ax1, ay1, ax2, ay2, atime0, atime1)
    # planeB = collisionPlane(bx1, by1, bx2, by2, btime0, btime1)
    # lineA = Line(ax1, ay1, ax2, ay2)
    # lineB = Line(bx1, by1, bx2, by2)

    # Checking for Parallel Lines
    # if lineA.m == lineB.m and lineA.isVertical == lineB.isVertical:
    if LineA.m == LineB.m and (LineA.isVertical and LineB.isVertical):
        return False # No Collision Detected. (Slopes Are Equal)
    else:
        # ix, iy = findIntersection(lineA, lineB)
        ix, iy = findIntersection(LineA, LineB)

        # Make Distance-To-Intersection in each plane
        planeA.calcDistI(ix, iy)
        planeB.calcDistI(ix, iy)

        # Check if intersection lies within both line segments
        if not (inRange(planeA, ix, iy) and inRange(planeB, ix, iy)):
            print("Intersection Out of Range")
            return False # No Collision Detected. (Intersection Out of Range)
        else:
            # # Testing
            # print(atime0, atime1, btime0, btime1)
            # print((atime1 - atime0).total_seconds(), (atime1 - atime0).total_seconds()/60)
            # print((btime1 - btime0).total_seconds(), (btime1 - btime0).total_seconds()/60)
            # print("A:", lineA.m, lineA.b)
            # print("B:", lineB.m, lineB.b)
            # print(ix, iy)

            # Time of A -> I
            a_to_i = (planeA.deltaT / planeA.distance * planeA.distanceI)

            # Time of B -> I
            b_to_i = (planeB.deltaT / planeB.distance * planeB.distanceI)

            # # Testing
            # print((atime0 + a_to_i).strftime("%Y-%m-%d %H:%M:%S"))
            # print((btime0 + b_to_i).strftime("%Y-%m-%d %H:%M:%S"))

            # intersectionTimeA = (atime0 + a_to_i).strftime("%Y-%m-%d %H:%M:%S")
            # intersectionTimeB = (btime0 + b_to_i).strftime("%Y-%m-%d %H:%M:%S")
            # intersectionTimeA = (planeA.t0 + a_to_i).strftime("%Y-%m-%d %H:%M:%S").total_seconds()
            # intersectionTimeB = (planeB.t0 + b_to_i).strftime("%Y-%m-%d %H:%M:%S").total_seconds()
            intersectionTimeA = (planeA.t0 + a_to_i)
            intersectionTimeB = (planeB.t0 + b_to_i)
            timeDiff = abs((intersectionTimeA - intersectionTimeB).total_seconds())

            print(f"intersectionTimeA: {intersectionTimeA}, intersectionTimeB: {intersectionTimeB}")
            if timeDiff <= 60:      # 60 second buffer
                return True # COLLISION DETECTED!
            else:
                print("Planes Intersect at Different Times")
                return False # No Collision Detected. (Planes Intersect at Different Times)
            



def noCollisions(origin, dest, x0, y0, x1, y1, take_off_time, landing_time):
    newPlane = collisionPlane(x0, y0, x1, y1, take_off_time, landing_time)
    newLine = flightPaths.Line(x0, y0, x1, y1)
    good = True
    [print(k, v) for k, v in flightPaths.intersections.items()]
    print(origin.name, dest.name)
    for fpath in flightPaths.intersections[(origin.name, dest.name)]:
        isCollision = False
        planes = Plane.objects.filter(origin=Airport.objects.get(name=fpath[0]), destination=Airport.objects.get(name=fpath[1]))      # TODO: this shouldn't work; needs to access name of airport
        for plane in planes:
            planeLP = collisionPlane(plane.origin.x, plane.origin.y, plane.destination.x, plane.destination.y, plane.takeOff_time, plane.landing_time)
            planeLine = flightPaths.Line(plane.origin.x, plane.origin.y, plane.destination.x, plane.destination.y)
            if findCollision(newPlane, planeLP, newLine, planeLine):
                return False    # If collision is found
    return True     # If no collision is found
