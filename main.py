from lark import Lark, Transformer
from parser_lark import *

def main():
    code = '''
        var variable:
        var variable: 
        var sdf: 
        var sdf:
        fun funname
    '''
    parsering(code)

    #print(la.parse("var value :").pretty('  '))


if __name__ == "__main__":
    main()