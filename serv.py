import socketserver
import socket
import threading


class MyTCPHandler(socketserver.BaseRequestHandler):

    # noinspection PyAttributeOutsideInit
    def handle(self):
        self.data = self.request.recv(2 ** 20).strip()
        s = '\nПривет, мой друг!'
        print(f"{self.client_address[0]} wrote from {threading.current_thread().name}:")
        print(str(self.data, "utf-8"))
        input()
        self.data = self.data+s.encode("utf-8")
        self.request.sendall(self.data)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runserver():
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 8000
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    try:
        print(f'Connected to {HOST}:{PORT}')
        print('Quit the server with CTRL-BREAK.')
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        while True:
            pass
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    runserver()
