from random import randint, random

from games.go.action import GoAction
from games.go.player import GoPlayer
from games.go.state import GoState
from games.state import State


class RandomGoPlayer(GoPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: GoState):
        # Escolha aleatoriamente entre passar e colocar uma peça
        if random() < 0.1:  # 10% de chance de passar
            return GoAction(-1, -1)  # Ação de passar o turno
        else:
            # Tente colocar peças aleatórias até encontrar uma ação válida
            while True:
                action = GoAction(randint(0, state.get_num_cols() - 1), randint(0, state.get_num_rows() - 1))
                if state.validate_action(action):
                    return action

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
