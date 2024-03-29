import os
import base64
import Pyro4

class FileServer(object):
    def __init__(self):
        self.name = None
        self.pyro_objects = dict()
        self.pyro_name_list = ["fs-1", "fs-2", "fs-3"]

    def set_pyro_object(self):
        i = 0
        for x in self.pyro_name_list:
            if self.name == x:
                pass
            else:
                self.pyro_objects[i] = Pyro4.Proxy("PYRONAME:{}@localhost:7777" . format(x))
                self.pyro_objects[i].set_name(x)
                i = i + 1

    def get_pyro_objects(self):
        print(self.pyro_objects)

    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

    def create_return_message(self,kode='000',message='kosong',data=None):
        return dict(kode=kode,message=message,data=data)

    def get_list(self):
        print("{}: LIST ops".format(self.name))
        try:
            daftarfile = []
            for x in os.listdir():
                if x[0:4]=='FFF-':
                    daftarfile.append(x[4:])
            return self.create_return_message('200',daftarfile)
        except:
            return self.create_return_message('500','Error')

    def create(self, name='filename000', caller='none'):
        if caller == 'none':
            return self.create_return_message('400', 'OK', 'Bad Request Error')

        if self.name == caller:
            for x in range(0, len(self.pyro_objects)):
                self.pyro_objects[x].create(name, self.name)

        nama='FFF-{}' . format(name)
        print("{}: CREATE ops {} FROM {} instance" . format(self.name, nama, caller))
        try:
            if os.path.exists(nama):
                return self.create_return_message('102', 'OK','File Exists')
            f = open(nama,'wb',buffering=0)
            f.close()
            return self.create_return_message('100','OK')
        except:
            return self.create_return_message('500','Error')

    def read(self,name='filename000'):
        nama='FFF-{}' . format(name)
        print("{}: READ ops {}" . format(self.name, nama))
        try:
            if not os.path.exists(nama):
                return self.create_return_message('404', 'OK','File Not Found')
            f = open(nama,'r+b')
            contents = f.read().decode()
            f.close()
            return self.create_return_message('101','OK',contents)
        except:
            return self.create_return_message('500','Error')
            
    def update(self,name='filename000',content='', caller='none'):
        if caller == 'none':
            return self.create_return_message('400', 'OK', 'Bad Request Error')

        if self.name == caller: 
            for x in range(0, len(self.pyro_objects)):
                self.pyro_objects[x].update(name, content, self.name)

        nama='FFF-{}' . format(name)
        print("{}: UPDATE ops {} FROM {} instance" . format(self.name, nama, caller))

        if (str(type(content))=="<class 'dict'>"):
            content = content['data']
        try:
            if not os.path.exists(nama):
                return self.create_return_message('404', 'OK','File Not Found')
            f = open(nama,'w+b')
            f.write(content.encode())
            f.close()
            return self.create_return_message('101','OK')
        except Exception as e:
            return self.create_return_message('500','Error',str(e))

    def delete(self, name='filename000', caller='none'):
        if caller == 'none':
            return self.create_return_message('400', 'OK', 'Bad Request Error')
        
        if self.name == caller:
            for x in range(0, len(self.pyro_objects)):
                self.pyro_objects[x].delete(name, caller)

        nama='FFF-{}' . format(name)
        print("{}: DELETE ops {} FROM {} instance" . format(self.name, nama, caller))

        try:
            if not os.path.exists(nama):
                return self.create_return_message('404', 'OK','File Not Found')
            os.remove(nama)
            return self.create_return_message('101','OK')
        except:
            return self.create_return_message('500','Error')



if __name__ == '__main__':
    k = FileServer()
    print(k.create('f1'))
    print(k.update('f1',content='wedusku'))
    print(k.read('f1'))
#    print(k.create('f2'))
#    print(k.update('f2',content='wedusmu'))
#    print(k.read('f2'))
    print(k.get_list())
    #print(k.delete('f1'))

