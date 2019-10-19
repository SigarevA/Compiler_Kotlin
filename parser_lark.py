from lark import Lark, Transformer

parser = Lark('''
        ?start: global

        global:  (expr )*
            
        ?expr: "var" ad 
            | "fun" function
            
        ?ad: CNAME ":"-> advariable
        
        ?function: CNAME -> funname
            

        ?paramets: parametr 
            | parametrs "," parametr           

        ?parametr: CNAME 

        ?parametrs: CNAME  -> name

        OPENPARAMETR: "("
        CLOSEPARAMETR : ")"  
        OPENBLOCK: "{"
        CLOSEBLOCK: "}"
        //DATATYPES: ["Int""STRING""Byte"] 
        
        %import common.CR
        %import common.CNAME
        %import common.NEWLINE
        %import common.WORD   // imports from terminal library
        %import common.CNAME
        %ignore " "
        %ignore NEWLINE
        COMMENT: "/*" /(.|\\n|\\r)+/ "*/"           
            |  "//" /(.)+/ NEWLINE
        %ignore COMMENT
     ''')


def parsering(code: str):
    res = parser.parse(code)
    #print(res)
    print(res.pretty("  "))


