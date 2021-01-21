import sys
from antlr4 import *

"""Necessary conditions to import depending on the directory we are"""
if __name__ is not None and "." in __name__ or __package__ is not None and __package__:
    from .ExprLexer import ExprLexer
    from .ExprParser import ExprParser
    from .TreeVisitor import TreeVisitor
else:
    from ExprLexer import ExprLexer
    from ExprParser import ExprParser
    from TreeVisitor import TreeVisitor



def compileLine(visitor, line):
    lexer = ExprLexer(InputStream(line))
    token_stream = CommonTokenStream(lexer)
    parser = ExprParser(token_stream)
    tree = parser.root()
    return visitor.visit(tree)


def main():
    visitor = TreeVisitor()
    inputValue = input('? ')
    while inputValue != ":q":
#        try:
        (resultText, shouldPrint) = compileLine(visitor, inputValue)
        if shouldPrint:
            print(resultText)
#        except:
#            print("Error in command")
        inputValue = input('? ')

if __name__ == '__main__':
    main()
