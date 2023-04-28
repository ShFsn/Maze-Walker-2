from http.server import BaseHTTPRequestHandler


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/init':
            with open('data/server_data', 'w') as f:
                f.write('1\n'   # init
                        '0')    # guest_on

        elif self.path == '/check_disconnect':
            data = ''
            while len(data) < 1:
                with open('data/server_data', 'r') as f:
                    data = f.read()
            if data == 'disconnect':
                self.wfile.write(bytes('confirm', "utf-8"))
                with open('data/server_data', 'w') as f:
                    f.write('confirm')
            else:
                self.wfile.write(bytes('negative', "utf-8"))

        elif self.path == '/stop':
            self.server.server_close()

        elif self.path == '/guest_ping':
            data = list()
            while len(data) < 2:
                with open('data/server_data', 'r') as f:
                    data = f.read().split('\n')
            data[1] = '1'
            with open('data/server_data', 'w') as f:
                f.write('\n'.join(data))
            self.wfile.write(bytes('established', "utf-8"))

        elif self.path == '/get_maze':
            with open('data/server_data', 'r') as f:
                data = f.read().split('#')
            if len(data) > 1:
                self.wfile.write(bytes(data[1], "utf-8"))
            else:
                self.wfile.write(bytes('', "utf-8"))

        elif len(self.path.split('/')) > 2:
            req = self.path.split('/')

            if req[1] == 'set_pos':
                data = list()
                while len(data) < 2:
                    with open('data/server_data', 'r') as f:
                        data = f.read().split('#')
                data[1 + int(req[2])] = req[3] + '\n' + req[4] + '\n'
                with open('data/server_data', 'w') as f:
                    f.write('#'.join(data))

            elif req[1] == 'get_pos':
                data = list()
                while len(data) < 2:
                    with open('data/server_data', 'r') as f:
                        data = f.read().split('#')
                self.wfile.write(bytes(data[1 + int(req[2])], "utf-8"))
