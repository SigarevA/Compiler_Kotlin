from lark import Lark, Transformer
from parser_lark import *

def main():
    code = '''
        1 + 2 + 2 * 3
    '''
    parsering(code)

    #print(la.parse("var value :").pretty('  '))


if __name__ == "__main__":
    main()