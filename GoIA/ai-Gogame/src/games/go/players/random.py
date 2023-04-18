from random import randint

from games.go.action import GoAction
from games.go.player import GoPlayer
from games.go.state import GoState
from games.state import State


class RandomGoPlayer(GoPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: GoState):
        return GoAction(randint(0, state.get_num_cols()), randint(0, state.get_num_rows()))

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
