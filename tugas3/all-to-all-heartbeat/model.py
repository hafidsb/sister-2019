import random
import os
import time


class ServiceModel(object):
    def __init__(self, lucky_number=None):
        self.lucky_number = 1

    def set_lucky_number(self, number):
        self.lucky_number = number

    def get_lucky_number(self):
        time.sleep(4.0)
        return self.lucky_number

    def send_heartbeat(self):
        return "OK"

    def connect(self, name="<empty>"):
        # self.lucky_number = random.randint(1, 1000)
        return "\nHello {}! Your lucky number is {}".format(name, self.lucky_number)

    def create_file(self, file_name):
        path = "file_storage/%d" % self.lucky_number
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        f = open(path + '/' + file_name, 'w')
        f.close()
        return "File %s has been created successfully" % file_name

    def read_file(self, file_name):
        path = "file_storage/%d/%s" % (self.lucky_number, file_name)
        try:
            f = open(path, 'r')
        except FileNotFoundError:
            return False
        return f.read()

    def edit_file(self, file_name, content, mode):
        path = "file_storage/%d/%s" % (self.lucky_number, file_name)
        try:
            f = open(path, mode)
            if mode == 'a':
                f.write(" " + content)
            elif mode == 'w':
                f.write(content)
            f.close()
        except FileNotFoundError:
            return False
        return self.read_file(file_name)

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
            return "File %s is not found." % file_name


if __name__ == '__main__':
    k = ServiceModel()
    print(k.connect("test from model"))
