#!/usr/bin/env python3
import math
from PIL import Image, ImageDraw, ImagePath, ImageOps
import random


class ConvexPolygon(object):
    """Constructor of a ConvexPolygon. Generates a convex polygon with a set of points setOfPoints. Orders the set of points and generates the convex hull just to be sure the resulting polygon introduced is a convex one. By default, sets the color of
    the polygon to black"""
    def __init__(self, setOfPoints, color=(0, 0, 0)):
        self.setOfPoints = list(set(setOfPoints))
        self.__orderSetOfPoints()
        self.setOfPoints = self.getConvexHull(self.setOfPoints)
        self.color = color

    """Finds the slope of a segment"""
    def __findSlope(self, pointA, pointB):
        return (pointA[1] - pointB[1]) / (pointA[0] - pointB[0])

    """Finds the slope of a segment"""
    def __yintercept(self, slope, point):
        return point[1] - slope*point[0]

    """Check if a point is part of a segment pointA-pointB"""
    def __isInline(self, lonelyPoint, pointA, pointB):
        if ((pointA[1] <= lonelyPoint[1] and lonelyPoint[1] <= pointB[1]) or (pointB[1] <= lonelyPoint[1] and lonelyPoint[1] <= pointA[1])):
            if lonelyPoint[0] == pointA[0] and lonelyPoint[0] == pointB[0]:
                return True
        if ((pointA[0] <= lonelyPoint[0] and lonelyPoint[0] <= pointB[0]) or (pointB[0] <= lonelyPoint[0] and lonelyPoint[0] <= pointA[0])):
            if lonelyPoint[1] == pointA[1] and lonelyPoint[1] == pointB[1]:
                return True
        return False

    """Check if a point is at the left of a segment pointA-pointB"""
    def __isBeforeLine(self, lonelyPoint, pointA, pointB):
        if (pointA[0] == pointB[0]):
            if lonelyPoint[0] <= pointA[0]:
                return True
            else:
                return False
        if ((pointA[1] < lonelyPoint[1] and lonelyPoint[1] < pointB[1]) or (pointB[1] < lonelyPoint[1] and lonelyPoint[1] < pointA[1])):
            if (lonelyPoint[0] < pointA[0] and lonelyPoint[0] < pointB[0]) or (lonelyPoint[0] > pointA[0] and lonelyPoint[0] > pointB[0]):
                return True
            m = self.__findSlope(pointA, pointB)
            c = self.__yintercept(m, pointA)
            x = (lonelyPoint[1] - c) / m
            if (lonelyPoint[0] <= x):
                return True
        return False

    """Calculates the coordinates of the center of the implicit polygon. Notice that this function calculates, the center, not the centroid"""
    def __calculateCenter(self):
        points = self.setOfPoints
        length = len(points)
        xCoordList = [point[0] for point in points]
        yCoordList = [point[1] for point in points]
        sumOfX = sum(xCoordList)
        sumOfY = sum(yCoordList)
        return (sumOfX / length, sumOfY / length)

    """Calculates if the point a is at the left of point b, using the center of the polygon as reference."""
    def __less(self, a, b, center):
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        if (ax - center[0] >= 0) and (bx - center[0] < 0):
            return False
        if (ax - center[0] < 0) and (bx - center[0] >= 0):
            return True
        if (ax - center[0] == 0) and (bx - center[0] == 0):
            if (ay - center[1] >= 0) or (by - center[1] >= 0):
                return ay > by
            return by > ay
        det = (ax - center[0]) * (by - center[1]) - (bx - center[0]) * (ay - center[1])
        if det < 0:
            return True
        if det > 0:
            return False
        d1 = math.pow((ax - center[0]), 2) + math.pow((ay - center[1]), 2)
        d2 = math.pow((bx - center[0]), 2) + math.pow((by - center[1]), 2)
        return d1 > d2

    """This function orders a set of points of a polygon in a clockwise order and taking the leftest point as reference."""
    def __orderSetOfPoints(self):
        orderedPoints = []
        if len(self.setOfPoints) <= 1:
            return self.setOfPoints
        center = self.__calculateCenter()
        points = self.setOfPoints.copy()
        while points != []:
            a = points[0]
            for point in points:
                if (a != point) and not self.__less(a, point, center):
                    a = point
            orderedPoints.append(a)
            points.remove(a)
        self.setOfPoints = orderedPoints
        return orderedPoints

    """Calculates and return the distance between two points a and b"""
    def __calculateDistanceBetweenPoints(self, a, b):
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        return math.sqrt(math.pow(ax - bx, 2) + math.pow(ay - by, 2))

    """Calculates and return the lowest coordinate of the implicit polygon, in case of a tie, the leftest one."""
    def __lowestCoord(self, setOfPoints):
        minCoordPoint = setOfPoints[0]
        for point in setOfPoints:
            if point[1] < minCoordPoint[1]:
                minCoordPoint = point
            elif point[1] == minCoordPoint[1]:
                if point[0] < minCoordPoint[0]:
                    minCoordPoint = point
        return minCoordPoint

    """Calculates the angle between two points, returns the angle"""
    def __calculateAngleBetweenTwoPoints(self, pointA, pointB):
        x = pointB[0] - pointA[0]
        y = pointB[1] - pointA[1]
        angle = math.atan2(y, x)
        return angle

    """Partition function to implement the quicksort"""
    def __partition(self, setOfPoints, referencePoint, low, high):
        i = low-1
        pivot = setOfPoints[high]
        for j in range(low, high):
            angleCurrentPoint = self.__calculateAngleBetweenTwoPoints(referencePoint, setOfPoints[j])
            anglePivotPoint = self.__calculateAngleBetweenTwoPoints(referencePoint, pivot)
            if angleCurrentPoint >= anglePivotPoint:
                i += 1
                setOfPoints[i], setOfPoints[j] = setOfPoints[j], setOfPoints[i]
        setOfPoints[i+1], setOfPoints[high] = setOfPoints[high], setOfPoints[i+1]
        return i+1

    """Quicksort function a set of points, using the quicksort algorithm"""
    def __quicksort(self, setOfPoints, referencePoint, low, high):
        if len(setOfPoints) == 0:
            return setOfPoints
        if low < high:
            pivot = self.__partition(setOfPoints, referencePoint, low, high)
            self.__quicksort(setOfPoints, referencePoint, low, pivot-1)
            self.__quicksort(setOfPoints, referencePoint, pivot+1, high)

    """Orders a set of points introduced on the parameter by angle using a point as a reference"""
    def __sortByAngle(self, referencePoint, setOfPoints):
        self.__quicksort(setOfPoints, referencePoint, 0, len(setOfPoints)-1)

    """Check if an angle is counter clockwise calculating the area. If the area is negative, the are is clockwise (return false), otherwise is counter clockwise (return true)"""
    def __isAngleCounterClockWise(self, pointA, pointB, pointC):
        area = (pointB[0]-pointA[0])*(pointC[1]-pointA[1]) - (pointB[1]-pointA[1])*(pointC[0]-pointA[0])
        if area < 0:
            return False
        return True

    """Check if two polygons are equal, if both are the same (have the same points) returns true, otherwise return false."""
    def isEqual(self, polygon):
        setOfPointsA = self.getSetOfPoints()
        setOfPointsB = polygon.getSetOfPoints()
        if(len(setOfPointsA) != len(setOfPointsB)):
            return False
        for i in range(0, len(setOfPointsA)-1):
            if setOfPointsA[i] != setOfPointsB[i]:
                return False
        return True

    """Set a color to the implicit polygon. setColor is a tuple (r, g, b)"""
    def setColor(self, setColor):
        self.color = setColor

    """returns the color assigned to the implicit polygon"""
    def __getColor(self):
        return self.color

    """returns the set of points of the implicit polygon"""
    def getSetOfPoints(self):
        return self.setOfPoints

    """Check if the point is inside the area of the implicit polygon"""
    def __isPointInside(self, point):
        points = self.setOfPoints
        numberOfIntersections = 0
        length = len(points)
        for i in range(0, length-1):
            if point == points[i]:
                return True
            if self.__isInline(point, points[i], points[i+1]):
                return True
            if self.__isBeforeLine(point, points[i], points[i+1]):
                numberOfIntersections += 1
        if point == points[length-1]:
            return True
        if self.__isInline(point, points[length-1], points[0]):
            return True
        if self.__isBeforeLine(point, points[length-1], points[0]):
            numberOfIntersections += 1
        if numberOfIntersections % 2 != 0:
            return True
        return False

    """Check if the the implicit polygon is inside the polygon of the parameter"""
    def isInsidePolygon(self, polygon):
        for point in self.setOfPoints:
            if not polygon.__isPointInside(point):
                return False
        return True

    """Returns a tuple with the number of vertices and edges of the implicit polygon"""
    def getNumberOfVerticesAndEdges(self):
        numberOfVertices = len(self.setOfPoints)
        numberOfEdges = 0
        if numberOfVertices == 2:
            numberOfEdges = 1
        elif numberOfVertices > 2:
            numberOfEdges = numberOfVertices
        return([numberOfVertices, numberOfEdges])

    """Calculate and return the perimeter of the implicit polygon"""
    def getPerimeter(self):
        points = self.setOfPoints
        length = len(points)
        if length < 2:
            return 0
        elif length == 2:
            return self.__calculateDistanceBetweenPoints(points[0], points[1])
        perimeter = self.__calculateDistanceBetweenPoints(points[length-1], points[0])
        for i in range(0, length-1):
            perimeter += self.__calculateDistanceBetweenPoints(points[i], points[i+1])
        return perimeter

    """Calculate and return the area of the implicit polygon"""
    def getArea(self):
        points = self.setOfPoints
        length = len(points)
        if(length <= 2):
            return 0
        xCoordList = [point[0] for point in points]
        yCoordList = [point[1] for point in points]
        sumOfX = xCoordList[length-1]*yCoordList[0]
        sumOfY = xCoordList[0]*yCoordList[length-1]
        for i in range(length-1):
            sumOfX += xCoordList[i]*yCoordList[i+1]
            sumOfY += xCoordList[i+1]*yCoordList[i] 
        return abs(sumOfX - sumOfY) * (1/2)

    """Calculate and return the coordinates of the centroid of the implicit polygon"""
    def getCentroid(self):
        points = self.setOfPoints
        length = len(points)
        if length == 0:
            return (0, 0)
        elif length == 1:
            return (points[0][0], points[0][1])
        xCoordList = [point[0] for point in points]
        yCoordList = [point[1] for point in points]
        sumX = 0
        sumY = 0
        sumDivList = []
        for i in range(0, length-1):
            sumDivList.append((xCoordList[i]*yCoordList[i+1] - xCoordList[i+1]*yCoordList[i]))
        sumDivList.append((xCoordList[length-1]*yCoordList[0] - xCoordList[0]*yCoordList[length-1]))
        for i in range(0, length-1):
            sumX += (xCoordList[i] + xCoordList[i+1])*sumDivList[i]
            sumY += (yCoordList[i] + yCoordList[i+1])*sumDivList[i]
        sumX += (xCoordList[length-1] + xCoordList[0])*sumDivList[length-1]
        sumY += (yCoordList[length-1] + yCoordList[0])*sumDivList[length-1]
        sumDiv = sum(sumDivList)
        xCoord = (sumX / sumDiv) * (1 / 3)
        yCoord = (sumY / sumDiv) * (1 / 3)
        return (xCoord, yCoord)

    """Check if the implicit polygon is a regular polygon (return true) or not (return false)"""
    def isARegularPolygon(self):
        points = self.setOfPoints
        length = len(points)
        if(length <= 2):
            return False
        distance = self.__calculateDistanceBetweenPoints(points[length-1], points[0])
        for i in range(0, length-1):
            if distance != self.__calculateDistanceBetweenPoints(points[i], points[i+1]):
                return False
        return True

    """Get the points of the resulting convex hull of the set of points introduced in the parameter setOfPoints"""
    def getConvexHull(self, setOfPoints):
        if len(setOfPoints) <= 3:
            return setOfPoints
        hullPoints = []
        startPoint = self.__lowestCoord(setOfPoints)
        hullPoints.append(startPoint)
        setOfPoints.remove(startPoint)
        self.__sortByAngle(startPoint, setOfPoints)
        hullPoints.append(setOfPoints[0])
        for i in range(1, len(setOfPoints)):
            nextPoint = setOfPoints[i]
            p = hullPoints[-1]
            hullPoints.pop(-1)
            while hullPoints != [] and self.__isAngleCounterClockWise(hullPoints[-1], p, nextPoint):
                p = hullPoints[-1]
                hullPoints.pop(-1)
            hullPoints.append(p)
            hullPoints.append(nextPoint)
        if not self.__isAngleCounterClockWise(hullPoints[-1], p, startPoint):
            p = hullPoints[-1]
            hullPoints.pop(-1)
        return hullPoints

    def pointInside(self, point):
        return self.__isPointInside(point)

    """Return all the points of the implicit polygon that are inside the polygon introduced in the parameter polygon"""
    def __getInnerPointsPolygon(self, polygon):
        points = self.setOfPoints
        innerPoints = []
        for point in points:
            if polygon.__isPointInside(point):
                innerPoints.append(point)
        return innerPoints

    """Calculates the point of intersection of two segments, if there's no intersection, returns None"""
    def __calculateIntersectionPoint(self, pointA, pointB, pointC, pointD):
        d = (pointD[1] - pointC[1]) * (pointB[0] - pointA[0]) - (pointD[0] - pointC[0]) * (pointB[1] - pointA[1])
        if d != 0:
            uA = ((pointD[0] - pointC[0]) * (pointA[1] - pointC[1]) - (pointD[1] - pointC[1]) * (pointA[0] - pointC[0])) / d
            uB = ((pointB[0] - pointA[0]) * (pointA[1] - pointC[1]) - (pointB[1] - pointA[1]) * (pointA[0] - pointC[0])) / d
        else:
            return
        if not(0 <= uA <= 1 and 0 <= uB <= 1):
            return
        return (pointA[0] + uA * (pointB[0] - pointA[0]), pointA[1] + uA * (pointB[1] - pointA[1]))

    """Returns the convex polygon resulting of the intersection bertween two polygons, the one implicit and the second one introduced by parameter"""
    def intersection(self, polygon):
        setOfPointsA = self.setOfPoints
        setOfPointsB = polygon.setOfPoints
        intersectionPolygon = []
        for i in range(0, len(setOfPointsA)-1):
            for j in range(0, len(setOfPointsB)-1):
                intersectPoint = self.__calculateIntersectionPoint(setOfPointsA[i], setOfPointsA[i+1], setOfPointsB[j], setOfPointsB[j+1])
                if intersectPoint is not None:
                    intersectionPolygon.append(intersectPoint)
        if len(setOfPointsB) >= 2:
            for i in range(0, len(setOfPointsA)-1):
                    intersectPoint = self.__calculateIntersectionPoint(setOfPointsA[i], setOfPointsA[i+1], setOfPointsB[len(setOfPointsB)-1], setOfPointsB[0])
                    if intersectPoint is not None:
                        intersectionPolygon.append(intersectPoint)            
        for i in range(0, len(setOfPointsB)-1):
            for j in range(0, len(setOfPointsA)-1):
                intersectPoint = self.__calculateIntersectionPoint(setOfPointsA[i], setOfPointsA[i+1], setOfPointsB[j], setOfPointsB[j+1])
                if intersectPoint is not None:
                    intersectionPolygon.append(intersectPoint)
        if len(setOfPointsA) >= 2:
            for i in range(0, len(setOfPointsB)-1):
                    intersectPoint = self.__calculateIntersectionPoint(setOfPointsA[len(setOfPointsA)-1], setOfPointsA[0], setOfPointsB[i], setOfPointsB[i+1])
                    if intersectPoint is not None:
                        intersectionPolygon.append(intersectPoint)            
        intersectionPolygon = intersectionPolygon + self.__getInnerPointsPolygon(polygon) + polygon.__getInnerPointsPolygon(self)
        return ConvexPolygon(intersectionPolygon)
        
    """Returns the convex polygon resulting of the union bertween two polygons, the one implicit and the second one introduced by parameter"""
    def union(self, polygon):
        points = self.getSetOfPoints() + polygon.getSetOfPoints()
        return ConvexPolygon(self.getConvexHull(points))

    """Function that translates the implicit polygon to the coordinates (0, 0) in order to later on, scale it"""
    def translate(self, minX, minY):
        translatedSetOfPoints = []
        for point in self.setOfPoints:
            translatedSetOfPoints.append((point[0]+minX, point[1]+minY))
        return translatedSetOfPoints

    """Function that scales the implicit polygon to a resolution 400x400"""
    def scale(self, maxX, maxY):
        scaledSetOfPoints = []
        ratioX = 1
        ratioY = 1
        if maxX != 0:
            ratioX = 398/maxX
        if maxY != 0:
            ratioY = 398/maxY
        for point in self.setOfPoints:
            scaledSetOfPoints.append((point[0]*ratioX, point[1]*ratioY))
        return scaledSetOfPoints

    """Returns the convex polygon resulting of the bounding box of the implicit polygon"""
    def getBoundingBox(self):
        return getBoundingBoxOfPolygons([self])

