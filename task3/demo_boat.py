import boat_control as bc
import sys
from fuzzy import MutableFuzzySet, Debug


class InputError(Exception):
    pass


def main():

    defuzzifier = bc.COADefuzzifier()
    fs_acc = bc.AcceleratorFuzzySystem(defuzzifier)
    fs_rudder = bc.RudderFuzzySystem(defuzzifier)

    while True:
        line_in = input()   # L, D, LK, DK, V, S - integeri
        if line_in == "KRAJ":
            break
        try:
            values = [int(value) for value in line_in.split(" ")]
        except ValueError:
            raise InputError("Please input 6 integers divided by space.")

        acceleration = int(fs_acc.deduce(values))
        angle = int(fs_rudder.deduce(values))

        # print(values[0], values[1], values[2], values[3], values[4], values[5], file=sys.stderr)
        # print(acceleration, angle, file=sys.stderr)
        print(acceleration, angle, flush=True)


if __name__ == '__main__':
    main()
