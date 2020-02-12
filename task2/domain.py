from itertools import product


class DomainElement(object):

    def __init__(self, values):
        self.values = values

    def get_number_of_components(self):
        return len(self.values)

    def get_component_value(self, index):
        return self.values[index]


class Domain(object):

    @staticmethod
    def int_range(first, last):
        return SimpleDomain(first, last)

    @staticmethod
    def combine(domain1, domain2):
        return CompositeDomain(domain1, domain2)

    def get_cardinality(self):
        pass

    def get_component(self, index):
        pass

    def get_number_of_components(self):
        pass

    def index_of_element(self, element):
        pass

    def element_for_index(self, index):
        pass


class SimpleDomain(Domain):

    def __init__(self, first, last):
        self.first = first
        self.last = last
        self._counter = first - 1

    def __iter__(self):
        return self

    def __next__(self):
        self._counter += 1
        if self._counter == self.last:
            self._counter = self.first - 1
            raise StopIteration
        else:
            return self._counter

    def __repr__(self):
        return ",".join([str(item) for item in self])

    def element_for_index(self, index):
        if index >= self.last - self.first or index < 0:
            raise IndexError("Index out of bounds!")
        return self.first + index

    def index_of_element(self, element):
        for index, elem in enumerate(range(self.first, self.last)):
            if elem == element:
                return index
        return None

    def get_cardinality(self):
        return self.last - self.first

    def get_component(self, index):
        return self

    def get_number_of_components(self):
        return 1


class CompositeDomain(Domain):

    def __init__(self, *domains):
        self.domains = domains
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= self.get_cardinality():
            self._index = 0
            raise StopIteration
        self._index += 1
        return self.element_for_index(self._index - 1)

    def __repr__(self):
        return str(list(product(*self.domains)))

    def element_for_index(self, index):
        if index >= self.get_cardinality() or index < 0:
            raise IndexError("Index out of bounds!")

        domain_element_set = list(product(*self.domains))

        return domain_element_set[index]

    def index_of_element(self, element):
        for index, elem in enumerate(product(*self.domains)):
            if elem == element:
                return index
        return None

    def get_cardinality(self):
        card = 0 if len(self.domains) == 0 else 1
        for domain in self.domains:
            card *= domain.get_cardinality()
        return card

    def get_number_of_components(self):
        return len(self.domains)

    def get_component(self, index):
        return self.domains[index]


def main():
    dom1 = Domain.int_range(0, 5)

    print("Elementi domene dom1:")
    print(dom1)
    print("Kardinalitet domene je:", dom1.get_cardinality())

    # print(dom1.index_of_element(3))
    # print(dom1.index_of_element(19))
    # print(dom1.element_for_index(2))
    # print(dom1.element_for_index(-1))
    dom2 = Domain.int_range(0, 3)
    print("\nElementi domene dom2:")
    print(dom2)
    print("Kardinalitet domene je:", dom2.get_cardinality())

    dom3 = CompositeDomain(dom1, dom2)
    print("\nElementi domene dom3:")
    print(dom3)
    print("Kardinalitet domene je:", dom3.get_cardinality())
    # print(dom3.get_number_of_components())
    # print(dom3.get_component(1))
    print(dom3.element_for_index(0))
    print(dom3.element_for_index(5))
    print(dom3.element_for_index(14))
    print(dom3.index_of_element((4, 1)))


if __name__ == '__main__':
    main()
