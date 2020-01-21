from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum


class AstNode(ABC):
    def __init__(self, **props):
        super().__init__()
        for k, v in props.items():
            setattr(self, k, v)

    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> [str, ...]:
        res = [str(self)]
        childs_temp = self.childs
        for i, child in enumerate(childs_temp):
            ch0, ch = '├', '│'
            if i == len(childs_temp) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None]) -> None:
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
    GT = ">"
    LT = "<"
    AND = "and"
    OR = "or"
    XOR = "xor"


class TypeVariable(Enum):
    INT = "Int"
    DOUBLE = "Double"
    FLOAT = "Float"
    SHORT = "Short"
    LONG = "Long"
    ANY = "Any"
    CHAR = "Char"
    BOOLEAN = "Boolean"
    ARRAY = "Array"
    FUN = "fun"


class NameStandardFun(Enum):
    PRINTLN = "println"
    PRINT = "PRINT"
    READLINE = "READLINE"


class ExpOperand(ExprNode):
    def __init__(self, value, **props):
        super().__init__(**props)
        self.value = value

    def __str__(self):
        return str(self.value)


class ParametrNode(ExprNode):
    def __init__(self, name, **props):
        super().__init__(**props)
        self.name = name

    @property
    def childs(self):
        return self.name,

    def __str__(self):
        return "parametr"


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
    def __init__(self, name, *args, **props):
        super().__init__(**props)
        self.name = name

    @property
    def childs(self):
        results = []
        results.append(self.name)
        if (hasattr(self, "value")):
            results.append(self.value)

        return results

    def __str__(self):
        return "var"


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

    def __str__(self):
        return "for"

    @property
    def childs(self):
        return self.name_var, self.sequnce, self.body


class BinNode(ExprNode):
    def __init__(self, operand1, operation, operand2, **props):
        super().__init__(**props)
        self.op = operation
        self.op1 = operand1
        self.op2 = operand2

    @property
    def childs(self):
        return self.op1, self.op2

    def __str__(self) -> str:
        return str(self.op.value)


class LogicBlock(StmtNode):
    def __init__(self, type_condit, body, *expr, **props):
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


class ElementsArray(ExprNode):
    def __init__(self, *exprs, **props):
        super().__init__(**props)
        self.els = exprs

    def __str__(self):
        return "elements"

    @property
    def childs(self):
        return self.els


class IteratorStmtList():
    def __init__(self, exprs):
        self.exprs = exprs
        self.count = -1

    def __next__(self):
        if self.count < len(self.exprs) - 1:
            self.count += 1
            return self.exprs[self.count]
        else:
            self.count = 0
            raise StopIteration

    def __iter__(self):
        return self



class StmtListNode(StmtNode):
    def __init__(self, entry_point, *exprs, **props):
        super().__init__(**props)
        self.entry_point = entry_point
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[StmtNode, ...]:
        return self.exprs

    def __str__(self) -> str:
        return self.entry_point

    def __iter__(self):
        return IteratorStmtList(self.exprs)



class StmtArray(StmtNode):
    def __init__(self, name, els, **props):
        super().__init__(**props)
        self.name = name
        self.els = els

    def __str__(self):
        return "array"

    @property
    def childs(self):
        return (self.name, self.els)


class WhileNode(ExprNode):
    def __init__(self, cond, body, **props):
        super().__init__(**props)
        self.cond = cond
        self.body = body

    def __str__(self):
        return "while"

    @property
    def childs(self):
        return self.cond, self.body


class FunNode(ExprNode):

    def __init__(self, name, body, **props):
        super().__init__(**props)
        self.name = name
        self.body = body

    def __iter__(self):
        return self.body

    def __str__(self):
        return "fun"

    @property
    def childs(self):
        return self.name, self.body


class Signature(StmtNode):
    def __init__(self, name, **props):
        super().__init__(**props)
        self.name = name

    def __str__(self):
        return self.name

    @property
    def childs(self):
        list_ret = []
        if hasattr(self, "parametrs"):
            list_ret.append(getattr(self, "parametrs"))
        if hasattr(self, "type"):
            list_ret.append(getattr(self, "type"))
        return list_ret


class ExprNodeReturn(ExprNode):
    def __init__(self, expr, **props):
        super().__init__(**props)
        self.expr = expr

    def __str__(self):
        return "return"

    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return self.expr,