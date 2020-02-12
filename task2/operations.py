from fuzzy import MutableFuzzySet, Debug
from domain import Domain


class BinaryFunction(object):

    def __init__(self, func):
        self.func = func

    def value_at(self, num1, num2):
        return self.func(num1, num2)


class UnaryFunction(object):

    def __init__(self, func):
        self.func = func

    def value_at(self, num):
        return self.func(num)


class Operations(object):

    @staticmethod
    def unary_operation(fset, un_func):
        new_mf_set = MutableFuzzySet(fset.domain)

        for elem in fset.domain:
            new_mf_set.set(elem, un_func.value_at(fset.get_value_at(elem)))

        return new_mf_set

    @staticmethod
    def binary_operation(fset1, fset2, bin_func):
        new_mf_set = MutableFuzzySet(fset1.domain)

        for elem in fset1.domain:
            new_mf_set.set(elem, bin_func.value_at(fset1.get_value_at(elem), fset2.get_value_at(elem)))

        return new_mf_set

    @staticmethod
    def zadeh_not():
        @UnaryFunction
        def not_wrapper(value):
            return 1 - value
        return not_wrapper

    @staticmethod
    def zadeh_and():
        @BinaryFunction
        def and_wrapper(value1, value2):
            return min(value1, value2)
        return and_wrapper

    @staticmethod
    def zadeh_or():
        @BinaryFunction
        def or_wrapper(value1, value2):
            return max(value1, value2)
        return or_wrapper

    @staticmethod
    def hamacher_t_norm(num):
        @BinaryFunction
        def t_norm_wrapper(a, b):
            return a * b / (num + (1 - num) * (a + b - a * b))
        return t_norm_wrapper

    @staticmethod
    def hamacher_s_norm(num):
        @BinaryFunction
        def s_norm_wrapper(a, b):
            return (a + b - (2 - num) * a * b) / (1 - (1 - num) * a * b)
        return s_norm_wrapper


def main():

    dom = Domain.int_range(0, 11)
    set1 = MutableFuzzySet(dom)
    set1.set(0, 1.0)
    set1.set(1, 0.8)
    set1.set(2, 0.6)
    set1.set(3, 0.4)
    set1.set(4, 0.2)
    Debug.print(set1, "Set1:")

    notset1 = Operations.unary_operation(set1, Operations.zadeh_not())
    Debug.print(notset1, "notSet1:")
    print()

    union = Operations.binary_operation(set1, notset1, Operations.zadeh_or())
    Debug.print(union, "Set1 union notSet1:")
    print()

    intersection = Operations.binary_operation(set1, notset1, Operations.zadeh_and())
    Debug.print(intersection, "Set1 intersection notSet1:")
    print()

    hinters = Operations.binary_operation(set1, notset1, Operations.hamacher_t_norm(1.0))
    Debug.print(hinters, "Set1 intersection with notSet1 using parameterised"
                         " Hamacher T norm with parameter 1.0:")


if __name__ == '__main__':
    main()
