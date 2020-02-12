from domain import Domain


class ElementNotInDomainError(Exception):
    pass


class MembershipError(Exception):
    pass


class IntUnaryFunction(object):

    def __init__(self, func):
        self.func = func

    def value_at(self, num):
        return self.func(num)


class StandardFuzzySets(object):

    @staticmethod
    def l_function(alpha, beta):
        @IntUnaryFunction
        def l_func(x):
            if x < alpha:
                return 1
            elif x >= beta:
                return 0
            else:
                return (beta - x) / (beta - alpha)
        return l_func

    @staticmethod
    def gamma_function(alpha, beta):
        @IntUnaryFunction
        def gamma(x):
            if x < alpha:
                return 0
            elif x >= beta:
                return 1
            else:
                return (x - alpha) / (beta - alpha)
        return gamma

    @staticmethod
    def lambda_function(alpha, beta, gamma):
        @IntUnaryFunction
        def value_at(x):
            if x < alpha:
                return 0
            elif x >= gamma:
                return 0
            elif beta > x >= alpha:
                return (x - alpha) / (beta - alpha)
            else:
                return (gamma - x) / (gamma - beta)
        return value_at


class FuzzySet(object):

    def get_domain(self):
        pass

    def get_value_at(self, domain_element):
        pass

    def cutoff(self, mi):
        pass


class MutableFuzzySet(FuzzySet):

    def __init__(self, domain):
        self.domain = domain
        self.memberships = [0. for _elem in self.domain]

    def get_domain(self):
        return self.domain

    def get_value_at(self, domain_element):
        if self.domain.index_of_element(domain_element) is None:
            raise ElementNotInDomainError("'{0}' is not in the set's domain.".format(domain_element))
        return self.memberships[self.domain.index_of_element(domain_element)]

    def set(self, domain_element, membership):
        if self.domain.index_of_element(domain_element) is None:
            raise ElementNotInDomainError("'{0}' is not in the set's domain.".format(domain_element))
        if membership < 0 or membership > 1:
            raise MembershipError("Membership must be a value between 0 and 1.")
        self.memberships[self.domain.index_of_element(domain_element)] = membership

    def cutoff(self, mi):
        cut = MutableFuzzySet(self.domain)
        for elem in self.domain:
            cut.set(elem, min(self.get_value_at(elem), mi))
        return cut


class CalculatedFuzzySet(FuzzySet):

    def __init__(self, domain, func):
        self.domain = domain
        self.func = func

    def get_domain(self):
        return self.domain

    def get_value_at(self, domain_element):
        return self.func.value_at(self.domain.index_of_element(domain_element))

    def cutoff(self, mi):
        cut = MutableFuzzySet(self.domain)
        for elem in self.domain:
            cut.set(elem, min(self.get_value_at(elem), mi))
        return cut


class Debug(object):

    @staticmethod
    def print(fset, header=""):
        print(header)
        if type(fset) is MutableFuzzySet:
            for elem, membership in zip(fset.domain, fset.memberships):
                print("d({0})={1}".format(elem, membership))
        elif type(fset) is CalculatedFuzzySet:
            for elem in fset.domain:
                print("d({0})={1}".format(elem, fset.get_value_at(elem)))
        else:
            print("Unknown type for debuging! Try printing a fuzzy set.")


def main():
    dom = Domain.int_range(0, 11)

    set1 = MutableFuzzySet(dom)
    set1.set(4, 0.2)
    set1.set(6, 0.4)
    set1.set(9, 0.5)

    dom1 = Domain.int_range(-5, 6)
    print(dom1)

    set2 = CalculatedFuzzySet(dom1,
                              StandardFuzzySets.lambda_function(
                                  dom1.index_of_element(-4),
                                  dom1.index_of_element(0),
                                  dom1.index_of_element(4)
                              ))

    set3 = CalculatedFuzzySet(dom1,
                              StandardFuzzySets.l_function(
                                  dom1.index_of_element(-4),
                                  dom1.index_of_element(0),
                              ))
    Debug.print(set1, "Set1:")
    print(set2.domain)
    Debug.print(set2, "Set2:")
    Debug.print(set3, "Set3:")


if __name__ == '__main__':
    main()
