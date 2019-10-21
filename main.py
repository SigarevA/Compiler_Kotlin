from lark import Lark, Transformer, Token
from parser_lark import *
from lark import Tree, Transformer

def getCodeTest1():
    code = '''
        1+2+3
        1+2+3
        1+2+3
        fun abs(fg: Int , yt:Double , yt:Double, yt:Double):Double{
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
        var prame: Int = 1 + 2  
        var primary: Int = prame
    '''
    return code

def getCodeTest3():
    code = '''
        var variab: Int = 9
        var variab: Int
        var gdffsd : Double = 3
        gdffsd / 3 + 2 * 3 - 3
    '''
    return code

def getCodeTest4():
    code = '''
        var prame: Int = 1 + 2  
        var primary: Int = prame        
    '''
    return code

def main():

    code = getCodeTest3()
    parsering(code)

    #print(la.parse("var value :").pretty('  '))

if __name__ == "__main__":
    main()