import socket, sys

target_address = sys.argv[1]
target_port = int(sys.argv[2])
message = sys.argv[3]

def start_client():
    address = (target_address, target_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(address)

    client.send(message.encode())

    response = client.recv(4096)

    print (response.decode())

if __name__ == "__main__":
    start_client()
