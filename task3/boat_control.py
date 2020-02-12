from abc import ABC, abstractmethod
from operations import Operations
from constants import *
from fuzzy import Debug


class COADefuzzifier(object):

    def defuzzify(self, fset):
        a, b = 0, 0
        for elem in fset.get_domain():
            a += elem * fset.get_value_at(elem)
            b += fset.get_value_at(elem)
        if abs(b) < 1e-9:
            return 0
        return a / b


class Rule(ABC):

    def __init__(self, antecedents, consequent):
        self.antecedents = antecedents
        self.consequent = consequent

    def apply(self, values):
        mi = 1
        for i in range(len(self.antecedents)):
            if self.antecedents[i] is not None:
                # mi *= self.antecedents[i].get_value_at(values[i])
                mi = min(mi, self.antecedents[i].get_value_at(values[i]))

        return self.consequent.cutoff(mi)


class FuzzySystem(ABC):

    def __init__(self, defuzzifier):
        self.defuzzifier = defuzzifier
        self.rules = []

    def deduce(self, values, defuz=True):
        consequences = [rule.apply(values) for rule in self.rules]
        union = consequences[0]
        for i in range(1, len(consequences)):
            union = Operations.binary_operation(union, consequences[i], Operations.zadeh_or())

        return self.defuzzifier.defuzzify(union) if defuz else union

    def add_rules(self, rules):
        self.rules.extend(rules)


class AcceleratorFuzzySystem(FuzzySystem):

    def __init__(self, defuzzifier):
        super(AcceleratorFuzzySystem, self).__init__(defuzzifier)

        too_slow = Rule([None, None, None, None, TOO_SLOW, None], SPEED_UP)
        too_fast = Rule([None, None, None, None, TOO_FAST, None], SLOW_DOWN)
        speed_up = Rule([FAR, FAR, FAR, FAR, None, None], SPEED_UP)
        self.add_rules([too_slow, too_fast, speed_up])


class RudderFuzzySystem(FuzzySystem):

    def __init__(self, defuzzifier):
        super(RudderFuzzySystem, self).__init__(defuzzifier)

        turn_r = Rule([None, None, CLOSE, None, None, None], TURN_RIGHT)
        turn_l = Rule([None, None, None, CLOSE, None, None], TURN_LEFT)
        wrong_way = Rule([None, None, None, None, None, WRONG_WAY], TURN_LEFT)
        self.add_rules([wrong_way, turn_r, turn_l])
