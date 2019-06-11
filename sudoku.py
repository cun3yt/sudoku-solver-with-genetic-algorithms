""" Genetic Algoritms Solver for a Given Sudoku State.

ps. Since Genetic Algoritms are randomized algorithm getting stuck
to a local minimum is a possiblity

run like this: `bash$ python3 sudoku.py`
"""

from itertools import accumulate
from random import randint, shuffle, sample
from operator import attrgetter


class Encoding:
    "f1,_2,_3,_4,_5,_6,_7,_8,_9xf1,_2,_3,_4,_5,_6,_7,_8,_9"
    def __init__(self, coding):
        self.coding = coding
        self.fitness()

    def fitness(self):
        # "f1,_2,_3,_4,_5,_6,_7,_8,_9xf1,_2,_3,_4,_5,_6,_7,_8,_9"
        groups = self.coding.split('x')
        # ["f1,_2,_3,_4,_5,_6,_7,_8,_9", "f1,_2,_3,_4,_5,_6,_7,_8,_9", ...]
        groups = [g[1::3] for g in groups]
        # ["123456789", "123456789", ...]

        # row sets
        rows = []

        rows.append(set(list(groups[0][:3]) + list(groups[1][:3]) + list(groups[2][:3])))
        rows.append(set(list(groups[0][3:6]) + list(groups[1][3:6]) + list(groups[2][3:6])))
        rows.append(set(list(groups[0][6:9]) + list(groups[1][6:9]) + list(groups[2][6:9])))

        rows.append(set(list(groups[3][:3]) + list(groups[4][:3]) + list(groups[5][:3])))
        rows.append(set(list(groups[3][3:6]) + list(groups[4][3:6]) + list(groups[5][3:6])))
        rows.append(set(list(groups[3][6:9]) + list(groups[4][6:9]) + list(groups[5][6:9])))

        rows.append(set(list(groups[6][:3]) + list(groups[7][:3]) + list(groups[8][:3])))
        rows.append(set(list(groups[6][3:6]) + list(groups[7][3:6]) + list(groups[8][3:6])))
        rows.append(set(list(groups[6][6:9]) + list(groups[7][6:9]) + list(groups[8][6:9])))

        # col sets
        cols = []

        cols.append(set(list(groups[0][::3]) + list(groups[3][::3]) + list(groups[6][::3])))
        cols.append(set(list(groups[0][1::3]) + list(groups[3][1::3]) + list(groups[6][1::3])))
        cols.append(set(list(groups[0][2::3]) + list(groups[3][2::3]) + list(groups[6][2::3])))

        cols.append(set(list(groups[1][::3]) + list(groups[4][::3]) + list(groups[7][::3])))
        cols.append(set(list(groups[1][1::3]) + list(groups[4][1::3]) + list(groups[7][1::3])))
        cols.append(set(list(groups[1][2::3]) + list(groups[4][2::3]) + list(groups[7][2::3])))

        cols.append(set(list(groups[2][::3]) + list(groups[5][::3]) + list(groups[8][::3])))
        cols.append(set(list(groups[2][1::3]) + list(groups[5][1::3]) + list(groups[8][1::3])))
        cols.append(set(list(groups[2][2::3]) + list(groups[5][2::3]) + list(groups[8][2::3])))

        row_total = list(accumulate([(9 - len(row)) for row in rows]))[-1]
        col_total = list(accumulate([(9 - len(col)) for col in cols]))[-1]

        self.f = row_total + col_total
        return self.f

    def cross(self, encoding2):
        groups = []
        groups.append(self.coding.split('x'))
        groups.append(encoding2.coding.split('x'))
        group = [groups[randint(0,1)][i] for i in range(0, 9)]
        return Encoding('x'.join(group))

    def mutate(self):
        groups = self.coding.split('x')
        i = randint(0, 8)

        indices = [index for index, value in enumerate(groups[i]) if value == '_']
        if len(indices) < 2:
            return
        index1, index2 = [(index + 1) for index in sample(indices, 2)]

        group_list = list(groups[i])
        group_list[index1], group_list[index2] = group_list[index2], group_list[index1]
        groups[i] = ''.join(group_list)

        self.coding = 'x'.join(groups)
        self.fitness()

    def __str__(self):
        return self.coding


def generate_block(block):
    # block: 'f1,_6,__,__,__,__,__,__,f5'
    # returns 'f1,_6,_3,_4,_2,_7,_8,_9,f5'

    nums = [str(num) for num in range(1,10)]
    reserved_nums = set(int(num) for num in block[1::3] if num in nums)
    remaining_nums = list(set(range(1,10)) - reserved_nums)

    shuffle(remaining_nums)

    block = list(block)
    block_len = len(block)

    i = 1
    while len(remaining_nums) > 0 and (i < block_len):
        if block[i] not in nums:
            block[i] = remaining_nums.pop()
        i += 3
    return ''.join([str(item) for item in block])


def generate_encoding(block_sequence):
    # block_sequence: 'f1,_6,__,__,__,__,__,__,f5xf9,_2,__,__,__,__,__,__,f3x...'
    # return: Encoding
    blocks = block_sequence.split('x')
    coding = 'x'.join([generate_block(block) for block in blocks])

    return Encoding(coding)


if __name__ == "__main__":
    coding = ("f1,f5,f7,f2,__,f4,f3,__,__x"
              "f6,f4,__,f3,f7,f5,__,f2,f1x"
              "f3,__,f2,__,f1,__,f4,__,__x"
              "__,f1,__,f7,f6,f3,__,__,__x"
              "__,f9,f6,__,f1,__,__,f3,f7x"
              "f7,f3,f8,__,f4,f9,f6,__,f1x"
              "f6,f7,__,f8,f3,f1,__,__,__x"
              "f1,__,f3,__,f6,__,f7,__,__x"
              "__,__,__,__,__,__,f1,f6,f3")

    population_size = 2500
    next_gen_size = 100
    mutation_percentage = 10

    population = []

    for i in range(1, population_size):
        e = generate_encoding(coding)
        population.append(e)

    population = sorted(population, key=attrgetter('f'))
    population = population[:next_gen_size]

    print('gen-0: best 3: %s %s %s' % (population[0].f, population[1].f, population[2].f))

    for gen_id in range(1, 200):
        for i in range(0, 6500):
            e1, e2 = sample(population, 2)
            if str(e1) == str(e2):
                print("the same")
                e2.mutate()
                population.append(e2)

            for j in range(0, 5):
                new_e = e1.cross(e2)
                if randint(0, 100) < mutation_percentage:
                    new_e.mutate()
                population.append(new_e)

        for i in range(0, 200):
            e = generate_encoding(coding)
            population.append(e)

        print("Before: %s" % len(population))

        population = list({ind.coding for ind in population})
        population = [Encoding(ind) for ind in population]

        print("After: %s" % len(population))

        population = sorted(population, key=attrgetter('f'))

        population = population[:next_gen_size]

        print('gen-%s: best 3: %s %s %s' % (gen_id, population[0].f, population[1].f, population[-1].f))

        if population[0].f == 0:
            print("Solution found: ")
            print(population[0])
            exit(0)

        print(population[0])
        print('----')
