from domain import Domain
from fuzzy import MutableFuzzySet, Debug


class DomainsDimensionError(Exception):
    pass


class Relations(object):

    @staticmethod
    def is_u_times_u_relation(fset):
        dom = fset.get_domain()
        if dom.get_number_of_components() != 2:
            return False
        dom1, dom2 = dom.get_component(0), dom.get_component(1)
        if dom1.get_cardinality() != dom2.get_cardinality():
            return False

        for i in range(dom1.get_cardinality()):
            if dom1.element_for_index(i) != dom2.element_for_index(i):
                return False
        return True

    @staticmethod
    def is_symmetric(fset):
        if not Relations.is_u_times_u_relation(fset):
            return False
        for elem in fset.get_domain():
            if fset.get_value_at(elem) != fset.get_value_at(elem[::-1]):
                return False
        return True

    @staticmethod
    def is_reflexive(fset):
        if not Relations.is_u_times_u_relation(fset):
            return False
        dom = fset.get_domain()
        step = 0
        for i in range(dom.get_component(0).get_cardinality()):
            if fset.get_value_at(dom.element_for_index(i+step)) != 1:
                return False
            step += dom.get_component(0).get_cardinality()
        return True

    @staticmethod
    def is_max_min_transitive(fset):
        if not Relations.is_u_times_u_relation(fset):
            return False
        dom = fset.get_domain()
        size = dom.get_component(0).get_cardinality()

        rows = [[fset.get_value_at(dom.element_for_index(j + i*size)) for j in range(size)] for i in range(size)]
        columns = list(map(list, zip(*rows)))

        fset2 = MutableFuzzySet(dom)
        for i, elem in enumerate(dom):
            mins = [min(x, y) for x, y in zip(rows[i//size], columns[i%size])]
            fset2.set(elem, max(mins))
        for i in range(dom.get_cardinality()):
            if fset2.get_value_at(dom.element_for_index(i)) > fset.get_value_at(dom.element_for_index(i)):
                return False
        return True

    @staticmethod
    def composition_of_binary_relations(r1, r2):
        dom1 = r1.get_domain()
        dom2 = r2.get_domain()
        size1_x = dom1.get_component(0).get_cardinality()
        size1_y = dom1.get_component(1).get_cardinality()
        size2_x = dom2.get_component(0).get_cardinality()
        size2_y = dom2.get_component(1).get_cardinality()
        if size1_x != size2_y:
            raise DomainsDimensionError("Invalid domain dimensions for composition.")
        rows = [[r1.get_value_at(dom1.element_for_index(j + i*size1_y)) for j in range(size1_y)] for i in range(size1_x)]
        columns = [[r2.get_value_at(dom2.element_for_index(i + j*size2_y)) for j in range(size2_x)] for i in range(size2_y)]

        new_domain = Domain.combine(dom1.get_component(0), dom2.get_component(1))
        new_fset = MutableFuzzySet(new_domain)
        for i, elem in enumerate(new_domain):
            mins = [min(x, y) for x, y in zip(rows[i//size1_x], columns[i%size2_y])]
            new_fset.set(elem, max(mins))
        return new_fset

    @staticmethod
    def is_fuzzy_equivalence(fset):
        if Relations.is_reflexive(fset) and Relations.is_symmetric(fset) and Relations.is_max_min_transitive(fset):
            return True
        return False


def main():
    u = Domain.int_range(1, 6)
    u2 = Domain.combine(u, u)

    r1 = MutableFuzzySet(u2)
    r1.set((1, 1), 1)
    r1.set((2, 2), 1)
    r1.set((3, 3), 1)
    r1.set((4, 4), 1)
    r1.set((5, 5), 1)
    r1.set((3, 1), 0.5)
    r1.set((1, 3), 0.5)

    r2 = MutableFuzzySet(u2)
    r2.set((1, 1), 1)
    r2.set((2, 2), 1)
    r2.set((3, 3), 1)
    r2.set((4, 4), 1)
    r2.set((5, 5), 1)
    r2.set((3, 1), 0.5)
    r2.set((1, 3), 0.1)

    r3 = MutableFuzzySet(u2)
    r3.set((1, 1), 1)
    r3.set((2, 2), 1)
    r3.set((3, 3), 0.3)
    r3.set((4, 4), 1)
    r3.set((5, 5), 1)
    r3.set((1, 2), 0.6)
    r3.set((2, 1), 0.6)
    r3.set((2, 3), 0.7)
    r3.set((3, 2), 0.7)
    r3.set((3, 1), 0.5)
    r3.set((1, 3), 0.5)

    r4 = MutableFuzzySet(u2)
    r4.set((1, 1), 1)
    r4.set((2, 2), 1)
    r4.set((3, 3), 1)
    r4.set((4, 4), 1)
    r4.set((5, 5), 1)
    r4.set((1, 2), 0.4)
    r4.set((2, 1), 0.4)
    r4.set((2, 3), 0.5)
    r4.set((3, 2), 0.5)
    r4.set((3, 1), 0.4)
    r4.set((1, 3), 0.4)

    print("R1:")
    print("UxU:", Relations.is_u_times_u_relation(r1))
    print("Reflexive:", Relations.is_reflexive(r1))
    print("Symmetric:", Relations.is_symmetric(r1))

    print("\nR2:")
    print("UxU:", Relations.is_u_times_u_relation(r2))
    print("Reflexive:", Relations.is_reflexive(r2))
    print("Symmetric:", Relations.is_symmetric(r2))

    print("\nR3:")
    print("UxU:", Relations.is_u_times_u_relation(r3))
    print("Reflexive:", Relations.is_reflexive(r3))
    print("Symmetric:", Relations.is_symmetric(r3))
    print("Max-min transitive:", Relations.is_max_min_transitive(r3))

    print("\nR4:")
    print("UxU:", Relations.is_u_times_u_relation(r4))
    print("Reflexive:", Relations.is_reflexive(r4))
    print("Symmetric:", Relations.is_symmetric(r4))
    print("Max-min transitive:", Relations.is_max_min_transitive(r4))

    u = Domain.int_range(1, 5)

    r = MutableFuzzySet(Domain.combine(u, u))
    r.set((1, 1), 1)
    r.set((2, 2), 1)
    r.set((3, 3), 1)
    r.set((4, 4), 1)
    r.set((1, 2), 0.3)
    r.set((2, 1), 0.3)
    r.set((2, 3), 0.5)
    r.set((3, 2), 0.5)
    r.set((3, 4), 0.2)
    r.set((4, 3), 0.2)

    r2 = r

    print("Početna relacija je neizrazita relacija ekvivalencije?", Relations.is_fuzzy_equivalence(r2))
    print()

    for i in range(3):
        r2 = Relations.composition_of_binary_relations(r2, r)
        print("Broj odrađenih kompozicija:" + str(i+1) + ". Relacija je:")
        Debug.print(r2)
        print("Ova relacija je neizrazita relacija ekvivalencije?")
        print(Relations.is_fuzzy_equivalence(r2))
        print()
    u1 = Domain.int_range(1, 5)
    u2 = Domain.int_range(1, 4)
    u3 = Domain.int_range(1, 5)

    r1 = MutableFuzzySet(Domain.combine(u1, u2))
    r1.set((1, 1), 0.3)
    r1.set((1, 2), 1)
    r1.set((3, 3), 0.5)
    r1.set((4, 3), 0.5)

    r2 = MutableFuzzySet(Domain.combine(u2, u3))
    r2.set((1, 1), 1)
    r2.set((2, 1), 0.5)
    r2.set((2, 2), 0.7)
    r2.set((3, 3), 1)
    r2.set((3, 4), 0.4)

    r1r2 = Relations.composition_of_binary_relations(r1, r2)
    Debug.print(r1r2)


if __name__ == '__main__':
    main()
