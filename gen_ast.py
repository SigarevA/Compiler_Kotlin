from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum


class AstNode(ABC):
    def __init__(self, row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__()
        self.row = row
        self.line = line
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


class BinNode(AstNode):
    def __init__(self, operation, operand1, operand2):
        self.op = operation
        self.op1 = operand1
        self.op2 = operand2

    @property
    def childs(self):
        return self.op1, self.op2

    def __str__(self):
        return " ".join([self.op1, self.op, self.op2])


class StmtListNode(StmtNode):
    def __init__(self, *exprs: StmtNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[StmtNode, ...]:
        return self.exprs

    def __str__(self)->str:
        return '...'
