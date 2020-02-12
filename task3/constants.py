from fuzzy import CalculatedFuzzySet, StandardFuzzySets, Debug
from domain import SimpleDomain


ANGLE_DOMAIN = SimpleDomain(-90, 91)
DISTANCE_DOMAIN = SimpleDomain(0, 1301)
VELOCITY_DOMAIN = SimpleDomain(0, 101)
ACCELERATION_DOMAIN = SimpleDomain(-50, 51)


TURN_LEFT = CalculatedFuzzySet(ANGLE_DOMAIN, StandardFuzzySets.gamma_function(150, 180))
TURN_RIGHT = CalculatedFuzzySet(ANGLE_DOMAIN, StandardFuzzySets.l_function(0, 30))

CLOSE = CalculatedFuzzySet(DISTANCE_DOMAIN, StandardFuzzySets.l_function(40, 60))
FAR = CalculatedFuzzySet(DISTANCE_DOMAIN, StandardFuzzySets.gamma_function(60, 75))

WRONG_WAY = CalculatedFuzzySet(DISTANCE_DOMAIN, StandardFuzzySets.l_function(0, 1))

TOO_FAST = CalculatedFuzzySet(VELOCITY_DOMAIN, StandardFuzzySets.gamma_function(60, 70))
TOO_SLOW = CalculatedFuzzySet(VELOCITY_DOMAIN, StandardFuzzySets.l_function(25, 50))

SPEED_UP = CalculatedFuzzySet(ACCELERATION_DOMAIN, StandardFuzzySets.lambda_function(55, 60, 65))
SLOW_DOWN = CalculatedFuzzySet(ACCELERATION_DOMAIN, StandardFuzzySets.l_function(40, 50))


if __name__ == '__main__':
    Debug.print(CLOSE)
    Debug.print(FAR)
