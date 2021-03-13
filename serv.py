import socketserver
import socket
import threading
from random import randint


def massRand(m):
    Sum = [0] * (len(m) + 1)
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
    locked = [0] * count
    lock = [False] * count
    names = [''] * count
    parms = [''] * count
    action = [''] * count

    @staticmethod
    def clear(x):
        lab.inside[x] = lab.devices[x] = lab.waiters[x] = lab.locked[x] = 0
        lab.names[x] = lab.parms[x] = lab.action[x] = ''
        lab.lock[x] = False

    @staticmethod
    def handle(a):
        sep = '#'
        v = list(map(str, a.split(sep)))
        s = v[0]
        if s == 'CREATE':
            n = int(v[1])
            x = massRand(lab.rooms)
            if x == -1:
                return 'Нет места'
            lab.rooms[x] = 0
            lab.sizes[x] = n
            return f'Успешно! Ваш номер комнаты <{x}>'
        if s == 'CREATEX':
            n, x = int(v[1]), int(v[2])
            if lab.rooms[x] == 0:
                return 'Нет места'
            lab.rooms[x] = 0
            lab.sizes[x] = n
            return f'Успешно! Ваш номер комнаты <{x}>'
        if s == 'JOIN':
            k, x, nam, par = int(v[1]), int(v[2]), v[3], v[4]
            if lab.rooms[x] == 1:
                return 'Такой комнаты нет'
            n, m = lab.sizes[x], lab.inside[x]
            if m + k > n:
                return f'Эта комната столько игроков не вместит. Свободно {n - m} мест'
            lab.names[x] += nam
            lab.parms[x] = par
            lab.devices[x] += 1
            lab.inside[x] += k
            return str(m)
        x = int(v[1])

        if s == 'SET':
            action = v[2]

            while lab.lock[x]:
                pass
            if lab.inside[x] == 0:
                return '0'

            lab.action[x] = action
            return '0'

        if s == 'DELETE':
            lab.rooms[x] = 1
            lab.sizes[x] = 0
            lab.clear(x)
            return '0'
        if s == 'CLEAR':
            lab.clear(x)
            return '0'

        while lab.lock[x]:
            pass
        if lab.inside[x] == 0:
            return '0'

        if s == 'RWAIT':
            while 0 < lab.inside[x] < lab.sizes[x]:
                pass
            return '0'
        if s == 'NAM':
            return lab.names[x]
        if s == 'PAR':
            return lab.parms[x]
        if s == 'GET':
            while lab.action[x] == '' and lab.inside[x] > 0:
                pass
            return lab.action[x]
        if s == 'WAIT':
            lab.waiters[x] += 1
            while lab.waiters[x] < lab.devices[x] and lab.inside[x] > 0:
                pass
            lab.lock[x] = True
            lab.locked[x] += 1
            if lab.locked[x] == lab.devices[x]:
                lab.lock[x] = False
                lab.locked[x] = lab.waiters[x] = 0
                lab.action[x] = ''
            return '0'


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
