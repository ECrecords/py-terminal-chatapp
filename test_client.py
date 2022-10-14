import socket


def main():

    HOST = "192.168.0.187"
    PORT = 4545

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

main()
