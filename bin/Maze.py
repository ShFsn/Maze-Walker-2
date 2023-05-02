from random import randint
from heapq import heappush, heappop
from bin.Player import Player
from bin.Connector import Connector


class Maze:
    def __init__(self):
        self._height = 0
        self._width = 0
        self._act_height = 0
        self._act_width = 0
        self._generator_type = ''
        self._points_pos_type = 0
        self._matrix = list()
        self._end_point = (0, 0)
        self._timer = 0
        self._player_1 = Player()
        self._player_1.set_letter('1')
        self._player_2 = Player()
        self._player_2.set_letter('2')
        self._single = True
        self._online = False
        self._host = False
        self._server_active = False
        self._connector = Connector()
        with open('data/Tile_entity', 'r') as f:
            self._tile_entity = f.read().split('\n')
        with open('data/Tile_empty', 'r') as f:
            self._tile_empty = f.read().split('\n')
        with open('data/Tile_wall', 'r') as f:
            self._tile_wall = f.read().split('\n')
        with open('data/Tile_path_up', 'r') as f:
            self._tile_path_up = f.read().split('\n')
        with open('data/Tile_path_left', 'r') as f:
            self._tile_path_left = f.read().split('\n')
        with open('data/Tile_path_down', 'r') as f:
            self._tile_path_down = f.read().split('\n')
        with open('data/Tile_path_right', 'r') as f:
            self._tile_path_right = f.read().split('\n')

    def set_single(self):
        self._player_1.activate()
        self._player_2.deactivate()
        self._single = True
        self._online = False

    def set_multi(self):
        self._player_1.activate()
        self._player_2.activate()
        self._single = False
        self._online = False

    def set_online(self):
        self._online = True

    def set_host(self):
        self._host = True

    def set_guest(self):
        self._host = False

    def is_single(self):
        return self._single

    def is_online(self):
        return self._online

    def is_host(self):
        return self._host

    def server_start(self):
        self._server_active = True
        return self._connector.server_start()

    def server_disconnect(self):
        self._connector.disconnect()

    def check_disconnect(self):
        return self._connector.check_disconnect()

    def server_stop(self):
        if self._server_active:
            self._connector.server_stop()
            self._server_active = False

    def check_init(self):
        return self._connector.check_init()

    def check_guest(self):
        return self._connector.check_guest()

    def connect_guest(self, address):
        return self._connector.connect_guest(address)

    def set_mp_maze(self, data):
        self._connector.set_mp_maze(data)

    def get_mp_maze(self):
        return self._connector.get_mp_maze()

    def is_finished(self):
        return 1 if self._player_1.get_pos() == self._end_point else 2 if \
               (self._player_2.get_pos() == self._end_point and not self.is_single()) else 0

    def set_generator(self, g_t):
        self._generator_type = g_t

    def set_size(self, height, width):
        self._height = int(height)
        self._act_height = self._height * 2 + 1
        self._width = int(width)
        self._act_width = self._width * 2 + 1

    def set_points_pos_type(self, pos_type):
        self._points_pos_type = pos_type
        print(self._points_pos_type)

    def get_timer(self):
        return self._timer

    def set_timer(self, timer):
        self._timer = timer

    def move(self, n_player, side):
        player = self._player_2 if (n_player == 2 and not self._single and not self._online) or \
                                   (not self._single and self._online and not self._host) else self._player_1
        pos = player.get_pos()
        new_pos = (pos[0] - 1, pos[1]) if side == 'up' \
            else (pos[0], pos[1] - 1) if side == 'left' \
            else (pos[0] + 1, pos[1]) if side == 'down' \
            else (pos[0], pos[1] + 1)
        if self._matrix[new_pos[0]][new_pos[1]] == 0:
            player.set_pos(new_pos[0], new_pos[1])

    def get_pos(self, n_player):
        player = self._player_2 if n_player == 2 else self._player_1
        return player.get_pos()

    def set_pos(self, n_player, pos):
        player = self._player_2 if n_player == 2 else self._player_1
        player.set_pos(pos[0], pos[1])

    def set_mp_pos(self, n_player, pos):
        self._connector.set_mp_pos(n_player, pos)

    def get_mp_pos(self, n_player):
        return self._connector.get_mp_pos(n_player)

    def _calc_path(self, pos_1, pos_2):
        wave_l = 11
        flag = True
        pos = pos_1
        self._matrix[pos[0]][pos[1]] = wave_l
        while flag:
            flag = False
            for i in range(self._act_height):
                for j in range(self._act_width):
                    if self._matrix[i][j] == wave_l:
                        self._matrix[i - 1][j] = wave_l + 1 if self._matrix[i - 1][j] == 0 else self._matrix[i - 1][j]
                        self._matrix[i + 1][j] = wave_l + 1 if self._matrix[i + 1][j] == 0 else self._matrix[i + 1][j]
                        self._matrix[i][j - 1] = wave_l + 1 if self._matrix[i][j - 1] == 0 else self._matrix[i][j - 1]
                        self._matrix[i][j + 1] = wave_l + 1 if self._matrix[i][j + 1] == 0 else self._matrix[i][j + 1]
                        flag = True
            wave_l += 1
        pos = pos_2
        wave_l = self._matrix[pos[0]][pos[1]]
        while wave_l >= 11:
            self._matrix[pos[0]][pos[1]] = 2
            if self._matrix[pos[0] - 1][pos[1]] == wave_l - 1:
                pos = (pos[0] - 1, pos[1])
            elif self._matrix[pos[0] + 1][pos[1]] == wave_l - 1:
                pos = (pos[0] + 1, pos[1])
            elif self._matrix[pos[0]][pos[1] - 1] == wave_l - 1:
                pos = (pos[0], pos[1] - 1)
            elif self._matrix[pos[0]][pos[1] + 1] == wave_l - 1:
                pos = (pos[0], pos[1] + 1)
            wave_l -= 1
        for i in range(self._act_height):
            for j in range(self._act_width):
                if self._matrix[i][j] > 2:
                    self._matrix[i][j] = 0

    def show_path(self, key):
        self._calc_path(self._player_1.get_pos() if key == '1' else self._player_2.get_pos(), self._end_point)

    def hide_path(self):
        for i in range(self._act_height):
            for j in range(self._act_width):
                if self._matrix[i][j] > 1:
                    self._matrix[i][j] = 0

    def set_data(self, save):
        s_cont = save.split('\n')
        self._height = int(s_cont[0])
        self._act_height = self._height * 2 + 1
        self._width = int(s_cont[1])
        self._act_width = self._width * 2 + 1
        self._player_1.set_pos(int(s_cont[2]), int(s_cont[3]))
        self._player_2.set_pos(int(s_cont[4]), int(s_cont[5]))
        self._end_point = (int(s_cont[6]), int(s_cont[7]))
        self._timer = int(s_cont[8])
        self._matrix = list()
        for i in range(self._act_height):
            self._matrix.append(list())
            for j in range(self._act_width):
                self._matrix[i].append(int(s_cont[i + 9][j]))

    def get_data(self):
        data = ''
        data += str(self._height) + '\n'
        data += str(self._width) + '\n'
        data += str(self._player_1.get_pos()[0]) + '\n'
        data += str(self._player_1.get_pos()[1]) + '\n'
        data += str(self._player_2.get_pos()[0]) + '\n'
        data += str(self._player_2.get_pos()[1]) + '\n'
        data += str(self._end_point[0]) + '\n'
        data += str(self._end_point[1]) + '\n'
        data += str(self._timer)
        for i in self._matrix:
            data += '\n'
            for j in i:
                data += str(j)
        return data

    def get_picture(self):
        string_matrix = ''

        # Debug renderer
        '''for i in range(self._act_width):
            for j in range(self._act_height):
                sym = '*' if self._matrix[i][j] == 1 else '-' if self._matrix[i][j] == 2 else ' '
                sym = 'F' if self._end_point[0] == i and self._end_point[1] == j else sym
                sym = 'A' if self._player_1.get_pos()[0] == i and self._player_1.get_pos()[1] == j else sym
                sym = 'B' if self._player_2.get_pos()[0] == i and self._player_2.get_pos()[1] == j and not \
                    self.is_single() else sym
                sym = str(self._matrix[i][j]) if self._matrix[i][j] > 10 else sym
                string_matrix += sym
            string_matrix += '\n'
        string_matrix = string_matrix[:-1]'''

        # Normal renderer
        lines_matrix = list()
        lines_matrix.append(' _ _ _' * (self._act_width - 2) + '\n')
        for i in range(1, self._act_height - 1):
            for j in range(3):
                lines_matrix.append('|')
            for j in range(1, self._act_width - 1):
                if self._player_2.get_pos() == (i, j) and not self.is_single():
                    tile = self._tile_entity.copy()
                    tile[1] = tile[1].split('#')[0] + self._player_2.get_letter() + tile[1].split('#')[1]
                elif self._player_1.get_pos() == (i, j):
                    tile = self._tile_entity.copy()
                    tile[1] = tile[1].split('#')[0] + self._player_1.get_letter() + tile[1].split('#')[1]
                elif self._end_point == (i, j):
                    tile = self._tile_entity.copy()
                    tile[1] = tile[1].split('#')[0] + 'F' + tile[1].split('#')[1]
                elif self._matrix[i][j] == 1:
                    tile = self._tile_wall
                elif self._matrix[i][j] == 2:
                    tile = list()
                    tile.append(self._tile_path_up[int(self._matrix[i - 1][j] == 2)])
                    tile.append(self._tile_path_left[int(self._matrix[i][j - 1] == 2)])
                    tile[1] += self._tile_path_right[int(self._matrix[i][j + 1] == 2)]
                    tile.append(self._tile_path_down[int(self._matrix[i + 1][j] == 2)])
                # elif self._matrix[i][j] == 0:
                else:
                    tile = self._tile_empty
                # path workaround
                tile[2] = tile[2][:2] + '|' + tile[2][-3:] if self._matrix[i + 1][j] == 2 and self._matrix[i][j] == 2 \
                    else tile[2]
                tile[1] = tile[1][:-1] + '-' if self._matrix[i][j + 1] == 2 and self._matrix[i][j] == 2 else tile[1]
                for k in range(3):
                    lines_matrix[k - 3] += tile[k]
            for j in range(3):
                lines_matrix[j - 3] += '\n'
        for i in lines_matrix:
            string_matrix += i

        return string_matrix[:-1]

    def _get_corresponding_edges(self, vert, edges):
        res = list()
        if vert[0] < self._height and edges[vert[0] * 2 - 1][vert[1] - 1] > 0:
            res.append((edges[vert[0] * 2 - 1][vert[1] - 1], vert[0] * 2 - 1, vert[1] - 1))
            edges[vert[0] * 2 - 1][vert[1] - 1] = -1
        if vert[0] > 1 and edges[vert[0] * 2 - 3][vert[1] - 1] > 0:
            res.append((edges[vert[0] * 2 - 3][vert[1] - 1], vert[0] * 2 - 3, vert[1] - 1))
            edges[vert[0] * 2 - 3][vert[1] - 1] = -1
        if vert[1] < self._width and edges[vert[0] * 2 - 2][vert[1] - 1] > 0:
            res.append((edges[vert[0] * 2 - 2][vert[1] - 1], vert[0] * 2 - 2, vert[1] - 1))
            edges[vert[0] * 2 - 2][vert[1] - 1] = -1
        if vert[1] > 1 and edges[vert[0] * 2 - 2][vert[1] - 2] > 0:
            res.append((edges[vert[0] * 2 - 2][vert[1] - 2], vert[0] * 2 - 2, vert[1] - 2))
            edges[vert[0] * 2 - 2][vert[1] - 2] = -1
        return res

    @staticmethod
    def _get_corresponding_vertx(edge):
        res = list()
        if edge[1] % 2 == 0:
            res.append((edge[1] // 2 + 1, edge[2] + 1))
            res.append((edge[1] // 2 + 1, edge[2] + 2))
        else:
            res.append(((edge[1] + 1) // 2, edge[2] + 1))
            res.append(((edge[1] + 1) // 2 + 1, edge[2] + 1))
        return res

    def _break_wall(self, vertx):
        # noinspection PyTypeChecker
        self._matrix[(vertx[0][0] - 1) * 2 + 1][(vertx[0][1] - 1) * 2 + 1] = 0
        # noinspection PyTypeChecker
        self._matrix[(vertx[1][0] - 1) * 2 + 1][(vertx[1][1] - 1) * 2 + 1] = 0
        # noinspection PyTypeChecker
        self._matrix[vertx[0][0] + vertx[1][0] - 1][vertx[0][1] + vertx[1][1] - 1] = 0

    def generate(self):
        self._timer = 0
        self._matrix = list()
        edges = list()
        queue = list()

        # Generating players and finish positions
        if self._points_pos_type == 1:
            self._player_1.set_pos(1, 1)
            self._player_2.set_pos(self._act_height - 2, 1)
            self._end_point = (1 + (self._act_height - 3) * randint(0, 1), self._act_width - 2)
        elif self._points_pos_type == 2:
            self._player_1.set_pos((randint(1, self._height) - 1) * 2 + 1, (randint(1, self._width) - 1) * 2 + 1)
            self._player_2.set_pos((randint(1, self._height) - 1) * 2 + 1, (randint(1, self._width) - 1) * 2 + 1)
            self._end_point = ((randint(1, self._height) - 1) * 2 + 1, (randint(1, self._width) - 1) * 2 + 1)
            while self._player_1.get_pos()[0] == self._player_2.get_pos()[0] \
                    and self._player_1.get_pos()[1] == self._player_2.get_pos()[1]:
                self._player_2.set_pos((randint(1, self._height) - 1) * 2 + 1, (randint(1, self._width) - 1) * 2 + 1)
            while (self._end_point[0] == self._player_1.get_pos()[0] and
                   self._end_point[1] == self._player_1.get_pos()[1]) or \
                    (self._end_point[0] == self._player_2.get_pos()[0] and
                     self._end_point[1] == self._player_2.get_pos()[1]):
                self._end_point = ((randint(1, self._height) - 1) * 2 + 1, (randint(1, self._width) - 1) * 2 + 1)
        elif self._points_pos_type == 3:
            perimeter = self._height * 2 + self._width * 2 - 4
            pos_1 = randint(1, perimeter)
            pos_2 = randint(1, perimeter)
            pos_f = randint(1, perimeter)
            while pos_1 == pos_2:
                pos_2 = randint(1, perimeter)
            while pos_f == pos_1 or pos_f == pos_2:
                pos_f = randint(1, perimeter)
            pos_h = 1
            pos_w = 3
            for i in range(1, perimeter + 1):
                if pos_1 == i:
                    self._player_1.set_pos(pos_h, pos_w)
                if pos_2 == i:
                    self._player_2.set_pos(pos_h, pos_w)
                if pos_f == i:
                    self._end_point = (pos_h, pos_w)
                if pos_w == 1:
                    pos_h -= 2
                elif pos_h == self._act_height - 2:
                    pos_w -= 2
                elif pos_w == self._act_width - 2:
                    pos_h += 2
                elif pos_h == 1:
                    pos_w += 2

        # Filling matrix with walls
        for i in range(self._act_height):
            self._matrix.append(list())
            for j in range(self._act_width):
                '''self._matrix[i].append(1 if i == 0 or i == self._act_height - 1 or j == 0 or j == self._act_width - 1
                                            or (i % 2 == 0 and j % 2 == 0) else -1)'''
                self._matrix[i].append(1)

        # Creating a set of graph edges with different randomly set values
        for i in range(self._height * 2 - 1):
            edges.append(list())
            for j in range(self._width - 1 + i % 2):
                edges[i].append(0)
        for k in range(1, (self._width - 1) * self._height + self._width * (self._height - 1) + 1):
            pos = randint(1, (self._width - 1) * self._height + self._width * (self._height - 1) + 1 - k)
            pos_curr = 0
            flag = True
            for i in range(self._height * 2 - 1):
                for j in range(self._width - 1 + i % 2):
                    pos_curr += 1 if edges[i][j] == 0 else 0
                    edges[i][j] = k if pos == pos_curr and flag else edges[i][j]
                    flag = False if pos == pos_curr else True

        # DFS
        if self._generator_type == 'DFS':
            q_len = 10
            vert = (randint(1, self._height), randint(1, self._width))
            self._matrix[(vert[0] - 1) * 2 + 1][(vert[1] - 1) * 2 + 1] = 0

            while q_len:
                ext = self._get_corresponding_edges(vert, edges)
                for i in ext:
                    heappush(queue, i)
                vertx = self._get_corresponding_vertx(heappop(queue))
                flag = False
                if self._matrix[(vertx[0][0] - 1) * 2 + 1][(vertx[0][1] - 1) * 2 + 1] == 1:
                    vert = (vertx[0][0], vertx[0][1])
                    flag = True
                if self._matrix[(vertx[1][0] - 1) * 2 + 1][(vertx[1][1] - 1) * 2 + 1] == 1:
                    vert = (vertx[1][0], vertx[1][1])
                    flag = True
                if flag:
                    self._break_wall(vertx)
                q_len = len(queue)

        # Minimum Spanning Tree
        if self._generator_type == 'MST':
            for i in range(len(edges)):
                for j in range(len(edges[i])):
                    heappush(queue, (edges[i][j], i, j))
            while len(queue):
                vertx = self._get_corresponding_vertx(heappop(queue))
                if self._matrix[(vertx[0][0] - 1) * 2 + 1][(vertx[0][1] - 1) * 2 + 1] == 0 \
                        and self._matrix[(vertx[1][0] - 1) * 2 + 1][(vertx[1][1] - 1) * 2 + 1] == 0:
                    self._calc_path(((vertx[0][0] - 1) * 2 + 1, (vertx[0][1] - 1) * 2 + 1),
                                    ((vertx[1][0] - 1) * 2 + 1, (vertx[1][1] - 1) * 2 + 1))
                    if self._matrix[(vertx[0][0] - 1) * 2 + 1][(vertx[0][1] - 1) * 2 + 1] == 2 \
                            and self._matrix[(vertx[1][0] - 1) * 2 + 1][(vertx[1][1] - 1) * 2 + 1] == 2:
                        flag = False
                    else:
                        flag = True
                    self.hide_path()
                else:
                    flag = True
                if flag:
                    self._break_wall(vertx)
