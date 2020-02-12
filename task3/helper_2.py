import boat_control as bc
from fuzzy import Debug


def main():
    defuzzifier = bc.COADefuzzifier()
    fsystemacc = bc.AcceleratorFuzzySystem(defuzzifier)
    fsystemrud = bc.RudderFuzzySystem(defuzzifier)

    print("Unesi L, D, LK, DK, V, S odvojene razmacima")
    values = [int(value) for value in input().split()]

    setacc = fsystemacc.deduce(values, defuz=False)
    acc = fsystemacc.deduce(values)
    Debug.print(setacc, "ACCELERATION SET:")
    print("ACCELERATION:", acc)

    setrud = fsystemrud.deduce(values, defuz=False)
    angle = fsystemrud.deduce(values)
    Debug.print(setrud, "RUDDER SET:")
    print("ANGLE:", angle)


if __name__ == '__main__':
    main()
