from colorama import init as colorama_init
from colorama import Fore, Back, Style
import operator
import pandas as pd
import time
import random
import re

colorama_init()

# H in hand, D in hand, C in hand, S in hand, R in hand
player_data = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
tally = [0, 0, 0, 0]

# [card number, suit, score]
# "R" = Joker
cards = [
    [4, "H", 0], [5, "H", 0], [6, "H", 0], [7, "H", 0], [8, "H", 0], [9, "H", 0], [10, "H", 0], ["J", "H", 0], ["Q", "H", 0], ["K", "H", 0], ["A", "H", 0],
    [4, "D", 0], [5, "D", 0], [6, "D", 0], [7, "D", 0], [8, "D", 0], [9, "D", 0], [10, "D", 0], ["J", "D", 0], ["Q", "D", 0], ["K", "D", 0], ["A", "D", 0],
    [5, "C", 0], [6, "C", 0], [7, "C", 0], [8, "C", 0], [9, "C", 0], [10, "C", 0], ["J", "C", 0], ["Q", "C", 0], ["K", "C", 0], ["A", "C", 0],
    [5, "S", 0], [6, "S", 0], [7, "S", 0], [8, "S", 0], [9, "S", 0], [10, "S", 0], ["J", "S", 0], ["Q", "S", 0], ["K", "S", 0], ["A", "S", 0],
    ["R", "", 40]
]

suits = ["H", "H", "D", "C", "S"]
trump_suit = ""
player_names = [f"{Fore.YELLOW}{Style.BRIGHT}Joe{Style.RESET_ALL}", f"{Fore.GREEN}{Style.BRIGHT}James{Style.RESET_ALL}", f"{Fore.MAGENTA}{Style.BRIGHT}Chuck{Style.RESET_ALL}", f"{Fore.CYAN}{Style.BRIGHT}Ellen{Style.RESET_ALL}"]

def card_color(suit):
    if suit == "H":
        output = f"{Fore.RED}Hearts{Style.RESET_ALL}"
    if suit == "D":
        output = f"{Fore.RED}Diamonds{Style.RESET_ALL}"
    if suit == "C":
        output = f"{Fore.BLACK}Clubs{Style.RESET_ALL}"
    if suit == "S":
        output = f"{Fore.BLACK}Spades{Style.RESET_ALL}"
    return output

def card_name(card, is_list):
    card_suit = ""
    card_type = ""
    card_color = ""
    if card[0] == "J":
        card_type += "Jack of "
    elif card[0] == "Q":
        card_type += "Queen of "
    elif card[0] == "K":
        card_type += "King of "
    elif card[0] == "A":
        card_type += "Ace of "
    else:
        card_type += str(card[0]) + " of "

    if card[1] == "H":
        card_color = f"{Fore.RED}"
        card_suit = "Hearts"
    if card[1] == "D":
        card_color = f"{Fore.RED}"
        card_suit = "Diamonds"
    if card[1] == "C":
        card_color = f"{Fore.BLACK}"
        card_suit = "Clubs"
    if card[1] == "S":
        card_color = f"{Fore.BLACK}"
        card_suit = "Spades"
    
    output = card_color + card_type + card_suit + f"{Style.RESET_ALL}"

    if card[0] == "R":
        output = f"{Fore.BLUE}Joker{Style.RESET_ALL}"

    if is_list:
        return f"{output}, "
    else:
        return f"{output}"

def suit_id(suit):
    if suit == "H":
        return 0
    elif suit == "D":
        return 1
    elif suit == "C":
        return 2
    elif suit == "S":
        return 3
    else:
        return 4
    
def hand_name(hand):
    output = ""
    for x in hand:
        output += card_name(x, True)
    output = re.sub(r', ?$', "", output)
    return output

def assign_scores(trump, hand):
    for x in hand:
        if type(x[0]) == str:
            if x[0] == "J":
                if trump == x[1]:
                    x[0] = "Right Bower"
                    x[2] = 16
                elif (trump == "H" and x[1] == "D") or (trump == "D" and x[1] == "H") or (trump == "C" and x[1] == "S") or (trump == "S" and x[1] == "C"):
                    x[0] = "Left Bower"
                    x[1] = trump
                    x[2] = 15
                else:
                    x[2] = 11
            elif x[0] == "Q":
                x[2] = 12
            elif x[0] == "K":
                x[2] = 13
            elif x[0] == "A":
                x[2] = 14
            elif x[0] == "R":
                x[1] = trump
                x[2] = 40
        else:
            x[2] = x[0]
        if x[1] == trump:
            x[2] += 20
    return cards

def sort_hand(hand):
    array = sorted(hand, key = operator.itemgetter(1, 2))
    return array

def cards_left(player, card):
    if card[1] == "H":
        player_data[player][0] += 1
    if card[1] == "D":
        player_data[player][1] += 1
    if card[1] == "C":
        player_data[player][2] += 1
    if card[1] == "S":
        player_data[player][3] += 1
    if card[0] == "R": # special case
        player_data[player][4] += 1

hands = [[],[],[],[]]
kitty = []

