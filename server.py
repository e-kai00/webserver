import socket
import os

HOST = "127.0.0.1"
PORT = 8080
MAX_DATA_SIZE = 1024
WWW_ROOT = "www"


def setup_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Server running on {HOST}: {PORT}...")
    return s


def handle_request(conn):
    data = conn.recv(MAX_DATA_SIZE)
    request_line = data.split(b'\r\n')[0].decode()
    method, path, version = request_line.split()
    print(f"Request: {method} {path} {version}")

    if path == "/":
        path = "/index.html"
    file_path = os.path.join(WWW_ROOT, path.lstrip("/"))
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            body = f.read()
            response = f"HTTP/1.1 200 OK\r\n\r\n{body}\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\nPage Not Found"    
    conn.sendall(response.encode())


def handle_connection(server_socket):
    while True:
        conn, addr = server_socket.accept()
        print('Connected by', addr)

        try:
            handle_request(conn)
        finally:
            # close client socket
            conn.close()

def main():
    server_socket = setup_server(HOST, PORT)
    try:
        handle_connection(server_socket)
    finally:
         # close server socket
        server_socket.close()


if __name__ == "__main__":
    main()
