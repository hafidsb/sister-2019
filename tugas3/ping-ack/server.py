from model import ServiceModel
import Pyro4

def start_server():
    # name server harus di start dulu dengan  pyro4-ns -n localhost -p 7777
    # gunakan URI untuk referensi name server yang akan digunakan
    # untuk mengecek service apa yang ada di ns, gunakan pyro4-nsc -n localhost -p 7777 list

    daemon = Pyro4.Daemon(host="localhost")
    name_server = Pyro4.locateNS("localhost", 7777)
    server = Pyro4.expose(ServiceModel)
    server_uri = daemon.register(server)
    print("server URI: ", server_uri)
    name_server.register("myserver", server_uri)
    daemon.requestLoop()


if __name__ == '__main__':
    start_server()
