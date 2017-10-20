import sys
import socket
import select


BUFFER_SIZE = 4096
PORT = 49001
SERVER_IP = '0.0.0.0'


def chat_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_IP, PORT))
    server.listen(10)
    sockets = [server]

    print "Chat server started on port " + str(PORT)
    try:
        while True:

            ready_to_read = select.select(sockets, [], [], 0)[0]

            for sock in ready_to_read:
                # a new connection request received
                if sock == server:
                    new_sock, addr = server.accept()
                    sockets.append(new_sock)
                    print "Client ({}, {}) connected".format(addr[0],addr[1])

                    notify(sockets, server, new_sock, '[{}:{}] entered our chatting room\n'.format(addr[0], addr[1]))

                # a message from a client, not a new connection
                else:
                    # process data received from client,
                    try:
                        # receiving data from the socket.
                        data = sock.recv(BUFFER_SIZE)
                        if data:
                            # there is something in the socket
                            notify(server, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                        else:
                            # remove the socket that's broken
                            if sock in sockets:
                                sockets.remove(sock)

                            # at this stage, no data means probably the connection has been broken
                            notify(server, sock, "Client ({}, {}) is offline\n".format(addr[0], addr[1]))

                            # exception
                    except:
                        notify(sockets, server, sock, "Client ({}, {}) is offline\n".format(addr[0], addr[1]))
                        continue
    except KeyboardInterrupt:
        server.close()
        print 'Server shutdown'
        sys.exit(0)


# broadcast chat messages to all connected clients
def notify(sockets, server, sock, message):
    for socket in sockets:
        # send the message only to peer
        if socket != server and socket != sock:
            try:
                socket.send(message)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in sockets:
                    sockets.remove(socket)


if __name__ == "__main__":
    sys.exit(chat_server())