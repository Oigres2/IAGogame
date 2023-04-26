from games.game_simulator import GameSimulator
from games.go.players.human import HumanGoPlayer
from games.go.players.random import RandomGoPlayer
from games.go.players.minimax import MinimaxGoPlayer
from games.go.players.greedy import GreedyGoPlayer
from games.go.simulator import GoSimulator


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()

def main():
    print("ESTG IA Games Simulator")

    num_iterations = 1


    ttt_simulations = [
        {
            "name": "Go - Human VS Human",
            "player1": RandomGoPlayer("Human"),
            "player2": RandomGoPlayer("Greedy")
        }  #  ,
        # {
        #     "name": "Go - Random VS Random",
        #     "player1": RandomGoPlayer("Random 1"),
        #     "player2": RandomGoPlayer("Random 2")
        # }   ,
        # {
        #     "name": "Go - Offensive VS Random",
        #     "player1": OffensiveGoPlayer("Offensive"),
        #     "player2": RandomGoPlayer("Random")
        # },
        # {
        #     "name": "Go - Defensive VS Random",
        #     "player1": DefensiveGoPlayer("Defensive"),
        #     "player2": RandomGoPlayer("Random")
        # }
    ]

    for sim in ttt_simulations:
        run_simulation(sim["name"], GoSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()
