import random
import abc

STARTING_FUNDS = 50
BET_SIZE = 10
DECK_SIZE = 52
AGGRESSIVE_THRESHOLD = 17
AGGRESSIVE_ACE_THRESHOLD = 20
CONSERVATIVE_THRESHOLD = 15


class PlayStyle():
    def play(self, score, aces):
        raise NotImplementedError()


class PlayAggressive(PlayStyle):
    def __init__(self):
        self.threshold = AGGRESSIVE_THRESHOLD

    def play(self, score, contains_ace):
        if score <= self.threshold or (score <= AGGRESSIVE_ACE_THRESHOLD and contains_ace):
            return True
        else:
            return False


class PlayConservative(PlayStyle):
    def __init__(self):
        self.threshold = CONSERVATIVE_THRESHOLD

    def play(self, score, contains_ace):
        if score <= self.threshold:
            return True
        else:
            return False


class Player:
    def __init__(self, deck, strategy=None):
        self.deck = deck
        self.wins = 0
        if strategy is not None:
            self.strategy = strategy

    def play(self):
        return self.strategy.play(self.total_score(), self.contains_ace())

    def reset_deck(self, deck):
        self.deck = deck

    def get_deck(self, index):
        return self.deck[index].name

    def get_last(self):
        return self.get_deck(len(self.deck) - 1)

    def draw_deck(self, card):
        self.deck.append(card)

    def contains_ace(self):
        b = False
        for c in self.deck:     # this covers the "flex" quality of an Ace.
            if c.value == 11:
                b = True
        return b

    def total_score(self):
        i = 0
        for c in self.deck:
            i += c.value
        for c in self.deck:     # this covers the "flex" quality of an Ace.
            if i > 21 and c.value == 11:
                c.value = 1
                i -= 10
        return i


class Deck:

    def __init__(self):
        self.cards = []
        self.reset()

    def draw(self):
        return self.cards.pop()

    def reset(self):
        self.cards = []
        for n in range(DECK_SIZE):
            self.cards.append(Card((n % 13) + 1))
        random.shuffle(self.cards)


class Card:
    def __init__(self, value):
        if value == 1:
            self.value = 11
            self.name = "Ace (1 or 11)"
        elif value == 11:
            self.value = 10
            self.name = "Jack (10)"
        elif value == 12:
            self.value = 10
            self.name = "Queen (10)"
        elif value == 13:
            self.value = 10
            self.name = "King (10)"
        else:
            self.value = value
            self.name = value


class Play:
    def __init__(self, playstyle):
        self.m = Deck()
        self.p = Player([self.m.draw(), self.m.draw()], playstyle)
        self.d = Player([self.m.draw()])

    def simulate(self, repetitions):
        for r in range(repetitions):
            self.m.reset()
            self.p.reset_deck([self.m.draw(), self.m.draw()])
            self.d.reset_deck([self.m.draw()])
            while self.p.play():
                self.p.draw_deck(self.m.draw())
            if self.p.total_score() == 21:
                p_win = True
            elif self.p.total_score() > 21:
                p_win = False
            else:
                while self.d.total_score() < 21 and self.d.total_score() < self.p.total_score():
                    self.d.draw_deck(self.m.draw())
                if 21 >= self.d.total_score() >= self.p.total_score():
                    p_win = False
                else:
                    p_win = True

            if p_win:
                self.p.wins += 1
            else:
                self.d.wins += 1

        return " final win rate: %s:%s. GG!" % (self.p.wins, self.d.wins)


aGame = Play(PlayAggressive())
print("Aggressive player A's" + aGame.simulate(5000))
cGame = Play(PlayConservative())
print("Conservative player A's" + cGame.simulate(5000))
