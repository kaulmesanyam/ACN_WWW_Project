import socket
import threading

PORT = 7777
BLACKLIST = {'www.blockedwebsite.com'}
CENSORED = {'Example'}

def handle_client(client_socket):
    request = client_socket.recv(4096).decode()
    print(request)
    # Parse the request to extract the host and port
    print('Parsing request...')
    command = request.split('\r\n')[0].split(' ')[0]
    print(f'command: {command}')
    if command == 'GET':
        host = request.split('\r\n')[1].split(' ')[1]
        request = f"GET / HTTP/1.0\r\nHost: {host}\r\n\r\n"
        parts = host.split(':')
        if len(parts) == 2:
            server_ip = parts[0]
            port = int(parts[1])
        else:
            server_ip = parts[0]
            port = 80

        print(f'host: {server_ip}  | port: {port}')

        if server_ip in BLACKLIST:
            # Send a custom HTML page informing the user that the website is blocked
            with open('blacklisted_response.html', 'rb') as f:
                response = f.read()
            client_socket.sendall(response)
        else:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((server_ip, port))

            server_socket.sendall(request.encode())

            response = server_socket.recv(4096)
            total = b''
            while response:
                print(response)
                total = total + response
                response = server_socket.recv(4096)

            filtered = ''
            for word in CENSORED:
                filtered = total.decode().replace(word, len(word)*'X')
            encoded = filtered.encode()
            client_socket.sendall(encoded)
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
