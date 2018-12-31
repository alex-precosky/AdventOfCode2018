"""Advent of Code 2018: Day 9"""
import copy
import re


class Particle:
    def __init__(self, p0, v):
        self.p = p0
        self.v = v

    def __repr__(self):
        return f'{self.p} {self.v}'

    @classmethod
    def from_string(self, input_str):
        match = re.search(r'(?<=position=<)[- ]+\d+(?=,)', input_str)
        p0x = int(match.group(0))

        match = re.search(r'(?<=, )[- ]\d+(?=>)', input_str)
        p0y = int(match.group(0))

        match = re.search(r'(?<=velocity=<)[- ]+\d+(?=,)', input_str)
        vx = int(match.group(0))

        match = re.search(r'[- ]+\d+(?=>$)', input_str)
        vy = int(match.group(0))

        return Particle([p0x, p0y], [vx, vy])

    def __eq__(self, other):
        return(self.p == other.p and self.v == other.v)


class MessageCloud:
    def __init__(self, particles):
        self.particles = copy.deepcopy(particles)

    def step(self):
        for i in range(len(self.particles)):
            particle = self.particles[i]

            particle.p[0] += particle.v[0]
            particle.p[1] += particle.v[1]

            self.particles[i] = particle

    def get_x_range(self):
        x_min = 99999999
        x_max = -99999999

        for particle in self.particles:
            if particle.p[0] < x_min:
                x_min = particle.p[0]

            if particle.p[0] > x_max:
                x_max = particle.p[0]

        return x_max - x_min

    def __repr__(self):
        return_str = ""

        x_min = 99999999
        x_max = -99999999
        y_min = 99999999
        y_max = -99999999

        for particle in self.particles:
            if particle.p[0] < x_min:
                x_min = particle.p[0]

            if particle.p[0] > x_max:
                x_max = particle.p[0]

            if particle.p[1] > y_max:
                y_max = particle.p[1]

            if particle.p[1] < y_min:
                y_min = particle.p[1]

        x_offset = -x_min
        y_offset = -y_min

        for j in range(y_min, y_max + 1):
            for i in range(x_min, x_max + 1):
                mark = False
                for particle in self.particles:
                    particle_x = (particle.p[0])
                    particle_y = (particle.p[1])

                    if particle_x == i and particle_y == j:
                        mark = True
                if mark:
                    return_str += "#"
                else:
                    return_str += "."
            return_str += "\n"

        return return_str


def main():
    particles = []
    for line in open('input/day10.txt').readlines():
        particle = Particle.from_string(line)
        particles.append(particle)

    message_cloud = MessageCloud(particles)

    # Keep stepping until the X range is at its minimum
    prev_x_range = 9999999
    i = 0
    while True:
        message_cloud.step()
        x_range = message_cloud.get_x_range()
        if x_range > prev_x_range:
            break
        prev_x_range = x_range
        i += 1

    # Finding the time the message appears requires stepping one step too far
    # Redo the stepping just to the point required
    message_cloud = MessageCloud(particles)
    for j in range(i):
        message_cloud.step()

    print(message_cloud)

    print(f'The message appeared after {i} minutes')

if __name__ == "__main__":
    main()
