import random


class ModelStart:
    def __init__(self):
        self.list_base_games = [0]
        self.list_expansions = []
        self.difficulty = 1

    def toggle_base(self, base_id:int):
        if base_id in self.list_base_games:
            self.list_base_games.remove(base_id)
        else:
            self.list_base_games.append(base_id)
        return self.list_base_games


    def toggle_exp(self, exp_id:int):
        if exp_id in self.list_expansions:
            self.list_expansions.remove(exp_id)
        else:
            self.list_expansions.append(exp_id)
        return self.list_expansions


class Deck:
    def __init__(self, base_sets, expansions):
        self.cards = list(range(18))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop(0)


class ModelMain:
    def __init__(self, list_base_games, list_expansions, difficulty):
        self.list_base_games = list_base_games
        self.list_expansions = list_expansions
        self.difficulty = difficulty
        self.deck = Deck(self.list_base_games, self.list_expansions)
        self.score_cards = []
        for _ in range(3):
            self.score_cards.append(self.deck.deal())
