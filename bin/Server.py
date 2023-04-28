from http.server import BaseHTTPRequestHandler


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/init':
            with open('data/server_data', 'w') as f:
                f.write('1\n'   # init
                        '0')    # guest_on

        elif self.path == '/guest_ping':
            with open('data/server_data', 'r') as f:
                data = f.read().split('\n')
            data[1] = '1'
            with open('data/server_data', 'w') as f:
                f.write('\n'.join(data))
            self.wfile.write(bytes('established', "utf-8"))

        elif self.path == '/stop':
            self.server.server_close()
