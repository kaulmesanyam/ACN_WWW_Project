# import urllib.request
#
# localhost = 'http://localhost:8000/'
# google = 'http://www.google.com/'
# proxy = 'http://localhost:8888/'
# def send_request():
#     url = proxy
#     response = urllib.request.urlopen(url)
#     print(response.read().decode())
#
# if __name__ == '__main__':
#     send_request()


import socket
import sys

def send_request(proxy_ip, server_ip, port, path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_ip, port))

    request = f"GET {path} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
    client_socket.send(request.encode())

    response = client_socket.recv(4096)
    while response:
        print(response.decode(), end='')
        response = client_socket.recv(4096)

    client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python web_client.py <proxy_ip> <server_ip> <port> <path>")
        sys.exit(1)

    proxy_ip = sys.argv[1]
    server_ip = sys.argv[2]
    port = int(sys.argv[3])
    path = sys.argv[4]

    send_request(proxy_ip, server_ip, port, path)
