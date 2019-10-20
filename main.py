from lark import Lark, Transformer, Token
from parser_lark import *
from lark import Tree, Transformer

def getCodeTest1():
    code = '''
        1+2+3
        1+2+3
        1+2+3
        fun abs():Double{
            var operand: Double
            val operand: Int
            when(operand){
                1 -> 1+1 
                1 -> {
                    1+2
                    21+3
                }
                else -> 2+1
            }
            
            while (2 <= 4) {
             1+12
            }

            for(op in 1..3){

            }
            
        }
    '''
    return code

def getCodeTest2():
    code = '''
        val a: Int = 10
        if(a == 10) {
        }
        else if(a == 9){
        }
        else if(a == 8){
        }
        else{
        }  
    '''
    return code

def getCodeTest3():
    code = '''
        1+1+1
        
    '''
    return code

def main():

    code = getCodeTest3()
    parsering(code)

    #print(la.parse("var value :").pretty('  '))


if __name__ == "__main__":
    main()