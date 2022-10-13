from atexit import unregister
from collections import namedtuple
import socket
import selectors
import sys
from typing import Union


Connection = namedtuple('Connection', ['id', 'addr', 'outb'])
id = 0

def menu(selector: selectors.DefaultSelector, connection_list: list) -> Union[selectors.DefaultSelector, list]:

    input = (sys.stdin.readline()).rstrip()

    input = input.split(" ")
    if input[0] == "help":
        help()
    elif input[0] == "myip":
        get_ip()
    elif input[0] == "myport":
        get_port()
    elif input[0] == "connect":
        (selector, connection_list) = connect(selector, connection_list, input[1], int(input[2]))
    elif input[0] == "list":
        list_connections(selector, connection_list)
    elif input[0] == "send":
        send_message(selector, int(input[1]), input[2:len(input)])
    elif input[0] == "terminate":
        terminate()
    elif input[0] == "exit":
        exit_program()
    else:
        print(  "invalid command: use command "
                "help to display valid commands" )
    
    return selector, connection_list


def help():
    print("myip display IP address\n"
          "connect connect to another peer \n"
          "send send messages to peers\n"
          "………….\nexit exit the program")

def get_ip():
    pass

def get_port():
    pass

def connect(selector: selectors.DefaultSelector, connection_list: list, ip: str, port: int) -> Union[selectors.DefaultSelector, list]:
#    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex((ip, port))
        events = selectors.EVENT_READ

        id = get_id()
        data = Connection(id, ip, "")

        connection_list.append((id, sock))
        selector.register(sock, events, data=data)

        print(f"The connection to peer {ip} is succeessfully established;")
        return selector, connection_list
    # except:
    #     print("The connection to peer was not established;")
    #     return selector, connection_list

def list_connections(selector: selectors.DefaultSelector, connection_list: list):
    print(f"id:\tIP Addresss\tPort")
    for entry in connection_list:
        print(f"{entry[0]}:\t{(selector.get_key(entry[1])).data.addr}\t{None}")

def send_message(selector: selectors.DefaultSelector, conn_id: int, msg: str):
    pass

def terminate():
    pass

def exit_program():
    exit()

def get_id():
    global id
    id += 1
    return id

def accept_wrapper(selector: selectors.DefaultSelector, connection_list: list, sock: socket.socket) -> Union[selectors.DefaultSelector, list]:
    # try:
        conn, addr = sock.accept()
        print(f"The connection to peer {addr[0]} is succeessfully established;")
        conn.setblocking(False)
        events = selectors.EVENT_READ
        id = get_id()
        data = Connection(id, addr[0], "")
        selector.register(conn, events, data=data)
        connection_list.append((id,conn))
        return selector, connection_list
    # except:
    #     print("The connection to peer was not established;")
    #     return selector, connection_list

def receive_msg(selector: selectors.DefaultSelector, connection_list: list, sock: socket.socket, data: any, mask: any) -> Union[selectors.DefaultSelector, list]:
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(recv_data.decode())
            #selector.unregister(sock)

    return selector, connection_list


            

def main():

    if len(sys.argv) != 2:
        print("usage: python3 terminal_chatapp <port number>")
        exit()

    # Grabs port from program arguments
    SEVER_PORT = sys.argv[1]
    conn_list = list()
    sel = selectors.DefaultSelector()

    lsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsocket.bind(("192.168.0.163", int(SEVER_PORT)))
    lsocket.listen()
    lsocket.setblocking(False)

    sel.register(lsocket, selectors.EVENT_READ, data=None)
    sel.register(sys.stdin, selectors.EVENT_READ, data="STDIN")

    while True:

        #print(">>", flush=True, end=" ")
        event = sel.select(timeout=None)

        for key, mask in event:
            
            if key.data == "STDIN":
                (sel, conn_list) = menu(sel,conn_list)
            else:
                if key.data is None:
                    (sel, conn_list) = accept_wrapper(sel, conn_list, key.fileobj)
                else:
                    (sel, conn_list) = receive_msg(sel, conn_list, key.fileobj, key.data, mask)
            

    lsocket.close()


main()
