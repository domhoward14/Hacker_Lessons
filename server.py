import socket, threading

bind_ip = "0.0.0.0"
bind_port = 9001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print (" -> listening on %s:%d" % (bind_ip, bind_port))

def process_client(client_connection):

    request = client_connection.recv(1024)
    print (" -> received '%s'" % (request.decode()))
    client_connection.send("Message received sucessfully".encode())
    client_connection.close()

while True:

    print ("Multi-threaded server enabled")
    client, addr = server.accept()
    print (" -> Accepted Connection from: %s:%d" % (addr[0], addr[1]))
    client_processor = threading.Thread(target = process_client, args=((client,)))
    client_processor.start()
