import random
import abc

STARTING_FUNDS = 50
BET_SIZE = 10
DECK_SIZE = 52
AGGRESSIVE_THRESHOLD = 16
CONSERVATIVE_THRESHOLD = 13


class PlayStyle():
    def play(self, score):
        raise NotImplementedError()


class PlayAggressive(PlayStyle):
    def __init__(self):
        self.threshold = AGGRESSIVE_THRESHOLD

    def play(self, score):
        if score <= self.threshold:
            return True
        else:
            return False


class PlayConservative(PlayStyle):
    def __init__(self):
        self.threshold = CONSERVATIVE_THRESHOLD

    def play(self, score):
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
        return self.strategy.play(self.total_score())

    def reset_deck(self, deck):
        self.deck = deck

    def get_deck(self, index):
        return self.deck[index].name

    def get_last(self):
        return self.get_deck(len(self.deck) - 1)

    def draw_deck(self, card):
        self.deck.append(card)

    def total_score(self):
        i = 0
        for c in self.deck:
            i += c.value
        for c in self.deck:     # this covers the "flex" quality of an Ace.
            if i > 21 and c.value == 11:
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


m = Deck()
p = Player([m.draw(), m.draw()], PlayConservative())
d = Player([m.draw()])

for r in range(1000):
    m.reset()
    p.reset_deck([m.draw(), m.draw()])
    d.reset_deck([m.draw()])
    you_win = True
    print("Your first card is: %s" % (p.get_deck(0)))
    print("Your second card is: %s" % (p.get_deck(1)))
    print("Dealer's first card is: %s" % (d.get_deck(0)))
    while p.play():
        p.draw_deck(m.draw())
        print("You drew: %s, for a total of %s points." % (p.get_last(), p.total_score()))

    if p.total_score() == 21:
        you_win = True
    elif p.total_score() > 21:
        you_win = False
    else:
        while d.total_score() < 21 and d.total_score() < p.total_score():
            d.draw_deck(m.draw())
            print("Dealer draws: %s, for a total of %s points." % (d.get_last(), d.total_score()))
        print("Dealer's total score is: %s" % (d.total_score()))
        print("Your total score is: %s" % (p.total_score()))
        if 21 >= d.total_score() >= p.total_score():
            you_win = False
        else:
            you_win = True

    if you_win:
        p.wins += 1
        print("You win! Your wins: %s" % p.wins)
    else:
        d.wins += 1
        print("You lose! Your wins: %s" % p.wins)

print("Your final win rate: %s:%s. GG!" % (p.wins, d.wins))
