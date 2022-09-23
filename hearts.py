import random
trials = 10000

class Deck:
    def __init__(self):
        self.cards = self.make_deck()
        self.size = len(self.cards)
    
    def make_deck(self):
        suits = ["C", "D", "H", "S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = []
        for suit in suits:
            for rank in ranks:
                card = suit + rank
                deck.append(card)
        return deck

    def shuffle(self):
        random.shuffle(self.cards)
        return  self.cards
    
    def draw(self):
        if self.size == 0:
            return "Deck is empty"
        else:
            self.size -= 1
            return self.cards.pop()

    def get_hand(self):
        hand = []
        for i in range(13):
            card = self.draw()
            hand.append(card)
        return hand

#number of spades in a hand
def spade_count(hand):
    spade = 0
    for card in hand:
        rank = card[0]
        if rank == "S":
            spade += 1
    return spade

#monte carlo on average hand

#over 1000 trials, number of trials with 1 spade, 2 spades, 3 spades, 4 spade, etc

hands = dict()
for trial in range(trials):
    attempt = Deck()
    attempt.shuffle()
    hand = attempt.get_hand()
    spades_in_hand = spade_count(hand)
    #record number of
    if spades_in_hand in hands:
        hands[spades_in_hand] += 1
    else:
        hands[spades_in_hand] = 1

def sort_hand(hands):
    d = dict()
    h = sorted(hands)
    for k in h:
        d[k] = hands[k]
    return d

hands = sort_hand(hands)

def get_distribution(hands, num_trials):
    d = dict()
    for k in hands:
        decimal = hands[k] / num_trials
        d[k] = decimal
    return d

print("in a game of heart, the player's hand probability of holding n spade is:")
spade_distribution = get_distribution(hands, trials)
print(spade_distribution)

def get_mean(distribution):
    mean = 0
    for k in distribution:
        mean += k * distribution[k]
    return mean

mean = get_mean(spade_distribution)
print(f"the mean number of spades is {mean}")


#how many turns does it usually take for a person to run out of rank?

#set up: randomize 4 hands at start of a game


#game_hands is a 2D list, [hands]
def get_turns_run_out(game_hands):
    turns = 13
    for hand in game_hands:
        player_card = spade_count(hand)
        if player_card < turns:
            turns = player_card
    return turns + 1

turns = dict()  #number of turns to run out
print("\n\ngetting number of turns for a player to void")
for trial in range(trials):
    d = Deck()
    d.shuffle()
    game_hands = []
    for h in range(4):
        player = d.get_hand()
        game_hands.append(player)
    turn_out = get_turns_run_out(game_hands)
    if turn_out not in turns:
        turns[turn_out] = 1
    else:
        turns[turn_out] += 1

turns = sort_hand(turns)


#how many turns does it take to draw out queen of spades?

print("in a game of heart, the m turns needed to get a void is:")
turn_distribution = get_distribution(turns, trials)
print(f"the turn distribution is: \n{turn_distribution}")

turn_mean = get_mean(turn_distribution)
print(f"the mean turn is {turn_mean}")

#given n rounds: P(1) P(2) P(3) P(4)

#after 1 turn
#P(1 | !1) = P(1 & !0) / P(!0) = P(1) / P(!0)
#P(2 | !1) = P(2 & !0) / P(!0) = P(2) / P(!0)
#P(3 | !1) = P(3 & !0) / P(!0) = P(3) / P(!0)
#P(4 | !1) = P(4 & !0) / P(!0) = P(4) / P(!0)

#

