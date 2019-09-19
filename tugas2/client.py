import Pyro4
import time
import threading
import serpent


def connect():
    uri = "PYRONAME:myserver@localhost:7777"
    server = Pyro4.Proxy(uri)
    print(server.get_greet("myself"))
    return server, uri


def menu():
    print("List of available services(with keyword for using it):")
    print("1. Create a text file on your current lucky number folder(file_create <filename>)")
    print("2. Print contents of your current lucky number storage(file_list)")
    print("3. Delete a text file on your current lucky number folder(file_delete <filename>)")
    print("4. Change your lucky number(ln_change <number>)")
    print("4. Print your current lucky number(ln_print)")
    print("8. Print services list(help)")
    print("9. Exit program(exit)")


def regular_pyro(uri):
    blobsize = 10 * 1024 * 1024
    num_blobs = 10
    total_size = 0
    start = time.time()
    name = threading.currentThread().name
    with Pyro4.core.Proxy(uri) as p:
        for _ in range(num_blobs):
            print("thread {0} getting a blob using regular Pyro call...".format(name))
            data = p.get_file(blobsize)
            data = serpent.tobytes(data)  # in case of serpent encoded bytes
            total_size += len(data)
    assert total_size == blobsize * num_blobs
    duration = time.time() - start
    print("thread {0} done, {1:.2f} Mb/sec.".format(name, total_size / 1024.0 / 1024.0 / duration))


if __name__ == '__main__':
    # print("\n\n**** regular pyro calls ****\n")
    # t1 = threading.Thread(target=regular_pyro, args=(u,))
    # t2 = threading.Thread(target=regular_pyro, args=(u,))
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    # input("enter to exit:")

    s, u = connect()
    is_connected = True
    menu()
    while is_connected:
        user_request = input("\n>> ").lower()
        if len(user_request.split()) > 1:
            if user_request.split()[0] == 'file_create':
                print(s.create_file(" ".join(user_request.split()[1:]) + ".txt"))
            elif user_request.split()[0] == 'file_delete':
                print(s.delete_file(" ".join(user_request.split()[1:]) + ".txt"))
            elif user_request.split()[0] == 'ln_change':
                try:
                    new_lucky_number = int(user_request.split()[1])
                    s.set_lucky_number(new_lucky_number)
                    print("Your lucky number now is {0}".format(new_lucky_number))
                except ValueError as e:
                    print("Error changing lucky number. Value must be integer!")
        elif user_request == 'ln_print':
            print(s.get_lucky_number())
        elif user_request == 'file_list':
            temp_contents = s.list_file()
            for file_name in temp_contents:
                print("- {}".format(file_name))
        elif user_request == 'help':
            menu()
        elif user_request == 'exit':
            is_connected = False
            print("Good bye!")
        else:
            print("Keyword not exist or wrong keyword usage. Enter 'help' for list of services")

    # s.create_file("funny.txt")
