# Generated from Expr.g by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete generic visitor for a parse tree produced by ExprParser.

class ExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#root.
    def visitRoot(self, ctx:ExprParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#expr.
    def visitExpr(self, ctx:ExprParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#polygonOperators.
    def visitPolygonOperators(self, ctx:ExprParser.PolygonOperatorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#simplePolygon.
    def visitSimplePolygon(self, ctx:ExprParser.SimplePolygonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#noReturningOperations.
    def visitNoReturningOperations(self, ctx:ExprParser.NoReturningOperationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#polygon.
    def visitPolygon(self, ctx:ExprParser.PolygonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#assign.
    def visitAssign(self, ctx:ExprParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#rgb.
    def visitRgb(self, ctx:ExprParser.RgbContext):
        return self.visitChildren(ctx)



del ExprParser