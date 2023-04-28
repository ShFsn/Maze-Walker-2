from bin.Server import Server
from http.server import ThreadingHTTPServer
from threading import Thread
# from random import randint
import socket
import time


# noinspection PyBroadException
class Connector:
    def __init__(self):
        self.web_server = None
        self._self_hostname = self._get_self_hostname()
        self._conn_hostname = None
        self._conn_port = None

    @staticmethod
    def _get_self_hostname():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        hostname = s.getsockname()[0]
        s.close()
        return hostname

    def _send_request(self, req):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._conn_hostname, self._conn_port))
        sock.send(str.encode(f"GET {req} HTTP/1.1\r\n\r\n\r\n"))
        response = sock.recv(1024)
        sock.close()
        return response.decode()

    # noinspection PyBroadException
    def _server_run(self):
        try:
            self.web_server.serve_forever()
        except:
            self.web_server.server_close()

    def server_start(self):
        hostname = self._get_self_hostname()
        # port = randint(40000, 59999)
        port = 8000
        self.web_server = ThreadingHTTPServer((hostname, port), Server)
        t = Thread(target=self._server_run)
        t.start()
        self._conn_hostname = hostname
        self._conn_port = port
        self._send_request('/init')
        return hostname, port

    @staticmethod
    def disconnect():
        start = time.time()
        data = list()
        while len(data) < 2:
            with open('data/server_data', 'r') as f:
                data = f.read()
            with open('data/server_data', 'w') as f:
                f.write('disconnect')
        with open('data/server_data', 'r') as f:
            data = f.read()
        while data != 'confirm' and time.time() - start < 1:
            with open('data/server_data', 'r') as f:
                data = f.read()

    def check_disconnect(self):
        if self._send_request('/check_disconnect') == 'confirm':
            return True
        return False


    def server_stop(self):
        self._send_request('/stop')

    @staticmethod
    def check_init():
        data = list()
        while len(data) < 2:
            with open('data/server_data', 'r') as f:
                data = f.read().split('\n')
        return True if int(data[0]) else False

    @staticmethod
    def check_guest():
        data = list()
        while len(data) < 2:
            with open('data/server_data', 'r') as f:
                data = f.read().split('\n')
        return True if int(data[1]) else False

    # noinspection PyBroadException
    def connect_guest(self, address):
        self._conn_hostname = address[0]
        self._conn_port = address[1]
        try:
            response = self._send_request('/guest_ping')
            return False if response == 'established' else True
        except:
            return True

    @staticmethod
    def set_mp_maze(maze_data):
        data = ''
        while len(data) < 2:
            with open('data/server_data', 'r') as f:
                data = f.read()
            if data.find('#'):
                data = data.split('#')[0]
            with open('data/server_data', 'w') as f:
                f.write(data + '\n#' + maze_data + '\n#' + maze_data.split('\n')[2] + '\n' + maze_data.split('\n')[3] +
                        '\n#' + maze_data.split('\n')[4] + '\n' + maze_data.split('\n')[5])

    def get_mp_maze(self):
        return self._send_request('/get_maze')

    def set_mp_pos(self, n_player, pos):
        if n_player == 1:
            data = list()
            while len(data) < 2:
                with open('data/server_data', 'r') as f:
                    data = f.read().split('#')
            data[1 + n_player] = str(pos[0]) + '\n' + str(pos[1]) + '\n'
            with open('data/server_data', 'w') as f:
                f.write('#'.join(data))
        if n_player == 2:
            self._send_request('/set_pos/' + str(n_player) + '/' + str(pos[0]) + '/' + str(pos[1]))

    def get_mp_pos(self, n_player):
        pos = '0\n0'
        if n_player == 1:
            data = list()
            while len(data) < 2:
                with open('data/server_data', 'r') as f:
                    data = f.read().split('#')
            pos = data[1 + n_player]
        elif n_player == 2:
            pos = self._send_request('/get_pos/' + str(n_player))
        return int(pos.split('\n')[0]), int(pos.split('\n')[1])

