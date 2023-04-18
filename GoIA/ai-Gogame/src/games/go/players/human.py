from games.go.action import GoAction
from games.go.player import GoPlayer
from games.go.state import GoState


class HumanGoPlayer(GoPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: GoState):
        state.display()
        print(f"Player {state.get_acting_player()}, choose a column: ")
        x = int(input())
        print(f"Player {state.get_acting_player()}, choose a row: ")
        y = int(input())

        while True:
            # noinspection PyBroadException
            try:
                return GoAction(x, y)
            except Exception:
                continue

    def event_action(self, pos: int, action, new_state: GoState):
        # ignore
        pass

    def event_end_game(self, final_state: GoState):
        # ignore
        pass
