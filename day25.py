class Point:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_str(self, input_str):
        components = input_str.split(',')
        w = int(components[0])
        x = int(components[1])
        y = int(components[2])
        z = int(components[3])

        return Point(w, x, y, z)


def get_manhattan_distance(p1, p2):
    return abs(p2.w-p1.w) + abs(p2.x-p1.x) + abs(p2.y-p1.y) + abs(p2.z-p1.z)


class Constallation:
    def __init__(self):
        self.points = []

    def add_point(self, pt):
        self.points.append(pt)

    def does_contain_point(self, pt):
        for c_point in self.points:
            if get_manhattan_distance(pt, c_point) <= 3:
                return True


def main():
    num_points = 0
    constallations = []
    for line in open('input/Day25.txt').readlines():
        num_points += 1
        point = Point.from_str(line.strip())

        matching_constallations = []

        #  build a list of constallations this point could belong to
        for constallation in constallations:
            if constallation.does_contain_point(point) is True:
                matching_constallations.append(constallation)

        if len(matching_constallations) == 0:
            # make a new constallation
            new_constallation = Constallation()
            new_constallation.add_point(point)
            constallations.append(new_constallation)
        elif len(matching_constallations) == 1:
            # add to existing constallation
            matching_constallations[0].add_point(point)
        else:
            # add to an existing constallation then merge the constallations it
            # joins
            matching_constallations[0].add_point(point)
            for constallation in matching_constallations[1:]:
                for point in constallation.points:
                    matching_constallations[0].add_point(point)
                constallations.remove(constallation)

    num_constllations = len(constallations)

    print(f'There are {num_constllations} constallations out of {num_points} points')

if __name__ == "__main__":
    main()
