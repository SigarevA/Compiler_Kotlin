from lark import Lark, Transformer

parser = Lark('''
        ?start: global

        global:  (expr)*
            
        !expr: "var" ad -> identvar
            | "val" ad -> identval
            | "fun" function
            | operation
            
        ?ad: CNAME ":" gettype
        
        ?gettype: INTEGER ("=" INT)?
            | FLOATTYPE  ("=" FLOAT)?
            | DOUBLE  ("=" FLOAT)?
            | SHORT ("=" INT)?
            | LONG ("=" INT)?
        
        ?operation: arithmetic
        
        ?arithmetic : [ arithmetic (ADD | SUB) ] mult -> bin_opt
        
        ?mult: [ mult (MUL | DIV) ] value -> bin_opt
             
        ?value: NUMBER
        
        ?function: CNAME -> funname

        INTEGER: "Int"
        FLOATTYPE : "Float"
        DOUBLE : "Double"
        SHORT : "Short"
        LONG : "Long"
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
    def bin_opt(self, args):
        return eval(args[0])






def parsering(code: str):
    res = parser.parse(code)
    print(res)
    print(res.pretty("  "))
    
    res = ASTBuilder.transform(res)
    print(res)


