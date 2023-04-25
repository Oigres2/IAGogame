from typing import Optional

from games.go.action import GoAction
from games.go.result import GoResult
from games.state import State
from copy import deepcopy


class GoState(State):
    EMPTY_CELL = -1

    def __init__(self, num_rows: int = 19):
        super().__init__()

        if num_rows < 9:
            raise Exception("the number of rows must be 9 or over")

        """
        the dimensions of the board
        """
        self.__num_rows = num_rows
        self.__num_cols = num_rows

        """
        the grid
        """
        self.__grid = [[GoState.EMPTY_CELL for _i in range(self.__num_rows)] for _j in range(self.__num_cols)]

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1

        """
        the index of the current acting player
        """
        self.__acting_player = 0

        """
        determine if a winner was found already 
        """
        self.__has_winner = False
        
        self.__black_score = 0
        
        self.__white_score = 0
        
        self.__consecutive_passes = 0
        
        self.__groups = {}
        

    def __count_territory(self, player):
        territory_count = 0
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if self.__grid[row][col] == player:
                    territory_count += 1
        return territory_count

    def __check_winner(self):
        black_score = self.__count_territory(0)
        white_score = self.__count_territory(1) + 6.5  # Komi

        if black_score > white_score:
            return 0, black_score, white_score
        elif white_score > black_score:
            return 1, black_score, white_score
        else:
            return "DRAW", black_score, white_score

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: GoAction) -> bool:
        if action.is_pass():
            return True
        
        col = action.get_col()
        row = action.get_row()
        player = self.__acting_player
    
        # valid column
        if col < 0 or col >= self.__num_cols:
            return False
        # valid row
        if row < 0 or row >= self.__num_rows:
            return False

        # check empty or full
        if self.__grid[row][col] != GoState.EMPTY_CELL:
            return False
        
        copy_grid = deepcopy(self.__grid)
        copy_grid[row][col] = player
        if not self.is_legal_position(copy_grid, player):
            return False

        return True
    
    def get_adjacent_positions(self, row: int, col: int):
        adjacent_positions = []
        if row > 0:
            adjacent_positions.append((row - 1, col))
        if row < self.__num_rows - 1:
            adjacent_positions.append((row + 1, col))
        if col > 0:
            adjacent_positions.append((row, col - 1))
        if col < self.__num_cols - 1:
            adjacent_positions.append((row, col + 1))
        return adjacent_positions

    def get_group(self, grid, row: int, col: int):
        color = grid[row][col]
        if color == GoState.EMPTY_CELL:
            return []

        visited = set()
        group = [(row, col)]

        for r, c in group:
            visited.add((r, c))
            for adj_row, adj_col in self.get_adjacent_positions(r, c):
                if (adj_row, adj_col) not in visited and grid[adj_row][adj_col] == color:
                    group.append((adj_row, adj_col))
                    visited.add((adj_row, adj_col))

        return group

    def count_liberties(self, grid, group):
        liberties = set()
        for row, col in group:
            for adj_row, adj_col in self.get_adjacent_positions(row, col):
                if grid[adj_row][adj_col] == GoState.EMPTY_CELL:
                    liberties.add((adj_row, adj_col))
        return len(liberties)

    def is_legal_position(self, grid, player):
        opponent = 0 if player == 1 else 1
        own_groups_to_remove = []
        opponent_groups_to_remove = []
        

        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if grid[row][col] == player:
                    group = self.get_group(grid, row, col)
                    if group not in own_groups_to_remove and self.count_liberties(grid, group) == 0:
                        own_groups_to_remove.append(group)
                elif grid[row][col] == opponent:
                    group = self.get_group(grid, row, col)
                    if group not in opponent_groups_to_remove and self.count_liberties(grid, group) == 0:
                        opponent_groups_to_remove.append(group)

        if len(own_groups_to_remove) > 1:
            return False

        if len(own_groups_to_remove) == 1 and len(opponent_groups_to_remove) == 0:
            return False

        if len(own_groups_to_remove) == 0 and len(opponent_groups_to_remove) == 0:
            if self.clone is not None and grid == self.clone:
                return False

        return True

    def update(self, action: GoAction):
        col = action.get_col()
        row = action.get_row()

        # If both players passed, check for a winner
        if action.is_pass():
            self.__consecutive_passes += 1
            print(f"Player {self.__acting_player} passou o turno")
            if self.__consecutive_passes >= 2:
                winner, black_score, white_score = self.__check_winner()
                self.__has_winner = True
                print(f"O jogo terminou. Vencedor: Player {winner}, Pontuação do jogador preto (Player 0): {black_score}, Pontuação do jogador branco (Player 1): {white_score}")
        else:
            self.__consecutive_passes = 0
            # update chosen coordinates
            if self.__grid[row][col] < 0:
                self.__grid[row][col] = self.__acting_player
            
            new_group_id = self.__find_group_id(row, col)
            new_group = self.get_group(self.__grid, row, col)
            self.__add_group_to_groups(tuple(new_group_id), new_group)

            # remove opponent's groups with zero liberties
            opponent = 1 if self.__acting_player == 0 else 0
            captured_stones = self.__remove_opponent_groups_with_zero_liberties(row, col, opponent)

            # update player's score
            if self.__acting_player == 0:
                self.__black_score += captured_stones
            else:
                self.__white_score += captured_stones

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1
        
        self.__update_groups()
        
    def __remove_opponent_groups_with_zero_liberties(self, row, col, opponent):
        captured_stones = 0
        checked_groups = set()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if not (0 <= nr < self.__num_rows and 0 <= nc < self.__num_cols):
                continue
            if self.__grid[nr][nc] == opponent:
                group_id = self.__find_group_id(nr, nc)
                if group_id not in checked_groups:
                    group_id = tuple(group_id)  # Converta group_id para uma tupla
                    group = self.__groups[group_id]
                    if self.__group_liberties(group) == 0:
                        captured_stones += self.__remove_group(group_id)
                    checked_groups.add(group_id)
        return captured_stones
    
    def __remove_group(self, group_id):
        group = self.__groups[group_id]
        stone_count = len(group)
        for row, col in group:
            self.__grid[row][col] = GoState.EMPTY_CELL
        del self.__groups[group_id]
        return stone_count
    
    def __group_liberties(self, group):
        liberties = set()
        for row, col in group:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if (0 <= nr < self.__num_rows) and (0 <= nc < self.__num_cols) and self.__grid[nr][nc] == GoState.EMPTY_CELL:
                    liberties.add((nr, nc))
        return len(liberties)
    
    def __find_group_id(self, row, col, visited=None):
        if visited is None:
            visited = set()

        if (row, col) in visited:
            return None

        visited.add((row, col))
        stone = self.__grid[row][col]

        if stone == GoState.EMPTY_CELL:
            return None

        # Verificar se a posição (row, col) pertence a algum grupo existente
        for group_id, group in self.__groups.items():
            if (row, col) in group:
                return group_id

        group_id = {(row, col)}

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc

            if (0 <= nr < self.__num_rows) and (0 <= nc < self.__num_cols):
                if self.__grid[nr][nc] == stone:
                    neighbor_group = self.__find_group_id(nr, nc, visited)
                    if neighbor_group is not None:
                        group_id.update(neighbor_group)

        return group_id
    
    def __add_group_to_groups(self, group_id, group):
        self.__groups[group_id] = group
    
    def __update_groups(self):
        new_groups = {}
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if self.__grid[row][col] != GoState.EMPTY_CELL:
                    group_id = self.__find_group_id(row, col)
                    if group_id not in new_groups:
                        new_groups[group_id] = {(row, col)}
                    else:
                        new_groups[group_id].add((row, col))
        self.__groups = new_groups   

    def __display_cell(self, row, col):
        print({
                  0: 'X',
                  1: 'O',
                  GoState.EMPTY_CELL: ' '
              }[self.__grid[row][col]], end="")

    def __display_numbers(self):
        for col in range(0, self.__num_cols):
            print('  ', end="")
            print(col, end="")
        print("")

    def __display_separator(self):
        for col in range(0, self.__num_cols):
            print("---", end="")
        print("-")

    def display(self):
        self.__display_numbers()
        self.__display_separator()

        for row in range(0, self.__num_rows):
            print(row, end="")
            print('|', end="")
            for col in range(0, self.__num_cols):
                self.__display_cell(row, col)
                print(' |', end="")
            print("")
            self.__display_separator()

        self.__display_numbers()
        print("")

    def __is_full(self):
        return self.__turns_count > (self.__num_cols * self.__num_rows)

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = GoState(self.__num_rows)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[GoResult]:
        if self.__has_winner:
            return GoResult.LOOSE if pos == self.__acting_player else GoResult.WIN
        if self.__is_full():
            return GoResult.DRAW
        return None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass
        
    def get_possible_actions(self):
        grid: list[list[int]] = []
        for i in range(self.get_num_rows()):
            for j in range(self.get_num_cols()):
                grid.append([i, j])

        return list(filter(
            lambda action: self.validate_action(action),
            map(
                lambda pos: GoAction(pos[0], pos[1]),
                grid))
        )

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
