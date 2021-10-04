class RPSGame:

    @staticmethod
    def results_print(players_choices: list) -> str:
        """Prints the result of the game: choices of players"""
        return f'{players_choices[0][1]}: {players_choices[0][2]}\n' \
               f'{players_choices[1][1]}: {players_choices[1][2]}'

    @staticmethod
    def get_winner(players_choices: list) -> tuple:
        """Defines the winner or draw"""
        choices = list(map(lambda x: x[:][2], players_choices))
        ids = list(map(lambda x: x[:][0], players_choices))
        if len(set(choices)) == 1:
            winner = 0
        else:
            if set(choices) == {'stone', 'scissors'}:
                winner = ids[choices.index('stone')]
            elif set(choices) == {'stone', 'paper'}:
                winner = ids[choices.index('paper')]
            else:
                winner = ids[choices.index('scissors')]
            ids.remove(winner)
        return winner, ids[0]
