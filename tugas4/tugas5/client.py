import Pyro4
import base64
import json
import sys

if len(sys.argv) > 1: 
    nama_instance = sys.argv[1] 
else:
    nama_instance = "fileserver"

def get_fileserver_object():
    uri = "PYRONAME:{}@localhost:7777" . format(nama_instance)
    fserver = Pyro4.Proxy(uri)
    fserver.set_name(nama_instance)
    fserver.set_pyro_server()
    return fserver

if __name__=='__main__':
    # f = get_fileserver_object()
    # f.create('slide1.pdf')
    # f.update('slide1.pdf', content = open('slide1.pdf','rb+').read() )

    # f.create('slide2.pptx')
    # f.update('slide2.pptx', content = open('slide2.pptx','rb+').read())

    # print(f.list())
    # d = f.read('slide1.pdf')
    # #kembalikan ke bentuk semula ke dalam file name slide1-kembali.pdf
    # open('slide1-kembali.pdf','w+b').write(base64.b64decode(d['data']))

    # k = f.read('slide2.pptx')
    # #kembalikan ke bentuk semula ke dalam file name slide2-kembali.pptx
    # open('slide2-kembali.pptx','w+b').write(base64.b64decode(k['data']))

    s = get_fileserver_object()
    connected = True

    while connected:
        client_input = input()
        split = client_input.split(" ")

        if split[0] == "list":
            print(s.list())
        elif split[0] == "pyro":
            s.get_pyro_server()
        elif split[0] == "exit":
            print("disconnected from server")
            print(s.get_name())
            # connected = False
        elif len(split) == 2:            
            if split[0] == "create":
                print(s.create(split[1]))
            elif split[0] == "read":
                print(s.read(split[1]))
            elif split[0] == "delete":
                print(s.delete(split[1]))
            else:
                print("command is not found.")
        elif len(split) > 2:
            if split[0] == "update":
                print(s.update(split[1], split[2]))
            else:
                print("command is not found")
        else:
            print("command is not found")