def setup():
    global hands, kitty
    for c, x in enumerate(hands):
        for a in range(10):
            card_limit = len(cards) - 1
            random_card = cards[random.randint(0,card_limit)]
            x.append(random_card)
            cards_left(c, random_card)
            cards.remove(random_card)
    kitty = cards
    #for x in range(0,4):
        #print(player_names[x] + "'s hand: ", hand_name(sort_hand(hands[x])))
    print(player_names[0] + "'s hand: ", hand_name(sort_hand(hands[0])))
    #print("Kitty: ", hand_name(sort_hand(kitty)))

def betting_phase():
    global trump_suit
    while True:
        bet = input("Would you like to bet? (Type a number and a suit (e.g. '6S' or '7H'), or the word 'no'.) — ")
        bet_split = list(bet)
        if bet == "no":
            print("OK! You pass.")
            trump_suit = suits[random.randint(0,len(suits)-1)]
            break
        try:
            bet_split[0] = int(bet_split[0])
        except:
            print("The first character must be a number.")
            continue
        if bet_split[0] < 6:
            print("You need to bet more than 6. — ")
            continue
        elif bet_split[1].lower() not in ("h","d","c","s"):
            print("Please use one of H, D, C, or S.")
            continue
        else:
            trump_suit = bet_split[1].upper()
            break
    print("For the sake of testing... ")
    print("\nThe trump suit is " + card_color(trump_suit))
    for x in hands:
        x = assign_scores(trump_suit, x) #FIXME: This needs to come AFTER the trump is decided


current_suit = ""
score_to_beat = ""
played_cards = []
hands_played = 0 # for played cards

def score_to_beat_text(score, status):
    if score > 20 and score != 60:
        score_text = str(score - 20) + " + Trump"
    elif score == 60:
        score_text = "Joker"
    else:
        score_text = str(score)
    if status == "now":
        out = f'{Fore.GREEN}The score to beat is {status} {score_text}{Style.RESET_ALL}'
    elif status == "":
        out = f'The score to beat is {score_text}'
    else:
        out = f'The score to beat is {status} {score_text}'
    print(out)

def turn(player):
    print("It is " + player_names[player] + "'s turn!")
    global current_suit
    global score_to_beat
    global hands_played

    if hands_played == 0: # this player is first and can play whatever
        random_card = random.randint(0,len(hands[player])-1)
        card_to_play = hands[player][random_card]
        print(player_names[player] + " plays " + card_name(card_to_play, False))
        current_suit = card_to_play[1]
        score_to_beat = card_to_play[2]
        score_to_beat_text(score_to_beat,"now")

    else: # this player must match suit
        score_to_beat_text(score_to_beat,"")
        must_play = player_names[player] + " must play " + card_color(current_suit)
        random_card = random.randint(0,len(hands[player])-1)
        card_to_play = hands[player][random_card]
        if player_data[player][suit_id(current_suit)] == 0:
            must_play += ", but has no cards of that suit"
            random_card = random.randint(0,len(hands[player])-1)
            card_to_play = hands[player][random_card]
        else:
            while card_to_play[1] != current_suit:
                random_card = random.randint(0,len(hands[player])-1)
                card_to_play = hands[player][random_card]
        print(must_play)
        print(player_names[player] + " plays " + card_name(card_to_play, False))
        if card_to_play[2] > score_to_beat and (card_to_play[1] == current_suit or card_to_play[1] == trump_suit):
            score_to_beat = card_to_play[2]
            score_to_beat_text(score_to_beat,"now")
        else:
            card_to_play[2] = 0 # set the score for this card to 0, since it's not valid
            score_to_beat_text(score_to_beat,"still")
    played_cards.append(card_to_play)
    hands[player].remove(card_to_play)
    player_data[player][suit_id(played_cards[hands_played][1])] -= 1
    hands_played += 1
    print("————")

leader = 0
order = [] # this is to ascertain player order, as well as to ensure the tally is calculated properly.

def find_winner(played):
    scores = []
    scores.append(played[0][2])
    scores.append(played[1][2])
    scores.append(played[2][2])
    scores.append(played[3][2])
    best_score = max(scores)
    best_score_index = pd.Series(scores).idxmax()
    # print(player_names[order[best_score_index]] + " wins with a score of " + str(best_score))
    print(player_names[order[best_score_index]] + " wins!")
    global score_to_beat
    global current_suit
    global played_cards
    global tally
    global leader
    tally[order[best_score_index]] += 1
    print(tally)
    score_to_beat = 0
    current_suit = ""
    played_cards = []
    leader = best_score_index

turns = 0

def full_turn(leader):
    global turns
    global hands_played
    hands_played = 0
    turns += 1
    print(f'\n\n{Back.WHITE}Turn {str(turns)}{Style.RESET_ALL}')
    global order
    order = [leader % 4, (leader + 1) % 4, (leader + 2) % 4, (leader + 3) % 4]
    turn(leader % 4)
    turn((leader + 1) % 4)
    turn((leader + 2) % 4)
    turn((leader + 3) % 4)
    find_winner(played_cards)

def winning_team(scores):
    team1 = scores[0] + scores[2]
    team2 = scores[1] + scores[3]
    if team1 > team2:
        print(player_names[0] + " and " + player_names[2] + " win!! ", team1, "–", team2)
    elif team1 < team2:
        print(player_names[1] + " and " + player_names[3] + " win!! ", team2, "–", team1)
    else:
        print("It's a tie ", team1, "–", team2)

setup()
betting_phase()
time.sleep(2)
for x in range(10):
    print(trump_suit)
    full_turn(leader)
    time.sleep(2)
winning_team(tally)