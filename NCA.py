import sys, socket, getopt, threading, subprocess, argparse

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 9000

def start_client(target, port):
    address = (target, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    message = input("NCA -> ")
    client.send(message.encode())

    while True:
        response = client.recv(4096)
        print (response.decode())
        message = input("NCA -> ")
        client.send(message.encode())


def run_command(client_connection):
    while True:
        try:
            user_input = client_connection.recv(4096)
            output=subprocess.run(user_input, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            client_connection.send(output.encode())
        except:
            exception = "Unexpected error: %s" % sys.exc_info()[0]
            client_connection.send(exception.encode())
            print("Unexpected error: %s" % sys.exc_info()[0])

def process_client(client_connection):
    if(upload):
        run_upload(user_input)

    else:
        run_command(client_connection)


def run_server(bind_ip, bind_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)

    print (" -> listening on %s:%d" % (bind_ip, bind_port))

    while True:
        print ("Multi-threaded server enabled")
        client, addr = server.accept()
        print (" -> Accepted Connection from: %s:%d" % (addr[0], addr[1]))
        client_processor = threading.Thread(target = process_client, args=((client,)))
        client_processor.start()

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    try:
        parser = argparse.ArgumentParser(description='Netcat Alternative Tool')

        parser.add_argument('-l', '--listen', dest='listen', action='store_true', help='Enables port listening, and defaults to port 9000 if -p option is not used')
        parser.add_argument('-e', '--execute', dest='execute', help='file to execute on the remote server')
        parser.add_argument('-c', '--command', dest='command', action='store_true', help='command to execute on the remote server')
        parser.add_argument('-u', '--upload', dest='upload_destination', action='store_true', help='location to upload on the target system')
        parser.add_argument('-t', '--target', dest='target', help='address of the target system')
        parser.add_argument('-p', '--port', dest='port', help='set the port of the target system', type=int)

        args = parser.parse_args()
        #listening functionality
        if(args.listen):
            #check that there is address provided
            if not(args.target):
                target = input("Target address was not provided. Please input IP address or domain name.").encode()

            run_server(args.target, args.port)

        elif(args.command):
            if not(args.target):
                args.target = input("Target address was not provided. Please input IP address or domain name.").encode()

            if not(args.port):
                args.port = input("Port number was not provided. Please input port #.").encode()

            start_client(args.target, args.port)

    except:
        print("Unexpected error:", sys.exc_info()[0])

if __name__ == "__main__":
    main()
