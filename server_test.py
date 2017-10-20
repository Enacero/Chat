import tcp_server
import socket
import time
import threading


def test_game_server_starts_tcp_server():

    server_thread = threading.Thread(target=tcp_server.chat_server)
    server_thread.start()

    time.sleep(0.00001)

    # This is our fake test client that is just going to attempt a connect and disconnect
    for i in range(10):
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect(('127.0.0.1', 49001))
        fake_client.close()

    # Make sure server thread finishes
    del server_thread
if __name__ == '__main__':
    test_game_server_starts_tcp_server()