"""adds one to the coordinates of a point"""
def __plusone(point):
    (x,y) = point
    return (x+1, y+1)

"""Generates a .png with name fileName with all the polygons introduced in the parameter setOfPolygons drawn on it"""
def drawPolygons(fileName, setOfPolygons):
    background = Image.new("RGB", (400, 400), color="#FFFFFF")
    draw = ImageDraw.Draw(background, 'RGBA')
    setOfPoints = []
    for polygon in setOfPolygons:
        setOfPoints += polygon.getSetOfPoints()
    xCoords = [point[0] for point in setOfPoints]
    yCoords = [point[1] for point in setOfPoints]
    minX = min(xCoords)
    minY = min(yCoords)
    listOfImages = []
    transformedPolygons = []
    for polygon in setOfPolygons:
        polygonCoords = polygon.translate(-minX, -minY)
        transformedPolygons.append(ConvexPolygon(polygonCoords, polygon.color))
    setOfPoints = []
    for polygon in transformedPolygons:
        setOfPoints += polygon.getSetOfPoints()
    xCoords = [point[0] for point in setOfPoints]
    yCoords = [point[1] for point in setOfPoints]
    maxX = max(xCoords)
    maxY = max(yCoords)
    for polygon in transformedPolygons:
        polygonCoords = polygon.scale(maxX, maxY)
        polygonCoords = list(map(__plusone,polygonCoords))
        (r, g, b) = polygon.color
        if len(polygonCoords) >= 2:
            draw.polygon(polygonCoords, fill=(r,g,b,160), outline=polygon.color)
        elif len(polygonCoords) == 1:
            draw.point(polygonCoords, fill=(r,g,b))
    background = ImageOps.flip(background)
    background.save(fileName)


"""Generates a polygon with numVertices random points between [0,1]"""
def randomPolygon(numVertices):
    points = []
    for i in range(0, numVertices):
        points.append((random.uniform(0, 1), random.uniform(0, 1)))
    return ConvexPolygon(points)


"""Returns the convex polygon resulting of the bounding box of the set of polygons introduced by parameter setOfPolygons"""
def getBoundingBoxOfPolygons(setOfPolygons):
    initSetPointsPolygon = setOfPolygons[0].getSetOfPoints()
    minX = initSetPointsPolygon[0][0]
    minY = initSetPointsPolygon[0][1]
    maxX = initSetPointsPolygon[0][0]
    maxY = initSetPointsPolygon[0][1]
    for polygon in setOfPolygons:
        for point in polygon.getSetOfPoints():
            if point[0] > maxX:
                maxX = point[0]
            if point[0] < minX:
                minX = point[0]
            if point[1] > maxY:
                maxY = point[1]
            if point[1] < minY:
                minY = point[1]
    return ConvexPolygon([(minX, minY), (minX, maxY), (maxX, maxY), (maxX, minY)])
