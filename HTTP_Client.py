import socket
import sys
from bs4 import BeautifulSoup
import urllib.parse


def send_request(proxy_ip, server_ip, port, path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_ip, port))

    request = f"GET {path} HTTP/1.0\r\nHost: {server_ip}\r\n\r\n"
    client_socket.send(request.encode())

    response = client_socket.recv(4096)
    html_content = b''
    while response:
        print(response)
        html_content += response
        response = client_socket.recv(4096)

    client_socket.close()

    soup = BeautifulSoup(html_content, 'html.parser')
    links = [urllib.parse.urljoin(f'http://{server_ip}', link.get('href')) for link in soup.find_all('a', href=True)]

    return links

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python web_client.py <proxy_ip> <server_ip> <port> <path>")
        sys.exit(1)

    proxy_ip = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    path = sys.argv[4]

    server_ip = '127.0.0.1'
    server_port = 80

    parts = host.split(':')
    if len(parts) == 2:
        server_ip = parts[0]
        server_port = int(parts[1])
    else:
        server_ip = parts[0]
        server_port = 80

    links = send_request(proxy_ip, host, port, path)

    for link in links:
        print(f"Sending request to: {link}")
        host = urllib.parse.urlparse(link).hostname + ":" + str(server_port)
        send_request(proxy_ip, host, port, urllib.parse.urlparse(link).path)