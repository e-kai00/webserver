import socket
import os
import threading
import time

HOST = "127.0.0.1"
PORT = 8080
MAX_DATA_SIZE = 1024
WWW_ROOT = "www"


def setup_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print(f"Server running on {host}: {port}...")
    return s


def handle_request(conn):
    data = conn.recv(MAX_DATA_SIZE)
    if not data: 
        return
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


def handle_connections(server_socket):
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def handle_client(conn, addr):
    # handles one client connection
    # each client will run in its own thread
    print(f"Connected by {addr}, thread={threading.get_ident()}")

    try:
        time.sleep(5)
        handle_request(conn)
    finally:
        conn.close()


def main():
    server_socket = setup_server(HOST, PORT)
    try:
        handle_connections(server_socket)
    finally:
         # close server socket
        server_socket.close()


if __name__ == "__main__":
    main()
