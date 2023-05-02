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

    while True:
        print("\n----- MAIN MENU -----\n")
        print("1. Play Go")
        print("2. Go rules")
        print("0. Close program")
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                print("\n----- PLAY GO -----\n")
                print("1. Human VS Human")
                print("2. Human VS Computer")
                print("3. Computer VS Computer")
                print("0. Go back")
                game_choice = input("Enter your choice: ")

                if game_choice == "1":
                    run_simulation("Go - Human VS Human", GoSimulator(HumanGoPlayer("Human 1"), HumanGoPlayer("Human 2")), 1)
                elif game_choice == "2":
                    while True:
                        print("\n----- SELECT DIFFICULTY -----\n")
                        print("1. Easy (Random)")
                        print("2. Medium (Greedy)")
                        print("3. Hard (Minimax)")
                        print("0. Go back")
                        difficulty_choice = input("Enter your choice: ")

                        if difficulty_choice == "1":
                            player = RandomGoPlayer("Random")
                        elif difficulty_choice == "2":
                            player = GreedyGoPlayer("Greedy")
                        elif difficulty_choice == "3":
                            player = MinimaxGoPlayer("Minimax")
                        elif difficulty_choice == "0":
                            break
                        else:
                            print("Invalid choice, please try again.")
                            continue

                        run_simulation(f"Go - Human VS {player.get_name}", GoSimulator(HumanGoPlayer("Human"), player), 1)
                        break
                elif game_choice == "3":
                    while True:
                        print("\n----- SELECT DIFFICULTY -----\n")
                        print("1. Easy (Random)")
                        print("2. Medium (Greedy)")
                        print("3. Hard (Minimax)")
                        print("0. Go back")
                        difficulty_choice = input("Enter your choice: ")

                        if difficulty_choice == "1":
                            player1 = RandomGoPlayer("Random 1")
                            player2 = RandomGoPlayer("Random 2")
                        elif difficulty_choice == "2":
                            player1 = GreedyGoPlayer("Greedy 1")
                            player2 = GreedyGoPlayer("Greedy 2")
                        elif difficulty_choice == "3":
                            player1 = MinimaxGoPlayer("Minimax 1")
                            player2 = MinimaxGoPlayer("Minimax 2")
                        elif difficulty_choice == "0":
                            break
                        else:
                            print("Invalid choice, please try again.")
                            continue

                        run_simulation(f"Go - {player1.get_name} VS {player2.get_name}", GoSimulator(player1, player2), 1)
                        break
                elif game_choice == "0":
                    break
                else:
                    print("Invalid choice, please try again.")
        elif choice == "2":
            print("\n----- GO RULES -----\n")
            print(f"1- O jogo é jogado em um tabuleiro de 9x9")
            print(f"2- A primeira jogada é feita pelo jogador com as pedras pretas (X), a seguir jogará o jogador com as brancas (O), e depois ambos os jogadores alternarão suas jogadas.")
            print(f"3- Uma jogada consiste em colocar uma pedra numa das intersecções vazias no tabuleiro, incluindo as bordas.")
            print(f"4- Uma vez introduzidas no jogo, as pedras não são movidas, mas podem ser capturadas pelo oponente e removidas do tabuleiro.")
            print(f"5- Uma pedra é capturada e removida do tabuleiro quando todas as intersecções diretamente adjacentes a ela (suas liberdades) são ocupadas por pedras do oponente. O mesmo aplica-se a grupos de pedras solidamente conectadas.")
            print(f"6- Via de regra, uma jogada pode ser feita em qualquer intersecção vazia no tabuleiro, mas há exceções: Uma pedra não pode ser colocada numa intersecção cujas liberdades, as intersecções adjacentes a ela, já estejam ocupadas por pedras do oponente ou se introduzi-la ali resultaria na captura de outras pedras da própria cor.")
            print(f"7- Um jogador pode passar sua vez a qualquer momento.")
            print(f"8- A partida termina quando ambos os jogadores passam a vez consecutivamente.")
            print(f"9- Vence o jogador com a maior pontuação.")
        elif choice == "0":
            print("Closing program. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
