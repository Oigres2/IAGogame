from games.go.player import GoPlayer
from games.go.state import GoState
from games.game_simulator import GameSimulator


class GoSimulator(GameSimulator):

    def __init__(self, player1: GoPlayer, player2: GoPlayer, num_rows: int = 9):
        super(GoSimulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the connect4 grid
        """
        self.__num_rows = num_rows

    def init_game(self):
        return GoState(self.__num_rows)

    def before_end_game(self, state: GoState):
        # ignored for this simulator
        pass

    def end_game(self, state: GoState):
        # ignored for this simulator
        pass
