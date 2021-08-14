import random
import uuid


def get_int(x):
    return random.randint(1, x)


def get_email():
    a = ['sdasdads', '2e2e2e2e', 'dfrfrgrg', '3d232d23d23', '24r34r343r34r']
    temp = random.choice(a) + '@' + random.choice(a) + '.com'
    return temp


def get_uid():
    return str(uuid.uuid4())


class FirstNameGen(object):

    def __init__(self):
        self.names = []
        with open('names.txt') as names:
            for r in names:
                temp = r.split('</li>')[0][4:]
                self.names.append(temp)

    def get_name(self):
        n = random.choice(self.names)
        return n
