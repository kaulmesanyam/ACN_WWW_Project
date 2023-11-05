import socket
import threading
from collections import defaultdict
import json
from _datetime import datetime

# Define constants
PORT = 8888
BLACKLIST = {'www.blockedwebsite.com'}
CENSORED = {'Example'}
access_date = datetime.today().date()

# File path for user statistics
user_stats_file = 'user_statistics.json'

# Function to save data to a JSON file
def saveDatatoFile(data):
    with open(user_stats_file, 'w') as file:
        json.dump(data, file)

# Function to load data from a JSON file
def loadData(user_stats_file):
    with open(user_stats_file, 'r') as json_file:
        loaded_data = json.load(json_file)
        # Print the loaded data
        print(f'data loaded from file - {loaded_data}')
        return loaded_data

# Load existing user statistics or initialize with empty data
user_statistics = loadData(user_stats_file)

# Function to update user access statistics
def update_statistics(client_address, accessed_website):
    # Ignore requests to detectportal.firefox.com
    if accessed_website != "detectportal.firefox.com":
        client_address_str = str(client_address)
        if client_address_str not in user_statistics:
            user_statistics[client_address_str] = {'accessed_websites': [], 'website_access_count': defaultdict(int)}

        accessed_site = {"website": accessed_website, "access_date": str(access_date)}
        user_statistics[client_address_str]['accessed_websites'].append(accessed_site)
        user_statistics[client_address_str]['website_access_count'][accessed_website] += 1
        saveDatatoFile(user_statistics)

# Function to handle client connections
def handle_client(client_socket, client_address):
    client_address = client_address[0]
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

            update_statistics(client_address, host)

            client_socket.close()
            server_socket.close()
    else:
        client_socket.close()

    print("socket closed")

# Function to run the proxy server
def run_proxy():
    proxy_address = ('127.0.0.1', PORT)
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(proxy_address)
    proxy_socket.listen(5)

    print(f'Proxy server is running on port {PORT}...')

    while True:
        client_socket, addr = proxy_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

# Entry point of the script
if __name__ == '__main__':
    run_proxy()
