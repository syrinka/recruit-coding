from __future__ import annotations


class Operator(object):
    prior: int = 0 # 优先级
    apply: int = 2 # 入参数目

    @staticmethod
    def get(name: str) -> Operator:
        """获取对应的操作符
        
        @param name : 操作符
        @return op : Operator
        @raise KeyError : 若试图获取的操作符不存在
        """
        # 访问全局变量获取对应类
        return globals()[name]

    def eval(*args):
        raise NotImplementedError


class add(Operator):
    def eval(a, b):
        return a + b


class sub(Operator):
    def eval(a, b):
        return a - b


class div(Operator):
    prior = 10
    def eval(a, b):
        return a / b


class mul(Operator):
    prior = 10
    def eval(a, b):
        return a * b


class pow(Operator):
    def eval(a, b):
        return a ** b


class abs(Operator):
    prior = 20
    apply = 1
    def eval(a):
        return a if a > 0 else -a


class rev(Operator):
    prior = 20
    apply = 1
    def eval(a):
        return -a


class rand(Operator):
    prior = 30
    apply = 0
    def eval():
        return __import__('random').random()


# 以下，定义新的操作

class limit(Operator):
    prior = -10
    apply = 3
    def eval(a, b, i):
        if i < a:
            return a
        elif i > b:
            return b
        return i


class okokok(Operator):
    def eval(a, b):
        return 0

