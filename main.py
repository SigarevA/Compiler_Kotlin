from lark import Lark, Transformer, Token
from parser_lark import *
from lark import Tree, Transformer

def main():


    code = '''
        1+2+1
        fun abs(value:Int , value:Double , value:Double):Int{}
    '''
    parsering(code)

    #print(la.parse("var value :").pretty('  '))


if __name__ == "__main__":
    main()