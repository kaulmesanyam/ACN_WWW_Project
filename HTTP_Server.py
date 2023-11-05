import socket
import threading
import os

# Define the port on which the web server will run
PORT = 8080

# Function to handle client connections
def handle_client(client_socket):
    # Receive the client's HTTP request
    request = client_socket.recv(4096).decode()

    # Parse the request to extract the file path
    file_path = request.split('\n')[0].split(' ')[1][1:]
    print(f"file to send - {file_path}")

    # Check if the requested file exists
    if os.path.exists(file_path):
        # If the file exists, open it and read its content
        with open(file_path, 'rb') as file:
            content = file.read()
            print(f"content read from file - {content}")

            # Prepare the HTTP response with a 200 OK status, content length, and the file content
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    else:
        # If the file does not exist, prepare an HTTP response with a 404 Not Found status
        response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"

    print(f"response to send - {response}")

    # Send the response back to the client
    client_socket.sendall(response.encode())
    client_socket.close()


# Function to run the web server
def run_server():
    server_address = ('127.0.0.1', PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print(f'Web server is running on port {PORT}...')

    while True:
        client_socket, addr = server_socket.accept()
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


# Entry point of the script
if __name__ == '__main__':
    run_server()
