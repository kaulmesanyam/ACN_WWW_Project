import socket
import sys
from bs4 import BeautifulSoup
import urllib.parse

# Function to send an HTTP GET request via a proxy, retrieve HTML content, and extract links
def send_request(proxy_ip, server_ip, port, path):
    # Create a client socket and connect to the proxy server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_ip, port))

    # Construct the HTTP GET request
    request = f"GET {path} HTTP/1.0\r\nHost: {server_ip}\r\n\r\n"
    client_socket.send(request.encode())

    # Receive the response in chunks (4096 bytes at a time)
    response = client_socket.recv(4096)
    html_content = b''
    while response:
        print(response)
        html_content += response
        response = client_socket.recv(4096)

    # Close the client socket
    client_socket.close()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract links from the HTML content and construct absolute URLs
    links = [urllib.parse.urljoin(f'http://{server_ip}', link.get('href')) for link in soup.find_all('a', href=True)]

    return links

if __name__ == '__main__':
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) < 5:
        print("Usage: python web_client.py <proxy_ip> <server_ip> <port> <path>")
        sys.exit(1)

    # Extract command line arguments
    proxy_ip = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    path = sys.argv[4]

    # Determine server IP and port from the provided host argument
    parts = host.split(':')
    if len(parts) == 2:
        server_ip = parts[0]
        server_port = int(parts[1])
    else:
        server_ip = parts[0]
        server_port = 80

    # Send a request to the proxy server
    links = send_request(proxy_ip, host, port, path)

    # For each link, send a request to retrieve and print more links
    for link in links:
        print(f"Sending request to: {link}")
        host = urllib.parse.urlparse(link).hostname + ":" + str(server_port)
        send_request(proxy_ip, host, port, urllib.parse.urlparse(link).path)
