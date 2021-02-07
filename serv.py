import socketserver
import socket

class MyTCPHandler(socketserver.BaseRequestHandler):

    # noinspection PyAttributeOutsideInit
    def handle(self, k=0):
        self.data = self.request.recv(2 ** 20).strip()
        s = '\nПривет, мой друг!'
        print("{} wrote:".format(self.client_address[0]))
        print(str(self.data, "utf-8"))
        self.data = self.data+s.encode("utf-8")
        k = k + 1
        print(k)
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = socket.gethostname(), 8000

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    try:
        print(f'Connected to {HOST}:{PORT}')
        print('Quit the server with CTRL-BREAK.')
        server.serve_forever()
    except KeyboardInterrupt:
        print()
