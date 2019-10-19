from lark import Lark, Transformer, Token
from gen_ast import *

parser = Lark('''
        ?start: foo

        foo:  (expr)*
            
        ?expr: "var" ad -> identvar
            | "val" ad -> identval
            | "fun" function
            | operation
            
        ?ad: CNAME ":" gettype
        
        ?gettype: INTEGER ["=" INT]
            | FLOATTYPE  ["=" FLOAT]
            | DOUBLE  ["=" FLOAT]
            | SHORT ["=" INT]
            | LONG ["=" INT]
            | ANY ["=" NUMBER]
        
        ?operation: arithmetic
        
        ?arithmetic : [ arithmetic (ADD | SUB) ] mult 
        
        ?mult: [ mult (MUL | DIV) ] value -> bin_opt
             
        ?value: NUMBER
        
        ?function: CNAME "(" [parametrs] ")" ":" gettype "{" body "}" -> funname
            
        ?parametrs : (parametr)*
            | parametrs "," parametr            
            
        parametr: CNAME ":" gettype
        
        ?body : 
                       
        INTEGER: "Int"
        FLOATTYPE : "Float"
        DOUBLE : "Double"
        SHORT : "Short"
        LONG : "Long"
        ANY: "Any"
        
        ADD: "+"
        SUB: "-"
        MUL: "*"
        DIV: "/"
        
        OPENPARAMETR: "("
        CLOSEPARAMETR : ")"  
        OPENBLOCK: "{"
        CLOSEBLOCK: "}"
        
        
        %import common.INT
        %import common.FLOAT
        %import common.NUMBER
        %import common.CNAME
        %import common.NEWLINE
        
        %ignore " "
        %ignore NEWLINE
        COMMENT: "/*" /(.|\\n|\\r)+/ "*/"           
            |  "//" /(.)+/ NEWLINE
        %ignore COMMENT
     ''')



class ASTBuilder(Transformer):

    def expr(self, args):
        print(len(args))
        print(args[0])
        print(len(args[0].children))
        op1 = args[0].children[0].children[0]
        op = args[0].children[1]
        op2 = args[0].children[2].children[0]
        return BinNode(op, op1, op2)

    #def foo(self, args):
        #pass
        #return StmtListNode(args[0])






def parsering(code: str):
    res = parser.parse(code)
    print(res)
    print(res.pretty("  "))

    #res = ASTBuilder().transform(res)