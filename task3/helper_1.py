import boat_control as bc
from fuzzy import Debug


def main():
    defuzzifier = bc.COADefuzzifier()
    fsystem = bc.AcceleratorFuzzySystem(defuzzifier)
    # fsystem = bc.RudderFuzzySystem(defuzzifier)

    index = int(input("Unesi broj pravila: "))

    rule = fsystem.rules[index]

    print("Unesi L, D, LK, DK, V, S odvojene razmacima")
    values = [int(value) for value in input().split()]

    new_set = rule.apply(values)
    value = defuzzifier.defuzzify(new_set)

    print("SET:")
    Debug.print(new_set, "PRAVILO")
    print("VRIJEDNOST: ", value)


if __name__ == '__main__':
    main()
