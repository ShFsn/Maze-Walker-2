from http.server import BaseHTTPRequestHandler


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/init':
            with open('data/server_data', 'w') as f:
                f.write('1\n'   # init
                        '0')    # guest_on

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
