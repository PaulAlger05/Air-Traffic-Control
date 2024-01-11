from fractions import *

class Line():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1        # Saved just in case line is vertical (Look at vertIntersection())
        self.isVertical = False
        try:
            self.m = Fraction((y2 - y1), (x2 - x1))
        except ZeroDivisionError:           # Checking for vertical line (undefined)
            self.isVertical = True
            self.m = 0                      # if vertical, self.m should be ignored
        self.b = (self.m * Fraction(-x1, 1)) + Fraction(y1, 1)

class Path():
    def __init__(self, name0, name1, x0, y0, x1, y1, line:Line):
        self.name = (name0, name1)
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.line = line

# Finds if the intersection point lies on both line segments
def inRange(path:Path, ix, iy) -> bool:
    def isBetween(a1, a2, a3) -> bool:
        lowA = min(a1, a2)
        highA = max(a1, a2)
        return lowA <= a3 and highA >= a3
    return isBetween(path.x0, path.x1, ix) and isBetween(path.y0, path.y1, iy)



# Finds if the two paths interesect
def findIfIntersection(pathA:Path, pathB:Path) -> bool:
    a = pathA.line
    b = pathB.line
    if a.m == b.m or (a.isVertical and b.isVertical):
        print("Slopes are Equal")
        return False    # No Collision Detected. (Slopes Are Equal)

    def vertIntersection(v, b):
        try:
            ix = v.x1       # doesn't matter if it is v.x1 or v.x0 -- it's the same x value
        except ZeroDivisionError:
            print("ix Error", b.b, a.b, a.m, b.m)
            ix = ""
        
        try:
            iy = float((b.m * Fraction(v.x1, 1)) + b.b)     # iy should just be b(x) ** (f(x) = mx + b)
        except ZeroDivisionError:
            print("iy Error", a.m, b.b, a.b, a.m, b.m, a.b)
            iy = ""
        return [ix, iy]


    if a.isVertical:
        ix, iy = vertIntersection(a, b)
    elif b.isVertical:
        ix, iy = vertIntersection(b, a)
    else:
        try:
            ix = float((b.b - a.b) / (a.m - b.m))
        except ZeroDivisionError:
            print("ix Error", b.b, a.b, a.m, b.m)
            return False
        try:
            iy = float((a.m * ((b.b - a.b) / (a.m - b.m))) + a.b)
        except ZeroDivisionError:
            print("iy Error", a.m, b.b, a.b, a.m, b.m, a.b)
            return False
    if ix == "" or iy == "":
            return False
    
    
    # return True if inRange(pathA, ix, iy) and inRange(pathB, ix, iy) else False
    if inRange(pathA, ix, iy) and inRange(pathB, ix, iy):                                 # Testing
        print(f"Path {pathA.name} <-> {pathB.name} intersect at ({ix}, {iy}).")
        return True
    else:
        print(ix, iy)
        print('No Intersection: Intersection out of line range')
        return False
    

    

intersections = {}


def base(apObjs):
    # apLocs = []
    airports = list(apObjs) # model.py passes in Airport.objects.all()

    processedAirports = [] * len(airports)  # container for the processed airports
    paths = []
    for i in range(0, len(airports)):
        loc0 = airports.pop(0)
        for loc1 in airports:
            line = Line(loc0.x, loc0.y, loc1.x, loc1.y) # Makes a line out of the two airports locations
            paths.append(Path(loc0.name, loc1.name, loc0.x, loc0.y, loc1.x, loc1.y, line))  # (More detailed object that contains line) -> into list of paths
        processedAirports.append(loc0)  # all paths from loc0 have been calc-ed, so put it in processed list



    for i in range(0, len(paths)):
        intersections[paths[i].name] = [paths[i].name]      # intersection will by default contain itself
        for j in range(0, len(paths)):
            if findIfIntersection(paths[i], paths[j]):  # finding if the two paths intersect
                intersections[paths[i].name].append(paths[j].name)      # add the path to the list of its intersections

    for k,v in intersections.items():     # Testing
        print(k, v)