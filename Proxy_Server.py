import socket
import threading

PORT = 8888
def handle_client(client_socket):
    request = client_socket.recv(4096)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('127.0.0.1', 8000))  # Change to the desired destination server

    server_socket.send(request)
    print(f'Client request sent to original server')
    response = server_socket.recv(4096)
    client_socket.send(response)
    print(f'response sent back to client')
    client_socket.close()
    server_socket.close()


def run_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', PORT))  # Proxy server listens on localhost, port 8888
    server.listen(5)

    print(f'Proxy server is running on port {PORT}...')

    while True:
        client_socket, addr = server.accept()
        print(f'Request from {addr} accepted')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    run_proxy()
