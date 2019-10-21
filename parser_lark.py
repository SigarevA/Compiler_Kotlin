from lark import Lark, Transformer, Token
from gen_ast import *

parser = Lark('''
        ?start: foo
        
        foo:  (glob)*

        ?glob: "fun" function
            | expr
            
        ?expr: "var" _ad "\\n"-> identvar
            | _ad "\\n"-> identval
            | IF if_rule (ELSE_IF if_rule)* (ELSE "{" body "}")?
            | "while" while_rule 
            | "for" for_rule
            | "when" when_rule "\\n"
            | standart_fun "\\n"
            | operation "\\n"
            
        ?standart_fun : println 
            | readline
            | print
            
        
        ?println : "println" "(" ")"
        ?print : "print" "(" (name | NUMBER | LETTER) ")"
        ?readline : "readLine" "(" ")"
          
        _ad: name ":" _gettype 
            | readline
        
        _gettype: INTEGER ["=" operation ]
            | FLOATTYPE  ["=" operation ]
            | DOUBLE  ["=" operation ]
            | SHORT ["=" operation ]
            | LONG ["=" operation ]
            | ANY ["=" NUMBER]
            | CHAR ["=" "'" LETTER "'"]
            
        ?for_rule: "("name "in" INT ".." INT ")" "{" "\\n" body "}"
        
        ?while_rule: "(" condition ")" "{" "\\n" body "}"
        
        
        ?when_rule: "(" name ")" "{" "\\n" when_body "}"
        
        ?when_body: ( (INT | FLOAT| LETTER | ELSE ) "->" ( operation | "{" "\\n" body"}") )+ 
        
        ?if_rule: "(" condition ")" "{" "\\n" body "}"
        
        ?condition: logic_op [ (AND | OR | XOR) logic_op ]
        
        ?logic_op: operation (LT | GT | EQUALS | NEQUALS | LE | GE) operation
            | name
         
        ?operation: arithmetic
        
        ?arithmetic : [ arithmetic (ADD | SUB) ] mult 
        
        ?mult: [ mult (MUL | DIV) ] value
             
        ?value: NUMBER -> litvar
            | name
        
        ?function: name "(" [parametrs] ")" ":" _gettype "{" "\\n" body "}" -> funname
            
        ?parametrs : parametr ("," parametr)*
            
        parametr: name ":" _gettype
        
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
        
        name : CNAME
        
        
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

    def name(self, args):
        return Name(args[0])

    def mult(self, args):
        operation = BinOp(args[1])
        return BinNode(args[0], operation, args[2])

    def litvar(self, args):
        return ExpOperand(args[0])

    def foo(self, args):
        return StmtListNode(*args)

    def arithmetic(self, args):
        operation = BinOp(args[1])
        return BinNode(args[0], operation, args[2])

    def identvar(self, args):
        type_of_var = TypeVariable(args[1])
        if len(args) == 2:
            return IdentVar(args[0], type_of_var)
        if len(args) == 3:
            return IdentVar(args[0], type_of_var, args[2])

    def parametr(self, args):
        return (args[0], args[1])





def parsering(code: str):
    res = parser.parse(code)
    print(res)
    print(res.pretty("  "))

    res = ASTBuilder().transform(res)
    print("\n".join(res.tree))