import random
import os
import errno


class ServiceModel(object):
    def __init__(self, lucky_number=None):
        self.lucky_number = 0

    def set_lucky_number(self, number):
        self.lucky_number = number

    def get_lucky_number(self):
        return self.lucky_number

    def get_greet(self, name="<empty>"):
        self.lucky_number = random.randint(1, 1000)
        return "Hello {}! Your lucky number is {}\n".format(name, self.lucky_number)

    def get_file(self, size):
        print("sending %d bytes" % size)
        data = b"x" * size
        return data

    def create_file(self, file_name):
        path = "file_storage/%d" % self.lucky_number
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        f = open(path + '/' + file_name, 'w')
        # f.write("Test from %d" % self.lucky_number)
        f.close()
        return "File %s has been created successfully" % file_name

    def read_file(self, file_name):
        path = "file_storage/%d/%s" % (self.lucky_number, file_name)
        f = open(path, 'r')
        return f.read()

    def edit_file(self, file_name):
        pass

    def list_file(self):
        path = "file_storage/%d" % self.lucky_number
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

        return os.listdir(path)

    def delete_file(self, file_name):
        path = "file_storage/%d/%s" % (self.lucky_number, file_name)
        try:
            os.remove(path)
            return "File %s has been deleted successfully" % file_name
        except FileNotFoundError:
            return "File %s not found." % file_name


if __name__ == '__main__':
    k = ServiceModel()
    print(k.get_greet("test from model"))
