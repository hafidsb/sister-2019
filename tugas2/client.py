import Pyro4
import time
import threading
import serpent


def connect(name):
    uri = "PYRONAME:myserver@10.151.30.145:7777"
    server = Pyro4.Proxy(uri)
    print(server.connect(name))
    return server, uri


def menu():
    print("List of available services(with keyword for using it):")
    print("1. Create a text file on your current lucky number folder(file_create <filename>)")
    print("2. Print contents of your current lucky number storage(file_list)")
    print("3. Print content of selected file(file_read <filename>")
    print("4. Edit content of selected file(file_edit <filename>")
    print("5. Delete a text file on your current lucky number folder(file_delete <filename>)")
    print("6. Change your lucky number(ln_change <number>)")
    print("7. Print your current lucky number(ln_print)")
    print("8. Print services list(help)")
    print("9. Exit program(exit)")


if __name__ == '__main__':
    name = input(">> input name: ")
    s, u = connect(name)
    is_connected = True
    menu()
    while is_connected:
        user_request = input("\n>> input: ").lower()
        if len(user_request.split()) > 1:
            if user_request.split()[0] == 'file_create':
                print(s.create_file(" ".join(user_request.split()[1:]) + ".txt"))
            elif user_request.split()[0] == 'file_read':
                read = s.read_file(" ".join(user_request.split()[1:]) + ".txt")
                if read == False:
                    print("File " + " ".join(user_request.split()[1:]) + ".txt not found")
                else:
                    print("\"" + read + "\"")
            elif user_request.split()[0] == 'file_edit':
                edit = s.read_file(" ".join(user_request.split()[1:]) + ".txt")
                if edit == False:
                    print("File " + " ".join(user_request.split()[1:]) + ".txt not found")
                    continue
                else:
                    print("Current file content: \"" + edit + "\"")
                change_mode = input("Content change(choose): \n 1. Append file\n 2. Rewrite file entirely\n\n>> choice:")
                if change_mode == '1':
                    mode = 'a'
                    change_content = input(">> content append: ")
                elif change_mode == '2':
                    mode = 'w'
                    change_content = input(">> content overwrite: ")
                else:
                    print("Change mode invalid")
                    continue
                if edit == "":
                    mode = 'w'
                print("New file content: \"" + s.edit_file(" ".join(user_request.split()[1:]) + ".txt", change_content, mode) + "\"")
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
            if temp_contents == []:
                print("Folder is empty")
                continue
            for file_name in temp_contents:
                print("- {}".format(file_name))
        elif user_request == 'help':
            menu()
        elif user_request == 'exit':
            is_connected = False
            print("Good bye " + name + "!")
        else:
            print("Keyword not exist or wrong keyword usage. Enter 'help' for list of services")
