from lark import Lark, Transformer, Token
from gen_ast import *

parser = Lark('''
        ?start: foo
        
        foo:  (glob)*

        ?glob: "fun" function
            | expr
            
        ?expr: "var" _ad "\\n"-> identvar
            | "val" _ad "\\n"-> identval
            | IF if_rule (ELSE_IF if_rule)* (ELSE "{" body "}")?
            | "while" while_rule
            | "for" for_rule
            | "when" when_rule
            | operation
            | standart_fun
            
        ?standart_fun : println 
            | readline
            | print
            
        
        ?println : "println" "(" ")"
        ?print : "print" "(" (CNAME | NUMBER | LETTER) ")"
        ?readline : "readLine" "(" ")"
          
        _ad: CNAME ":" _gettype 
            | readline
        
        _gettype: INTEGER ["=" INT]
            | FLOATTYPE  ["=" FLOAT]
            | DOUBLE  ["=" FLOAT]
            | SHORT ["=" INT]
            | LONG ["=" INT]
            | ANY ["=" NUMBER]
            | CHAR ["=" LETTER]
            
        ?for_rule: "("CNAME "in" INT ".." INT ")" "{" "\\n" body "}"
        
        ?while_rule: "(" condition ")" "{" "\\n" body "}"
        
        
        ?when_rule: "(" CNAME ")" "{" "\\n" when_body "}"
        
        ?when_body: ( (INT | FLOAT| LETTER | ELSE ) "->" ( operation | "{" "\\n" body"}") )+ 
        
        ?if_rule: "(" condition ")" "{" "\\n" body "}"
        
        ?condition: logic_op [ (AND | OR | XOR) logic_op ]
        
        ?logic_op: operation (LT | GT | EQUALS | NEQUALS | LE | GE) operation
            | CNAME
        
         
        ?operation: arithmetic
        
        ?arithmetic : [ arithmetic (ADD | SUB) ] mult 
        
        ?mult: [ mult (MUL | DIV) ] value
             
        ?value: NUMBER -> litvar
            | CNAME
        
        ?function: CNAME "(" [parametrs] ")" ":" _gettype "{" "\\n" body "}" -> funname
            
        ?parametrs : (parametr)*
            | parametrs "," parametr            
            
        parametr: CNAME ":" _gettype
        
        ?body : expr* -> body
                       
        INTEGER: "Int"
        FLOATTYPE : "Float"
        DOUBLE : "Double"
        SHORT : "Short"
        LONG : "Long"
        ANY: "Any"
        CHAR: "Char"
        
        ADD: "+"
        SUB: "-"
        MUL: "*"
        DIV: "/"
        AND: "and"
        OR: "or"
        XOR: "xor"
        ELSE: "else"
        ELSE_IF : "else if"
        IF : "if"
        
        GE:      ">="
        LE:      "<="
        NEQUALS: "!="
        EQUALS:  "=="
        GT:      ">"
        LT:      "<"
        
        OPENPARAMETR: "("
        CLOSEPARAMETR : ")"  
        OPENBLOCK: "{"
        CLOSEBLOCK: "}"
        
        
        %import common.INT
        %import common.FLOAT
        %import common.NUMBER
        %import common.CNAME
        %import common.NEWLINE
        %import common.LETTER
        
        %ignore " "
        %ignore NEWLINE
        COMMENT: "/*" /(.|\\n|\\r)+/ "*/"           
            |  "//" /(.)+/ NEWLINE
        %ignore COMMENT
     ''')



class ASTBuilder(Transformer):

    def litvar(self, args):
        return ExpOperand(args[0])

    def foo(self, args):
        return StmtListNode(args[0])


    def arithmetic(self, args):
        return BinNode(args[0], args[1], args[2])






def parsering(code: str):
    res = parser.parse(code)
    print(res)
    print(res.pretty("  "))

    res = ASTBuilder().transform(res)
    print("\n".join(res.tree))