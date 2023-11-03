import socket
import threading
import os

PORT = 8080
def handle_client(client_socket):
    request = client_socket.recv(4096).decode()

    # Parse the request to extract the file path
    file_path = request.split('\n')[0].split(' ')[1][1:]
    print(f"file to send - {file_path}")
    # Check if the requested file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            print(f"content read from file - {content}")
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"

    print(f"response to send - {response}")
    client_socket.sendall(response.encode())
    client_socket.close()


def run_server():
    server_address = ('127.0.0.1', PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print(f'Web server is running on port {PORT}...')

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == '__main__':
    run_server()
