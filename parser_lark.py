from lark import Lark, Transformer, Token
from gen_ast import *
from scope import Scope

parser = Lark('''
        ?start: foo
        
        foo:  (glob)*

        ?glob: "fun" function
            | expr
        
        ?expr: identvar
            | "val"  "\\n"-> identval
            | ifelse "\\n"
            | "while" while_rule "\\n"
            | "for" for_rule "\\n"
            | "when" when_rule "\\n"
            | standart_fun "\\n"
            | operation "\\n"
            | returnexpr
            
        returnexpr : "return" exprout    
        
        ?exprout : ifelse "\\n"
            | "when" when_rule "\\n"
            | operation "\\n"
            
        ifelse : if_rule (elseif)* (else_rule)?
        
        if_rule : "if" "(" condition ")" "{" "\\n" body "}"
        
        elseif : "else if" "(" condition ")" "{" "\\n" body "}"
        
        else_rule : "else" "{" body "}"    
        
        ?standart_fun : println 
            | readline
            | print
            
        
        println : PRINTLN "("   [ ( operation | "'" LETTER "'"  ) ] ")"
        print : PRINT "(" ("'"LETTER"'" | operation ) ")" 
        readline : READLINE "("")"
          
        identvar: "var" name ":" ( type | "Array<" type ">") "=" possiblevalue
            | "var" name ":" (type | "Array<" type ">")
            | "var" name "=" possiblevalue
        
        
        ?possiblevalue : operation
            | "'" letter "'"
            | logicaloperand 
            | "arrayOf(" elements_arr ")"
            | readline
            
        logicaloperand : (T | F)
            | condition
            
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
            
        type : INTEGER | FLOATTYPE | DOUBLE 
            | SHORT | LONG | ANY | BOOLEAN | CHAR
           
        ?elements_arr : operation ("," operation)*
            | "'" letter "'" ("," "'"letter"'")*
        
        ?letter : LETTER -> litvar
        
        ?function: name "(" [ parametrs ] ")" [ ":" type ] "{" "\\n" body "}" -> funname
        
        ?parametrs : parametr ("," parametr)* 
            
        parametr: name ":" type
        
        ?body : expr* -> body
          
        PRINTLN : "println"
        PRINT : "print"
        READLINE : "readline"
                       
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

    def returnexpr(self, args):
        props = {}
        return ExprNodeReturn(args[0], **props)

    def println(self, args):
        props = {}
        if (len(args) == 2) :
            props["parametrs"] = args[1] if not isinstance(args[1], Token) else ExpOperand(args[1])
        return Signature(args[0], **props)

    def readline(self, args):
        return Signature(args[0])

    def print(self, args):
        props = {}
        if (len(args) == 2):
            props["parametrs"] = args[1] if not isinstance(args[1], Token) else ExpOperand(args[1])
        return Signature(args[0], **props)

    def funname(self, args):
        props = {}
        if len(args) == 3:
            key = "parametrs" if isinstance(args[1], StmtListNode) else "type"
            props[key] = args[1]
        if len(args) == 4 :
            props["type"] = args[1]
            props["parametrs"] = args[2]
        return FunNode(args[0], args[-1], **props)

    def parametrs(self, args):
        return StmtListNode("parametrs", args)

    def varlesstype(self, args):
        return IdentVar(args[0], **{"value": args[1]})

    def elements_arr(self, args):
        return ElementsArray(*args)

    def for_rule(self, args):
        return ForNode(args[0], args[1], args[2])

    def sequence(self, args):
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

    def type(self, args):
        return TypeVariable(args[0])

    def identvar(self, args):
        props = {}
        key = "type" if isinstance(args[1], TypeVariable) else "value"
        props[key] = args[1]
        if len(args) == 3:
            props["value"] = args[2]
        return IdentVar(args[0], **props)

    def logicaloperand(self, args):
        return ExpOperand(args[0])

    def parametr(self, args):
        return ( args[0], args[1] )

    def logic_op(self, args):
        if(len(args) == 3):
            operation = BinOp(args[1])
            return BinNode(args[0], operation, args[2])
        return Name(args[0])

    def while_rule(self, args):
        return WhileNode(args[0], args[1])


def parsering(code: str):
    res = parser.parse(code)
    print(res.pretty("  "))

    res = ASTBuilder().transform(res)
    print("\n".join(res.tree))
    scop = Scope(res)
    print("\n".join(res.tree))
