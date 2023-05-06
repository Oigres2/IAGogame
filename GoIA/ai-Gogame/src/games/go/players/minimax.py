import math
import random

from games.go.player import GoPlayer
from games.go.result import GoResult
from games.go.state import GoState
from games.state import State
from games.go.action import GoAction


class MinimaxGoPlayer(GoPlayer):

    def __init__(self, name):
        self.action_count = 0
        super().__init__(name)

    '''
    This heuristic will simply count the maximum number of consecutive pieces that the player has
    It's not a great heuristic as it doesn't take into consideration a defensive approach
    '''

    def __heuristic(self, state: GoState):
        player_score = state._count_captured_pieces(self.get_current_pos())
        opponent_score = state._count_captured_pieces(1 - self.get_current_pos())

        player_territory = 0
        opponent_territory = 0

        player_potential_captures = 0
        opponent_potential_captures = 0

        for i in range(state.get_num_rows()):
            for j in range(state.get_num_cols()):
                cell = state.get_grid()[i][j]
                neighbours = state.get_adjacent_positions(i, j)

                if cell == -1:  # if the cell is empty
                    if all(state.get_grid()[n[0]][n[1]] == self.get_current_pos() for n in neighbours):
                        player_territory += 1
                    elif all(state.get_grid()[n[0]][n[1]] == 1 - self.get_current_pos() for n in neighbours):
                        opponent_territory += 1
                elif cell == self.get_current_pos():  # if the cell is owned by the player
                    if any(state.get_grid()[n[0]][n[1]] == 1 - self.get_current_pos() for n in neighbours):
                        player_potential_captures += 1
                elif cell == 1 - self.get_current_pos():  # if the cell is owned by the opponent
                    if any(state.get_grid()[n[0]][n[1]] == self.get_current_pos() for n in neighbours):
                        opponent_potential_captures += 1

        return (player_score + player_territory + player_potential_captures) - (opponent_score + opponent_territory + opponent_potential_captures)

    def minimax(self, state: GoState, depth: int, alpha: int = -math.inf, beta: int = math.inf,
                is_initial_node: bool = True):
        # first we check if we are in a terminal node (victory, draw or loose)
        if state.is_finished():
            return {
                GoResult.WIN: 40,
                GoResult.LOOSE: -40,
                GoResult.DRAW: 0
            }[state.get_result(self.get_current_pos())]

        # if we reached the maximum depth, we will return the value of the heuristic
        if depth == 0:
            return self.__heuristic(state)

        # if we are the acting player
        if self.get_current_pos() == state.get_acting_player():
            # very small integer
            value = -math.inf
            selected_action = None

            for action in state.get_possible_actions():
                new_state = state.clone()
                new_state.update(action)
                pre_value = value
                value = max(value, self.minimax(new_state, depth - 1, alpha, beta, False))
                if value > pre_value:
                    selected_action = action
                if value > beta:
                    break
                alpha = max(alpha, value)

            return selected_action if is_initial_node else value

        # if it is the opponent's turn
        else:
            value = math.inf
            for action in state.get_possible_actions():
                new_state = state.clone()
                new_state.update(action)
                value = min(value, self.minimax(new_state, depth - 1, alpha, beta, False))
                if value < alpha:
                    break
                beta = min(beta, value)
            return value


    def get_action(self, state: GoState):
        self.action_count += 1

        if self.action_count > 39:
            return GoAction(is_pass=True)
        
        # Introduce some randomness in the initial moves
        if self.action_count < 3:
            possible_actions = state.get_possible_actions()
            return random.choice(possible_actions)
        
        return self.minimax(state, 2)
    
    def event_new_game(self):
        super().event_new_game()
        self.action_count = 0

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
