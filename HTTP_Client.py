import socket
import sys
from bs4 import BeautifulSoup
import urllib.parse


def send_request(proxy_ip, server_ip, port, path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_ip, port))

    request = f"GET {path} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
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
    server_ip = sys.argv[2]
    port = int(sys.argv[3])
    path = sys.argv[4]

    links = send_request(proxy_ip, server_ip, port, path)

    for link in links:
        print(f"Sending request to: {link}")
        send_request(proxy_ip, urllib.parse.urlparse(link).hostname, port, urllib.parse.urlparse(link).path)