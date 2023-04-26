from random import choice
from games.go.action import GoAction
from games.go.player import GoPlayer
from games.go.state import GoState
from games.state import State


class GreedyGoPlayer(GoPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: GoState):
        valid_actions = []
        for i in range(state.get_num_rows()):
            for j in range(state.get_num_cols()):
                action = GoAction(i, j)
                if state.validate_action(action):
                    valid_actions.append(action)

        if len(valid_actions) <= 0:
            return GoAction(is_pass = True)

        # Avalia o ganho de cada ação válida e seleciona a melhor
        best_gain = -1
        best_actions = []

        for action in valid_actions:
            new_state = state.clone()
            new_state.update(action)

            opponent = 1 if state.get_acting_player() == 0 else 0
            captured_count = new_state._count_territory(opponent)
            gain = captured_count - state._count_territory(opponent)

            if gain > best_gain:
                best_gain = gain
                best_actions = [action]
            elif gain == best_gain:
                best_actions.append(action)

        if best_actions:
            return choice(best_actions)
        else:
            return GoAction(is_pass=True)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass