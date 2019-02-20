import random

STARTING_FUNDS = 50
BET_SIZE = 10
DECK_SIZE = 52


class Player:
    def __init__(self, deck):
        self.deck = deck
        self.funds = STARTING_FUNDS

    def reset_deck(self, deck):
        self.deck = deck

    def get_deck(self, index):
        return self.deck[index].name

    def get_last(self):
        return self.get_deck(len(self.deck) - 1)

    def draw_deck(self, deck):
        self.deck.append(deck)

    def total_score(self):
        i = 0
        for c in self.deck:
            i += c.value
        for c in self.deck:     # this covers the "flex" quality of an Ace.
            if i > 21 and c.value == 11:
                i -= 10
        return i


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


def draw():
    i = random.randint(0, DECK_SIZE)
    card = Card((i % 13) + 1)
    return card


p = Player([draw(), draw()])
d = Player([draw()])
keepGoing = 'y'

while keepGoing[0].lower() == 'y':
    p.reset_deck([draw(), draw()])
    d.reset_deck([draw()])
    you_win = True
    print("Your first card is: %s" % (p.get_deck(0)))
    print("Your second card is: %s" % (p.get_deck(1)))
    print("Dealer's first card is: %s" % (d.get_deck(0)))
    answer = raw_input("Hit or stand?")
    while answer[0].lower() == 'h':
        p.draw_deck(draw())
        print("You drew: %s, for a total of %s points." % (p.get_last(), p.total_score()))
        if p.total_score() <= 21:
            answer = raw_input("Hit or stand?")
        else:
            answer = 's'

    if p.total_score() == 21:
        you_win = True
    elif p.total_score() > 21:
        you_win = False
    else:
        while d.total_score() < 21 and d.total_score() < p.total_score():
            d.draw_deck(draw())
            print("Dealer draws: %s, for a total of %s points." % (d.get_last(), d.total_score()))
        print("Dealer's total score is: %s" % (d.total_score()))
        print("Your total score is: %s" % (p.total_score()))
        if 21 >= d.total_score() >= p.total_score():
            you_win = False
        else:
            you_win = True

    if you_win:
        p.funds += BET_SIZE
        d.funds -= BET_SIZE
        print("You win! Your funds: $%.2f" % p.funds)
    else:
        p.funds -= BET_SIZE
        d.funds += BET_SIZE
        print("You lose! Your funds: $%.2f" % p.funds)

    keepGoing = raw_input("Try again?")

print("Your final score: $%.2f. GG!" % p.funds)
