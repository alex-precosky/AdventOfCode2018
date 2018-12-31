"""Advent of Code 2018: Day 9"""
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
        self.particles = particles

        # printing the message is limited to these characters
        self.x_lim = 100
        self.y_lim = 20

    def step(self):
        for i in range(len(self.particles)):
            particle = self.particles[i]

            particle.p[0] += particle.v[0]
            particle.p[1] += particle.v[1]

            self.particles[i] = particle

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

        x_scale = self.x_lim / (x_max-x_min)
        y_scale = self.y_lim / (y_max-y_min)

        for j in range(self.y_lim):
            for i in range(self.x_lim):
                mark = False
                for particle in self.particles:
                    particle_x = (particle.p[0] + x_offset) * x_scale
                    particle_y = (particle.p[1] + y_offset) * y_scale

                    if (particle_x >= i and particle_x <= i+1) and (particle_y >= j and particle_y <= j+1):
                        mark = True
                if mark:
                    return_str += "#"
                else:
                    return_str += "."
            return_str += "\n"

        return_str += f"x_offset: {x_offset} x_scale: {x_scale}"
        return return_str


def main():
    particles = []
    for line in open('input/day10.txt').readlines():
        particle = Particle.from_string(line)
        print(particle)
        particles.append(particle)

    message_cloud = MessageCloud(particles)

    for i in range(10375):
        message_cloud.step()

    print(message_cloud)

if __name__ == "__main__":
    main()
