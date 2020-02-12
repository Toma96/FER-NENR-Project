

class Sample:

    def __init__(self, line):
        split_line = line.split()
        self.x = float(split_line[0])
        self.y = float(split_line[1])
        self.a = float(split_line[2])
        self.b = float(split_line[3])
        self.c = float(split_line[4])
        self.class_code = [self.a, self.b, self.c]

    def get_class(self):
        for i, c in enumerate(self.class_code):
            if c == 1:
                return self.class_code[i]


class Dataset:

    def __init__(self, filepath):
        self.samples = []
        with open(filepath, "r") as f:
            for line in f.readlines():
                self.samples.append(Sample(line))


