from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum


class AstNode(ABC):
    def __init__(self, **props):
        super().__init__()
        for k, v in props.items():
            setattr(self, k, v)

    @property
    def childs(self)->Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self)->str:
        pass

    @property
    def tree(self)->[str, ...]:
        res = [str(self)]
        childs_temp = self.childs
        for i, child in enumerate(childs_temp):
            ch0, ch = '├', '│'
            if i == len(childs_temp) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None])->None:
        func(self)
        map(func, self.childs)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None



class ExprNode(AstNode):
    pass

class StmtNode(ExprNode):
    pass

class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'

class ParametrNode():
    def __init__(self, name, type, **props):
        super().__init__(**props)
        self.name = name
        self.type = type

    @property
    def childs(self):
        return self.name, self.type


    def __str__(self):
        return "parametr"

class TypeVariable(Enum):
    INT = "Int"
    DOUBLE = "Double"
    FLOAT = "Float"
    SHORT = "Short"
    LONG = "Long"
    ANY = "Any"
    CHAR = "Char"



class ExpOperand(ExprNode):
    def __init__(self, value, **props):
        super().__init__(**props)
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(ExprNode):
    def __init__(self, name, **props):
        super().__init__(**props)
        self.name = name

    def __str__(self):
        return str(self.name)

class IdentVar(ExprNode):
    def __init__(self, name, type_var, *args, **props):
        super().__init__(**props)
        self.name = name
        self.type_var = type_var
        self.value = None
        if len(args) != 0:
            self.value = args[0]

    @property
    def childs(self):
        return (self.name, ) if self.value is None else (self.name, self.value)

    def __str__(self):
        return str(self.type_var.value)


class BinNode(ExprNode):
    def __init__(self, operand1, operation, operand2, **props):
        super().__init__(**props)
        self.op = operation
        self.op1 = operand1
        self.op2 = operand2

    @property
    def childs(self):
        return self.op1, self.op2

    def __str__(self)->str:
        return str(self.op.value)

class StmtListNode(StmtNode):
    def __init__(self, *exprs, **props):
        super().__init__(**props)
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[StmtNode, ...]:
        return self.exprs

    def __str__(self)->str:
        return '...'