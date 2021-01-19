import socketserver
import socket


class MyTCPHandler(socketserver.BaseRequestHandler):

    # noinspection PyAttributeOutsideInit
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(str(self.data, "utf-8"))
        self.request.sendall(self.data.upper()[1:])


if __name__ == "__main__":
    HOST, PORT = socket.gethostname(), 8000

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
