from games.go.action import GoAction
from games.go.player import GoPlayer
from games.go.state import GoState


class HumanGoPlayer(GoPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_user_input(self, prompt: str) -> int:
        while True:
            try:
                user_input = input(prompt)
                return int(user_input)
            except ValueError:
                print("Entrada inválida. Por favor, insira um número inteiro válido.")

    def get_action(self, state: GoState):
        state.display()

        while True:
            pass_input = input("Digite 'p' para passar a jogada ou 'm' para fazer uma jogada: ")

            if pass_input.lower() == 'p':
                action = GoAction(is_pass=True)
            elif pass_input.lower() == 'm':
                x = self.get_user_input(f"Player {state.get_acting_player()}, escolha uma coluna: ")
                y = self.get_user_input(f"Player {state.get_acting_player()}, escolha uma linha: ")

                if x is not None and y is not None:
                    action = GoAction(x, y)
                else:
                    print("Valores de coluna e linha inválidos, tente novamente.")
                    continue
            else:
                print("Entrada inválida, tente novamente.")
                continue

            if state.validate_action(action):
                return action
            else:
                print("Jogada inválida, tente novamente.")

    def event_action(self, pos: int, action, new_state: GoState):
        # ignore
        pass

    def event_end_game(self, final_state: GoState):
        # ignore
        pass
