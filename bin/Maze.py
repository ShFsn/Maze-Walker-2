from bin.Player import Player


class Maze:
    def __init__(self):
        self._height = 0
        self._width = 0
        self._act_height = 0
        self._act_width = 0
        self._matrix = list()
        self._end_point = (0, 0)
        self._timer = 0
        self._player_1 = Player()
        self._player_1.set_letter('1')
        self._player_2 = Player()
        self._player_2.set_letter('2')
        self._single = True
        self._online = False
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

    def is_single(self):
        return self._single

    def is_finished(self):
        return self._player_1.get_pos() == self._end_point or \
               (self._player_2.get_pos() == self._end_point and not self.is_single())

    def get_timer(self):
        return self._timer

    def set_timer(self, timer):
        self._timer = timer

    def move(self, n_player, side):
        player = self._player_1 if n_player == 1 else self._player_2
        pos = player.get_pos()
        new_pos = (pos[0] - 1, pos[1]) if side == 'up' \
            else (pos[0], pos[1] - 1) if side == 'left' \
            else (pos[0] + 1, pos[1]) if side == 'down' \
            else (pos[0], pos[1] + 1)
        if self._matrix[new_pos[0]][new_pos[1]] == 0:
            player.set_pos(new_pos[0], new_pos[1])

    def show_path(self, key):
        wave_l = 11
        flag = True
        pos = self._player_1.get_pos() if key == '1' else self._player_2.get_pos()
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
        pos = self._end_point
        wave_l = self._matrix[pos[0]][pos[1]]
        while wave_l > 11:
            if self._matrix[pos[0] - 1][pos[1]] == wave_l - 1:
                self._matrix[pos[0]][pos[1]] = 2
                pos = (pos[0] - 1, pos[1])
            elif self._matrix[pos[0] + 1][pos[1]] == wave_l - 1:
                self._matrix[pos[0]][pos[1]] = 2
                pos = (pos[0] + 1, pos[1])
            elif self._matrix[pos[0]][pos[1] - 1] == wave_l - 1:
                self._matrix[pos[0]][pos[1]] = 2
                pos = (pos[0], pos[1] - 1)
            elif self._matrix[pos[0]][pos[1] + 1] == wave_l - 1:
                self._matrix[pos[0]][pos[1]] = 2
                pos = (pos[0], pos[1] + 1)
            wave_l -= 1
        self._matrix[pos[0]][pos[1]] = 2
        for i in range(self._act_height):
            for j in range(self._act_width):
                if self._matrix[i][j] > 2:
                    self._matrix[i][j] = 0

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
                if self._player_2.get_pos() == (i, j):
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
