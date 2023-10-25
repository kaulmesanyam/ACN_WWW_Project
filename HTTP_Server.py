import socket
import threading
import os


def handle_client(client_socket):
    request = client_socket.recv(4096).decode()

    # Parse the request to extract the file path
    file_path = request.split('\n')[0].split(' ')[1][1:]

    # Check if the requested file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"

    client_socket.sendall(response.encode())
    client_socket.close()


def run_server():
    server_address = ('127.0.0.1', 6789)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print('Web server is running on port 6789...')

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    run_server()
