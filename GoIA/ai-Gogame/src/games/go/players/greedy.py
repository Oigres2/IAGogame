from random import choice
from games.go.action import GoAction
from games.go.player import GoPlayer
from games.go.state import GoState
from games.state import State


class GreedyGoPlayer(GoPlayer):

    def __init__(self, name):
        self.action_count = 0
        super().__init__(name)

    def get_action(self, state: GoState):
        self.action_count += 1

        if self.action_count > 38:
            return GoAction(is_pass=True)

        valid_actions = []
        capturing_actions = []

        for i in range(state.get_num_rows()):
            for j in range(state.get_num_cols()):
                action = GoAction(i, j)
                if state.validate_action(action):
                    new_state = state.clone()
                    new_state.update(action)
                    
                    opponent = 1 if state.get_acting_player() == 0 else 0
                    captured_count = new_state._count_captured_pieces(action)
                    
                    if captured_count > 0:
                        capturing_actions.append(action)
                    else:
                        valid_actions.append(action)

        if len(capturing_actions) > 0:
            print(f"Player {state.get_acting_player()} selected a capturing action: {action.get_row()}, {action.get_col()}")
            return choice(capturing_actions)
        elif len(valid_actions) > 0:
            return choice(valid_actions)
        else:
            return GoAction(is_pass=True)
        
    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass