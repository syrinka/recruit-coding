from typing import List, Literal, Union
from op import Operator
import re


class Atom(object):
    """表达式的最小单元"""
    type: Literal['op', 'num', 'lquote', 'rquote']
    value: Union[int, Operator, None]
    prior: int = 0

    def __init__(self, type, value=None):
        if type == 'op':
            value = Operator.get(value)
            self.prior = value.prior
        
        self.type = type
        self.value = value
        

    def __repr__(self):
        if self.type == 'lquote':
            r = '('
        elif self.type == 'rquote':
            r = ')'
        elif self.type == 'op':
            r = self.value.__name__
        else:
            r = self.value
        return f' {r} '


def parse(expr: str) -> List[Atom]:
    """分解表达式为原子列表
    
    包括：操作数，操作符，左括号，右括号

    @param expr : 表达式
    @return atoms : 原子列表
    """
    step = re.compile(r'\(|\)|-?[\d\.]+|[A-Za-z]+')
    raw = re.finditer(step, expr)

    def isnum(str) -> bool:
        try:
            float(str)
            return True
        except ValueError:
            return False

    result = []
    for i in raw:
        if i[0] == '(':
            result.append(Atom('lquote'))
        elif i[0] == ')':
            result.append(Atom('rquote'))
        elif isnum(i[0]):
            result.append(Atom('num', float(i[0])))
        else:
            result.append(Atom('op', i[0]))

    return result


def build(atoms: List[Atom]) -> List[Atom]:
    """构造逆波兰表达式，后置操作符

    在这一步将移除所有括号

    @param atoms :
    @return noquote : 不再有括号的原子列表
    """
    s1: List[Atom] = []
    s2: List[Atom] = []
    for atom in atoms:
        if atom.type == 'num':
            s2.append(atom)
        elif atom.type == 'op':
            while True:
                if not s1 or s1[-1].type == 'lquote':
                    s1.append(atom)
                    break
                elif atom.prior > s1[-1].prior \
                    or atom.value.apply < s1[-1].prior:
                    s1.append(atom)
                    break
                else:
                    s2.append(s1.pop())
        elif atom.type == 'lquote':
            s1.append(atom)
        elif atom.type == 'rquote':
            while True:
                atom_ = s1.pop()
                if atom_.type == 'lquote':
                    # 丢弃一对括号
                    break
                else:
                    s2.append(atom_)

    while s1:
        s2.append(s1.pop())

    return s2


def calc(atoms: List[Atom]) -> int:
    """计算逆波兰表达式的最终值
    
    @raise TypeError : 当操作的入参不足
    """
    stack = []
    for atom in atoms:
        if atom.type == 'num':
            stack.append(atom.value)
        elif atom.type == 'op':
            op = atom.value
            args, stack[-op.apply:] = stack[-op.apply:], []
            stack.append(op.eval(*args))
    
    return stack[0]


if __name__ == '__main__':
    import sys
    expr = ' '.join(sys.argv[1:])
    if not expr:
        print('''Usage: python3 main.py EXPR

  简易计算器，支持括号，支持定义更多操作

  已定义操作：add，sub，mul，div，pow，abs，rev

EXPR：表达式，例 “1 add 5”，“1 mul (5 sub 3)”
''')
        exit(0)

    a = parse(expr)
    # print(a)
    b = build(a)
    c = calc(b)

    print(c)
