"""Necessary conditions to import depending on the directory we are"""
if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor

"""Adds path of the father directory to import the polygons file"""
if __package__ is None or not __package__:
    from sys import path
    path.append('..')

from polygons import *

"""Print all real numbers with 3 digits after the decimal dot"""
def printablePoint(point):
    return ("%.3f" % point[0])+' '+("%.3f" % point[1])

"""map booleans to yes or no instead of true or false as requested."""
def printBoolean(boolean):
    if boolean:
        return "yes"
    else:
        return "no"

"""Visitor of the compiler tree. Check the nodes depending of the input of the user"""
class TreeVisitor(ExprVisitor):

    """global dictionary to store the variables introduced by the user associated with the corresponding polygon"""
    def __init__(self):
        self.variables = {}

    """Visit the root node, return the result of visiting the tree result=(resultText, shouldPrint)"""
    def visitRoot(self, ctx: ExprParser.RootContext):
        n = next(ctx.getChildren())
        result = self.visit(n)
        if result is None:
            return (None, False)
        return self.visit(n)

    """Visit the expr node, forward result to upper nodes"""
    def visitExpr(self, ctx: ExprParser.ExprContext):
        n = next(ctx.getChildren())
        return self.visit(n)

    """Visit the simplePolygon node:
        Treats the expressions that result in a polygon with one or less polygon inputs:
            -Variable
            -Polygon
            -Random polygon
            -Bounding box
    """
    def visitSimplePolygon(self, ctx: ExprParser.SimplePolygonContext):
        variable = ctx.VARIABLE()
        polygon = ctx.polygon()
        polygonExpr = ctx.polygonExpr()
        numberOfVertices = ctx.INT()
        if variable is not None:
            return self.variables[variable.getText()]
        elif polygon is not None:
            return self.visit(polygon)
        elif numberOfVertices is not None:
            return randomPolygon(int(numberOfVertices.getText()))
        elif polygonExpr is not None:
            polygon = self.visit(polygonExpr)
            if ctx.getChild(0).getSymbol().type == ExprParser.BOUNDINGBOX:
                return polygon.getBoundingBox()
            else:
                return polygon

    """Visit the polygonOperators node:
        Treats the operations that return polygons.
        Returns the polygons resulting from the operations:
            -Union
            -Intersection
    """
    def visitPolygonOperators(self, ctx: ExprParser.PolygonOperatorsContext):
        tokenType = ctx.getChild(1).getSymbol().type
        polygonExpr = ctx.polygonExpr(0)
        secondPolygonExpr = ctx.polygonExpr(1)
        polygon = None
        secondPolygon = None
        if polygonExpr is not None:
            polygon = self.visit(polygonExpr)
        if secondPolygonExpr is not None:
            secondPolygon = self.visit(secondPolygonExpr)
        if tokenType == ExprParser.UNION:
            return polygon.union(secondPolygon)
        if tokenType == ExprParser.INTERSECTION:
            return polygon.intersection(secondPolygon)

    """Visit the noReturningOperations node:
        Treats the operations that don't return a polygon.
        The following operations should print the result as text:
            - Perimeter
            - Area
            - Vertices
            - Centroid
            - Print
            - Equal
            - Inside
        The color operation assigns a color to a variable.
        The draw operation prints in a .png file the drawed polygons.
    """
    def visitNoReturningOperations(self, ctx: ExprParser.NoReturningOperationsContext):
        tokenType = ctx.getChild(0).getSymbol().type
        polygonExpr = ctx.polygonExpr(0)
        secondPolygonExpr = ctx.polygonExpr(1)
        stringValue = ctx.STRING()
        polygon = None
        secondPolygon = None
        if polygonExpr is not None:
            polygon = self.visit(polygonExpr)
        if secondPolygonExpr is not None:
            secondPolygon = self.visit(secondPolygonExpr)

        if tokenType == ExprParser.PERIMETER:
            return (polygon.getPerimeter(), True)
        elif tokenType == ExprParser.AREA:
            return (polygon.getArea(), True)
        elif tokenType == ExprParser.VERTICES:
            return (polygon.getNumberOfVerticesAndEdges()[0], True)
        elif tokenType == ExprParser.CENTROID:
            centroid = polygon.getCentroid()
            return (printablePoint(centroid), True)
        elif tokenType == ExprParser.PRINT and polygon is not None:
            points = ""
            for point in polygon.getSetOfPoints():
                points = points+printablePoint(point)+"  "
            return (points, True)
        elif tokenType == ExprParser.PRINT and stringValue is not None:
            return (stringValue.getText()[1:-1], True)
        elif tokenType == ExprParser.EQUAL:
            return (printBoolean(polygon.isEqual(secondPolygon)), True)
        elif tokenType == ExprParser.INSIDE:
            return (printBoolean(polygon.isInsidePolygon(secondPolygon)), True)
        elif tokenType == ExprParser.COLOR:
            variable = ctx.VARIABLE().getText()
            self.variables[variable].setColor(self.visit(ctx.rgb()))
        elif tokenType == ExprParser.DRAW:
            polygons = list(map(self.visit, ctx.polygonExpr()))
            fileName = ctx.FILENAME().getText()
            drawPolygons(fileName, polygons)
            return (fileName, False)

    """visit polygon node, returns the polygon"""
    def visitPolygon(self, ctx: ExprParser.PolygonContext):
        l = [n for n in ctx.getChildren()]
        points = []
        for e in l:
            if e.getSymbol().type == ExprParser.POINT:
                points.append(tuple(map(float, e.getText().split(" "))))
        polygon = ConvexPolygon(points)
        return polygon

    """visit assign node, store in variables dictionary the variable with the polygon"""
    def visitAssign(self, ctx: ExprParser.AssignContext):
        variable = ctx.VARIABLE().getText()
        polygon = self.visit(ctx.polygonExpr())
        self.variables[variable] = polygon

    """visit rgb node, returns the color in RGB from 0 to 255"""
    def visitRgb(self, ctx: ExprParser.RgbContext):
        (red, green, blue) = tuple(map(float, ctx.RGB().getText().split(" ")))
        return (int(red*255), int(green*255), int(blue*255))
