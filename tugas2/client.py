import Pyro4

def connect():
    uri = "PYRONAME:myserver@localhost:7777"
    server = Pyro4.Proxy(uri)
    print(server.get_greet("myself"))

if __name__ == '__main__':
    connect()