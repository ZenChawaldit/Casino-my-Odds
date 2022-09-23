import random

####Assumptions
total_games = 100000
player_return = 1
banker_non_six_return = 1
banker_six_return = 0.5
tie_return = 8
tiger_tie_return = 35
tiger_return = 20
small_tiger_return = 22
big_tiger_return = 50
print("\n\nStarting Baccarat Simulation")
print(f'''
Assumptions:
Total Games: {total_games}
Pay Offs
Player: {player_return} time
Banker: {banker_non_six_return} time
Banker with 6: {banker_six_return} time
Tie: {tie_return} times
Tiger Tie: {tiger_tie_return} times
Small Tiger: {small_tiger_return} times
Big Tiger: {big_tiger_return} times
Tiger: {tiger_return} times''')


####Program
class Deck:
    def __init__(self, size):
        self.cards = self.make_deck(size)
        self.size = len(self.cards)
        
    def make_deck(self, size):
        suits = ["C", "D", "H", "S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = []
        for d in range(size):
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
            return False
        else:
            self.size -= 1
            return self.cards.pop()

def get_pok_score(hand):
    score = 0
    score_chart = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":0,
                    "J":0, "Q":0, "K":0, "A":1}
    for card in hand:
        rank = card[1:]
        score += score_chart[rank]
    return score % 10


#rule: 

#1. check if there's any pok
#2. check if player can draw
#3. check if banker can draw
#4. get score


#small tiger: banker gets score of 6 with 2 cards
def is_small_tiger(hand):
    return len(hand) == 2 and get_pok_score(hand) == 6

#big tiger: banker gets score of 6 with 3 cards
def is_big_tiger(hand):
    return len(hand) == 3 and get_pok_score(hand) == 6

def is_tiger(hand):
    return is_big_tiger(hand) or is_small_tiger(hand)

#tie: score tie
def is_tie(player, banker):
    return get_pok_score(player) == get_pok_score(banker)

#twin tiger: pairs on both sides
def is_tiger_tie(player, banker):
    return is_tie(player, banker) and is_tiger(banker)
 
# returns the final hand
def play(deck):
    #starting hand
    player = [deck.draw(), deck.draw()]
    banker = [deck.draw(), deck.draw()]

    #edge case, run out of card, new deck and output again
    for card in player:
        if card == False:
            deck = Deck(4)
            deck.shuffle()
            return play(deck)
    for card in banker:
        if card == False:
            deck = Deck(4)
            deck.shuffle
            return play(deck)
            
    player_score = get_pok_score(player)     
    banker_score =  get_pok_score(banker)

    #check for naturals
    if banker_score in range(8,10) or player in range(8,10):
        return [player, banker]
    #player draws
    elif player_score in range(0,6):
        card = deck.draw()
        if card == False:
            deck = Deck(4)
            deck.shuffle()
            return play(deck)
        else:
            player.append(card)
            player_score = get_pok_score(player)
    
    #bankers draws
    if banker_score in range(0,3):
        card = deck.draw()
        if card == False:
            deck = Deck(4)
            deck.shuffle()
            return play(deck)
        else:
            banker.append(card)
            banker_score = get_pok_score(player)

    elif (banker_score == 3 and player_score != 8):
        card = deck.draw()
        if card == False:
            deck = Deck(4)
            deck.shuffle()
            return play(deck)
        else:
            banker.append(card)
            banker_score = get_pok_score(player)

    elif (banker_score == 4 and player_score in range(2,8)):
        card = deck.draw()
        if card == False:
            deck = Deck(4)
            deck.shuffle()
            return play(deck)
        else:
            banker.append(card)
            banker_score = get_pok_score(player)
    elif (banker_score == 5 and player_score in range(4,8)):
        card = deck.draw()
        if card == False:
            deck = Deck(4)
            return play(deck)
        else:
            banker.append(card)
            banker_score = get_pok_score(player) 
    elif (banker_score == 6 and player_score in range(6,8)):
        card = deck.draw()
        if card == False:
            deck = Deck(4)
            return play(deck)
        else:
            banker.append(card)
            banker_score = get_pok_score(player)
    #banker stays
    return [player, banker]

deck = Deck(4)
deck.shuffle()

player_win = 0
banker_win = 0
tie = 0
tiger_tie = 0
small_tiger = 0
big_tiger = 0
tiger = 0
for i in range(total_games):
    game = play(deck)
    player_hand = game[0]
    banker_hand = game[1]
    player_score = get_pok_score(player_hand)
    banker_score = get_pok_score(banker_hand)
    if player_score > banker_score:
        player_win += 1
    elif player_score < banker_score:
        banker_win += 1
        if is_small_tiger(banker_hand):
            small_tiger += 1
            tiger += 1
        elif is_big_tiger(banker_hand):
            big_tiger += 1
            tiger += 1
    else:
        tie += 1
        if is_tiger_tie(player_hand, banker_hand):
            tiger_tie += 1

def percentage(part, whole):
    percent = 100 * float(part) / float(whole)
    return str(percent) + "%"

###get win rates
player_win_rate = percentage(player_win, total_games)
bank_win_rate = percentage(banker_win, total_games)
tie_win_rate = percentage(tie, total_games)
tiger_tie_win_rate = percentage(tiger_tie, total_games)
small_tiger_win_rate = percentage(small_tiger, total_games)
big_tiger_win_rate = percentage(big_tiger, total_games)
tiger_win_rate = percentage(tiger, total_games)

print(f'''
***Win Rates***
Banker: {bank_win_rate}
Player: {player_win_rate}
Tie: {tie_win_rate}
Tiger Tie: {tiger_tie_win_rate}
Small Tiger: {small_tiger_win_rate}
Big Tiger: {big_tiger_win_rate}
Tiger: {tiger_win_rate}
''')

###Expected value calculation

#banker = pure win + tiger win + tie
'''
def expected_player_return(win_rate, player_return, tie_rate):
    return win_rate * player_return

def expected_banker_return():
    return 

def expected_tie_return
'''


