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
    GE = '>='
    LE = "<="
    NEQUALS = "!="
    EQUALS = "=="
    GT =  ">"
    LT = "<"
    AND = "and"
    OR = "or"
    XOR = "xor"

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
    BOOLEAN = "Boolean"


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

class LogicalVariable(ExprNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

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
        return str("var " + self.type_var.value)

class SequnceNode(ExprNode):
    def __init__(self, start, end, **props):
        super().__init__(**props)
        self.start = start
        self.end = end

    def __str__(self):
        return "seq"

    @property
    def childs(self):
        return self.start, self.end

class ForNode(ExprNode):
    def __init__(self, name_var, sequnce, body, **props):
        super().__init__(**props)
        self.name_var = name_var
        self.sequnce = sequnce
        self.body = body



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

class LogicBlock(StmtNode):
    def __init__(self, type_condit, body, *expr,  **props):
        super().__init__(**props)
        self.body = body
        self.type_condit = type_condit
        self.condit = None
        if len(expr) != 0:
            self.condit = expr[0]

    def __str__(self):
        return self.type_condit

    @property
    def childs(self):
        return (self.condit, self.body) if self.condit is not None else (self.body,)

class IfelseList(StmtNode):
    def __init__(self, *conditions, **props):
        super().__init__(**props)
        self.conditions = conditions

    @property
    def childs(self):
        return self.conditions

    def __str__(self):
        return "ifelse"

class StmtListNode(StmtNode):
    def __init__(self, entry_point, *exprs, **props):
        super().__init__(**props)
        self.entry_point = entry_point
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[StmtNode, ...]:
        return self.exprs

    def __str__(self)->str:
        return self.entry_point