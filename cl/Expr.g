grammar Expr;

root : expr? ' '* COMMENT? EOF ;

expr : noReturningOperations 
    | assign
    ;

polygonExpr : '(' ' '* polygonExpr ' '* ')' #simplePolygon
            | polygon #simplePolygon
            | VARIABLE #simplePolygon
            | RANDOM INT #simplePolygon
            | BOUNDINGBOX polygonExpr #simplePolygon
            | polygonExpr UNION polygonExpr #polygonOperators
            | polygonExpr INTERSECTION polygonExpr #polygonOperators
            ;

noReturningOperations : PERIMETER ' ' polygonExpr 
                    | AREA ' ' polygonExpr
                    | VERTICES ' ' polygonExpr
                    | CENTROID ' ' polygonExpr
                    | PRINT ' ' (polygonExpr|STRING)
                    | INSIDE ' ' polygonExpr ', ' polygonExpr
                    | EQUAL ' ' polygonExpr ', ' polygonExpr
                    | COLOR ' ' VARIABLE ', ' rgb
                    | DRAW ' ' '"' FILENAME '"' (', ' polygonExpr)+
                    ;


polygon : ( '[' (' ')* ']' | '[' POINT ('  ' POINT)* ']' ) ;
assign : VARIABLE ' '* ASSIGN ' '* polygonExpr ;
rgb: '{' RGB '}' ;

RGB: ZEROTOONE ' ' ZEROTOONE ' ' ZEROTOONE;
ZEROTOONE : ('1' ('.''0'+)? |'0' ('.' INT)? ) ;
POINT : FLOAT ' ' FLOAT ;
INT : [0-9]+ ;
SIGNED_INT : '-'? INT ;
FLOAT : SIGNED_INT ('.' (INT) )? ;

ASSIGN : ':=' ;
COLOR : 'color' ;

UNION : (' '* '+' ' '*) ;
INTERSECTION : (' '* '*' ' '*) ;
BOUNDINGBOX : '#' ;
RANDOM : '!' ;

PRINT : 'print' ;
AREA : 'area' ;
PERIMETER: 'perimeter' ;
VERTICES: 'vertices' ;
CENTROID: 'centroid' ;

EQUAL : 'equal' ;
INSIDE : 'inside' ;

DRAW : 'draw' ;

COMMENT : '//' .* ;
STRING : '"' ([A-Za-z0-9 ]|'-')* '"' ;
FILENAME: [A-Za-z0-9]* '.' ('png'|'PNG');
VARIABLE : [A-Za-z]+ [A-Za-z0-9]* ;

WS : [ \n]+ -> skip;