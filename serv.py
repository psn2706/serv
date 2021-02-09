import socketserver
import socket
import threading
from random import randint


def massRand(m):
    Sum = [0] * (len(m)+1)
    for i in range(len(m)):
        Sum[i + 1] = Sum[i] + m[i]
    r = randint(0, Sum[len(m)] - 1)
    for i in range(len(m)):
        if Sum[i] <= r < Sum[i + 1]:
            return i
    return -1


class lab:
    count = 100
    rooms = [1] * count
    sizes = [0] * count
    inside = [0] * count
    devices = [0] * count
    waiters = [0] * count
    names = [''] * count
    parms = [''] * count
    action = [''] * count

    @staticmethod
    def handle(a):
        pos = a.find(' ')
        s = a[0:pos]
        if s == 'CREATE':
            x = massRand(lab.rooms)
            if x == -1:
                return 'Нет места'
            lab.rooms[x] = 0
            lab.sizes[x] = int(a[pos + 1:])
            return f'Успешно! Ваш номер комнаты <{x}>'
        if s == 'CREATEX':
            s = a[pos + 1:]
            n, x = map(int, s.split(','))
            if lab.rooms[x] == 0:
                return 'Нет места'
            lab.rooms[x] = 0
            lab.sizes[x] = n
            return f'Успешно! Ваш номер комнаты <{x}>'
        if s == 'JOIN':
            s = a[pos + 1:]
            k, x, nam, par = map(str, s.split(','))
            k, x = int(k), int(x)
            if lab.rooms[x] == 1:
                return 'Такой комнаты нет'
            n, m = lab.sizes[x], lab.inside[x]
            if m+k > n:
                return f'Эта комната столько игроков не вместит. Свободно {n-m} мест'
            lab.names[x] += nam
            lab.parms[x] = par
            lab.devices[x] += 1
            lab.inside[x] += k
            return str(m)
        if s == 'SET':
            s = a[pos + 1:]
            action, x = map(str, s.split(','))
            x = int(x)
            lab.action[x] = action
            return '0'
        x = int(a[pos + 1:])
        if s == 'RWAIT':
            while lab.inside[x] < lab.sizes[x]:
                pass
            return '0'
        if s == 'NAM':
            return lab.names[x]
        if s == 'PAR':
            return lab.parms[x]
        if s == 'GET':
            while lab.action[x] == '':
                pass
            return lab.action[x]
        if s == 'WAIT':
            lab.waiters[x] += 1
            while lab.waiters[x] < lab.devices[x]:
                pass
            if lab.waiters[x] == lab.devices[x]:
                lab.waiters[x] = 0
            if lab.action[x] != '':
                lab.action[x] = ''
            return '0'
        if s == 'DELETE':
            lab.rooms[x] = 1
            return '0'
        if s == 'CLEAR':
            lab.inside[x], lab.devices[x], lab.waiters[x] = [0]*3
            lab.names[x], lab.parms[x], lab.action[x] = ['']*3


class MyTCPHandler(socketserver.BaseRequestHandler):

    # noinspection PyAttributeOutsideInit
    def handle(self):
        data = self.request.recv(2 ** 20).strip()
        ans = lab.handle(data.decode("utf-8"))
        self.request.sendall(ans.encode("utf-8"))


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
