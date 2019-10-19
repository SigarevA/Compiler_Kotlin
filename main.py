from lark import Lark, Transformer
from parser_lark import *

def main():
    code = '''
        var variable: Int
        var variable: Int
        var sdf: Int
        var sdf:Float
        fun funname
    '''
    parsering(code)

    #print(la.parse("var value :").pretty('  '))


if __name__ == "__main__":
    main()