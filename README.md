
# Programming Assignement WWW

This assignment contains 4 parts such as “simple web client”, “simple web proxy
server”, “simple web server” and the enhancement in the simple proxy server
“extended web proxy"

### Steps to follow for the execution of code :

1. Running HTTP_Client.py with given arguments as follows in terminal
Here the host is server_ip:server_port
```
python3 HTTP_Client.py <proxy_ip> <host> <proxy_port> <path>
python3 HTTP_Client.py 127.0.0.1 127.0.0.1:8080 7777 /
``` 


2. Running the HTTP_Server.py
```
python3 HTTP_Server.py
``` 

#### if want to connect the server via proxy then run this also
3. Running the Proxy_Server.py
```
python3 Proxy_Server.py
```

#### To configure the proxy manually in the browser
look for menu selections like Edit, Preferences, Advanced, Proxies. After changing the proxy in the browser then run the extended proxy server file.

#### Now to implement enhancement to proxy server
4. Run the extended proxy server
```
python3 HTTP_Proxy_ext.py
```


