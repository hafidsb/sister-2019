import random


class ServiceModel(object):
    def __init__(self):
        pass

    def get_greet(self, name="<empty>"):
        lucky_number = random.randint(1, 100)
        return "Hello {}! Your lucky number is {}".format(name, lucky_number)

if __name__ == '__main__':
    k = ServiceModel()
    print(k.get_greet("test from client"))
