import socket

HOST = "127.0.0.1"
PORT = 8080
MAX_DATA_SIZE = 1024

# Create a TCP socket to listen on localhost:80.
# Wait for a connection from a client.
# Receive the HTTP request, parse the first line.
# Send a minimal HTTP response with the requested path.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Server running on {HOST}: {PORT}...")

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)

        try:
            data = conn.recv(MAX_DATA_SIZE)
            request_line = data.split(b'\r\n')[0].decode()
            method, path, version = request_line.split()
            print(f"Request: {method} {path} {version}")

            response = f"HTTP/1.1 200 OK\r\n\r\nRequested path: {path}\r\n"
            conn.sendall(response.encode())

        finally:
            # close client socket
            conn.close()
finally:
    # close server socket
    s.close()