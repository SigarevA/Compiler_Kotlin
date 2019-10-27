from lark import Lark, Transformer, Token
from gen_ast import *

parser = Lark('''
        ?start: foo
        
        foo:  (glob)*

        ?glob: "fun" function
            | expr
            
        ?expr: "var" _ad "\\n"-> identvar
            | "val" _ad "\\n"-> identval
            | ifelse "\\n"
            | "while" while_rule "\\n"
            | "for" for_rule "\\n"
            | "when" when_rule "\\n"
            | standart_fun "\\n"
            | operation "\\n"
        
        ifelse : if_rule (elseif)* (else_rule)?
        
        if_rule : "if" "(" condition ")" "{" "\\n" body "}"
        
        elseif : "else if" "(" condition ")" "{" "\\n" body "}"
        
        else_rule : "else" "{" body "}"    
        
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
            | BOOLEAN ["=" logicaloperand]
            
        logicaloperand : T | F
            
        ?for_rule: "("name "in" (  sequence | name ) ")" "{" "\\n" body "}"
        
        ?sequence: INT ".." INT
        
        ?while_rule: "(" condition ")" "{" "\\n" body "}"
        
        
        ?when_rule: "(" name ")" "{" "\\n" when_body "}"
        
        ?when_body: ( (INT | FLOAT| LETTER | ELSE ) "->" ( operation | "{" "\\n" body"}") )+ 
        
        ?condition: [ condition (AND | OR | XOR) ] logic_op
        
        ?logic_op: operation (LT | GT | EQUALS | NEQUALS | LE | GE) operation
            | name -> logic_op
         
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
        BOOLEAN : "Boolean"
        F : "true"
        T : "false"
        
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

    def for_rule(self, args):
        pass

    def sequnce(self, args):
        return SequnceNode(ExpOperand(args[0]), ExpOperand(args[1]))

    def else_rule(self, args):
        return LogicBlock("else", args[0])

    def elseif(self, args):
        return LogicBlock("else if", args[1], args[0])

    def if_rule(self, args):
        return LogicBlock("if", args[1], args[0])

    def condition(self, args):
        operation = BinOp(args[1])
        return BinNode(args[0], operation, args[2])

    def ifelse(self, args):
        return IfelseList(*args)

    def body(self, args):
        return StmtListNode('body', *args)

    def name(self, args):
        return Name(args[0])

    def ifna(self, args):
        pass

    def mult(self, args):
        operation = BinOp(args[1])
        return BinNode(args[0], operation, args[2])

    def litvar(self, args):
        return ExpOperand(args[0])

    def foo(self, args):
        return StmtListNode('...', *args)

    def arithmetic(self, args):
        operation = BinOp(args[1])
        return BinNode(args[0], operation, args[2])

    def identvar(self, args):
        type_of_var = TypeVariable(args[1])
        if len(args) == 2:
            return IdentVar(args[0], type_of_var)
        if len(args) == 3:
            return IdentVar(args[0], type_of_var, args[2])

    def logicaloperand(self, args):
        return ExpOperand(args[0])

    def parametr(self, args):
        return (args[0], args[1])

    def logic_op(self, args):
        if(len(args) == 3):
            operation = BinOp(args[1])
            return BinNode(args[0], operation, args[2])
        return Name(args[0])


def parsering(code: str):
    res = parser.parse(code)
    print(res)
    print(res.pretty("  "))

    res = ASTBuilder().transform(res)
    print("\n".join(res.tree))