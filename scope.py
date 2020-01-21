import sys

from gen_ast import FunNode
from gen_ast import *


class Scope:
    def __init__(self, stmtlist):
        entrypoint = None
        functions = []
        for stmtnode in stmtlist:
            print(type(stmtnode))
            if isinstance(stmtnode, FunNode):
                if stmtnode.name.name == "main":
                    if entrypoint is not None:
                        print('Определены более одного метода main!')
                        sys.exit(1)
                    entrypoint = stmtnode
                else:
                    functions.append(stmtnode)

        if entrypoint is None:
            print("Метод main Не найден !")
            sys.exit(0)

        for exprNode in stmtlist:
            if isinstance(exprNode, IdentVar) and not hasattr(exprNode, "value"):
                print('Поле {} не присвоено значение ! '.format(exprNode.name))
                exit(0)
            if not hasattr(exprNode, "type"):
                if self.isint(exprNode.value.value):
                    exprNode.value = int(exprNode.value.value)
                    setattr(exprNode, "type", TypeVariable("Int"))
                if self.isfloat(exprNode.value.value):
                    exprNode.value = float(exprNode.value.value)
                    setattr(exprNode, "type", TypeVariable("Double"))

        self.initvar(entrypoint)

    def initvar(self, block):
        for targetNode in block.body:
            if isinstance(targetNode, IdentVar):
                if isinstance(targetNode.value, ExpOperand):
                    print(targetNode.value.value.value)
                if hasattr(targetNode, "value") and isinstance(targetNode.value, Name):
                    tempbody = block
                    self.replacevar(targetNode, block.body)
                    while isinstance(targetNode.value, Name):
                        if hasattr(tempbody, "parent"):
                            tempbody = tempbody.parent
                        else:
                            print('Переменная с названием {} не была определена!'.format(targetNode.value))
                            exit(0)
                        self.replacevar(targetNode, block.body)

    def replacevar(self, exprNode, stmtlist):
        for tempNode in stmtlist:
            if (tempNode == exprNode):
                break
            if isinstance(tempNode, IdentVar) and str(tempNode.name) == str(exprNode.value):
                if hasattr(tempNode, 'type'):
                    print(tempNode.type)
                exprNode.value = tempNode.value




    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def isint(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
