import socket
import threading


def send_request():
    s = socket.socket()
    s.connect(("127.0.0.1", 8080))

    request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    s.sendall(request.encode())

    response = s.recv(4069)
    print(response.decode())

    s.close()

threads = []
for i in range(3):
    t = threading.Thread(target=send_request)
    t.start()
    threads.append(t)
    
for t in threads:
    t.join()
 