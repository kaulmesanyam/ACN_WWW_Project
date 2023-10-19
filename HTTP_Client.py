import urllib.request

localhost = 'http://localhost:8000/'
google = 'http://www.google.com/'
proxy = 'http://localhost:8888/'
def send_request():
    url = proxy
    response = urllib.request.urlopen(url)
    print(response.read().decode())

if __name__ == '__main__':
    send_request()