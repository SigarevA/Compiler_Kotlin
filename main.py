from parser_lark import *
from Test.test import getTest

def main():

    test = getTest()
    parsering(test())
    #print(la.parse("var value :").pretty('  '))

if __name__ == "__main__":
    main()