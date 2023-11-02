import socket
import threading

PORT = 8888
def handle_client(client_socket):
    request = client_socket.recv(4096).decode()
    print(request)
    # Parse the request to extract the host and port
    print('Parsing request...')
    command = request.split('\r\n')[0].split(' ')[0]
    print(f'command: {command}')
    if command == 'GET':
        host = request.split('\r\n')[1].split(' ')[1]
        port = 6789

        print(f'host: {host}  | port: {port}')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, port))

        server_socket.sendall(request.encode())

        response = server_socket.recv(4096)
        while response:
            client_socket.sendall(response)
            response = server_socket.recv(4096)

        client_socket.close()
        server_socket.close()
    else:
        client_socket.close()

    print("socket closed")


def run_proxy():
    proxy_address = ('127.0.0.1', PORT)
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(proxy_address)
    proxy_socket.listen(5)

    print(f'Proxy server is running on port {PORT}...')

    while True:
        client_socket, addr = proxy_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    run_proxy()
