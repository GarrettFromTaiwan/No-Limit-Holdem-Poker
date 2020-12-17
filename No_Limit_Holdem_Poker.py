from random import random, sample
from collections import Counter

def Build_deck():
    # Return a new deck of 52 poker cards
    # With card's form like (suit, value) ex: (1,13), (4,9), (2, 11)
    # new_deck: set of 52 poker cards
    new_deck = set((suit, value) for suit in range(4, 0, -1) for value in range(13, 0, -1))
    return new_deck

def Initialization():
    global player_HC, board, poker_cards, shuffled_cards, num_fill_cards      
    def Build_cards():
        # Return a deck of poker cards excluding specified cards
        def Specified_cards():
            global player_HC, board
            # SC: set of specified cards include every player's hole cards and community cards
            SC = set()
            for k, v in player_HC.items():
                if v != False:
                    for i in v:
                        SC.add(i)
            for k, v in board.items():
                if v != False:
                    for i in v:
                        SC.add(i)
            return SC 
        set_52_cards = Build_deck()
        set_specified_cards = Specified_cards()
        # UC: a deck of unspecified cards
        UC = sorted(list(set_52_cards-set_specified_cards), reverse=True)
        return UC
    def Add_rand_num():
        ## Add a random number in front of poker cards for sorting (It's like card-shuffling)
        ## With card's form like [random, (suit, value)] ex: [0.2134534, (1,13)], [0.98979133,(4,9)]
        global poker_cards
        return sorted([[random(), card] for card in poker_cards])
    def Num_of_fill_cards():
        global poker_cards, player_number
        return 2*player_number+5 - (52-len(poker_cards))
    player_HC = Initialize_HC()
    board = Initialize_board()
    poker_cards = Build_cards()
    shuffled_cards = Add_rand_num()
    num_fill_cards = Num_of_fill_cards()

def Initialize_HC():
    # Initialize the dictionary of player hold cards to the original one
    global player_number, player_HC_ori
    HC = { k: [] for k in range(1, player_number+1) }
    for k in range(1, player_number+1):
        if player_HC_ori[k]:
            for v in player_HC_ori[k]:
                HC[k].append(v)
    return HC

def Initialize_board():
    # Initialize the dictionary of board to the original one
    global board_ori
    Bd = {}
    for k, v in board_ori.items():
        Bd[k] = v.copy()
    return Bd    
    
def Shuffle_cards():
    global shuffled_cards
    for i in range(len(shuffled_cards)):
        shuffled_cards[i][0] = random()
    shuffled_cards.sort()

def Fill_cards():
    # Randomly fill(or deal) the unspecified card holes
    global player_HC, board, poker_cards
    ## Initialize each player's hole cards and community cards
    player_HC = Initialize_HC()
    board = Initialize_board()
    ## Filling process
    if num_fill_cards >= 1:
        ## UC: Random cards for unspecified card holes
        UC = sample(poker_cards, k = num_fill_cards)
        fill_count = 0
        for k, v in player_HC.items():
            holes = 2 - len(v)
            for i in range(holes):
                player_HC[k].append(UC[fill_count])
                fill_count += 1
        for k, v in board.items():
            if k == 'F':
                holes = 3 - len(v)
                for i in range(holes):
                    board[k].append(UC[fill_count])
                    fill_count += 1
            else:
                if not v:
                    board[k].append(UC[fill_count])
                    fill_count += 1
    
def Player_all_cards(stage = 'River'):
    # Return each player's all cards (hole cards + community cards)
    global player_HC
    # All Cards(AC) = [(2,10),(1,13),(2,11),(3,11),(3,10),(2,1),(2,13)] ---> [(suit, value)]
    player_AC = {}
    for k, v in player_HC.items():
        player_AC[k] = v.copy()
    try:
        if stage == 'River':
            for i in player_AC:
                player_AC[i] += board['F']+board['T']+board['R']
        elif stage == 'Turn':
            for i in player_AC:
                player_AC[i] += board['F']+board['T']
        elif stage == 'Flop':
            for i in player_AC:
                player_AC[i] += board['F']
    except:
        for i in player_AC:
                player_AC[i] += board['F']+board['T']+board['R']
    return player_AC

def Player_all_cards2(player_AC):
    def Cards_to_list(cards):
    # Return a sorted list of cards
        list_cards = [list(i) for i in zip(*cards)]
        return list_cards
    # Return each player's all cards in the 2nd form (AC2)
    # AC2 = [[2,1,2,3,3,2,2], [10, 13, 11, 11, 10, 1, 13]] ---> [[suits], [values]]
    player_AC2 = {}
    for k in player_AC.keys():
        player_AC2[k] = Cards_to_list(player_AC[k])
    return player_AC2

def Player_hands(player_AC2):
    # Return each player's hands
    player_hands = {k: Poker_hands(v) for k, v in player_AC2.items()}
    return player_hands

def Poker_hands(AC2):
    # Return hands = [ [hands type, 5 card values of hands] ]
    # AC2 = [[2,1,2,3,3,2,2], [10, 13, 11, 11, 10, 1, 13]] ---> [[suits], [values]]
    # Algorithm:
    # <flush test> --->          flush                 /         no flush 
    #              --->     <straight test>            /     <straight test>       
    #              --->   9: straight flush/ 6: flush  /  5: straight/ no straight
    #              --->  10: Royal flush               /             / <no straight test>
    #              --->                                /             / 1: Hightcard/ 2: One pair/ 3: Two pairs/
    #                                                                  4: Trips/ 7: Full house/ 8: Quads
    # 
    ##------------------------------ <Flush Test> ---------------------------------
    p_cards = Flush_test(AC2)
    # For straight test and no straight test
    p_values = p_cards[0]
    p_flush = p_cards[1]
    len_values_set = len(set(p_values))
    ##--------------------------- <No Straight Test> ------------------------------
    if len_values_set < 5:        
        hands = No_straight_hand(p_values)
        return hands
    ##----------------------------- <Straight Test> -------------------------------
    elif len_values_set >= 5:
        Is_straight = Straight_hand(p_values, p_flush, len_values_set)
        # Straight, Straight Fluse, or Royal Flush
        if Is_straight:
            return Is_straight
        # No Straight
        else:
            ##------------------------- <No Straight Test> ----------------------------
            if p_flush == 0:
                hands = No_straight_hand(p_values)
                return hands
            # Flush(6): Not a straight but has more than 5 same suit cards
            elif p_flush == 6:
                values_set = sorted(list(set(p_values)), reverse=True)
                t = []
                hands = [t]
                t.append(6)
                for i in range(5):
                    t.append(values_set[i])
                # hands = [ [hands type, values_set[i] for i in range(5)] ]
                return hands

def Flush_test(AC2):
# AC2 = [[2,1,2,3,3,2,2], [10, 13, 11, 11, 10, 1, 13]] ---> [[suits], [values]]
# p_cards = [ [Flush card's values], 6 ] if thre is a flush in the 5-7 cards
#           [ [Original card's values], 0 ] if no flush is in the 5-7 cards
    p_cards = [ [] ]
    suit_count = Counter(AC2[0]).most_common(1)
    most_suit = suit_count[0][0]
    most_count = suit_count[0][1]
    if most_count >= 5:
        for i, suit in enumerate(AC2[0]):
            if suit == most_suit:
                p_cards[0].append(AC2[1][i])
        p_cards.append(6)
    else:
        p_cards[0] = AC2[1]
        p_cards.append(0)
    return p_cards

def No_straight_hand(p_values):
    # Return the biggest hands if no straight is in the 5-7 cards
    # hands = [ [hands type, the biggest hands] ] in the 5-7 cards
    sorted_v = sorted(p_values, reverse=True)
    value_count = Counter(sorted_v).most_common()
    t = []
    hands = [t]
    ## One pair(2)     
    if value_count[0][1] == 2 and value_count[1][1] == 1:
        t.append(2)
        for i in range(2):
            t.append(value_count[0][0])
        for i in range(1,4):
            t.append(value_count[i][0])
        return hands
    ## Two Pair(3)
    elif value_count[0][1] == 2 and value_count[1][1] == 2:
        t.append(3)
        for i in range(2):
            t.append(value_count[0][0])
        for i in range(2):
            t.append(value_count[1][0])
        if value_count[2][1] == 1:
            t.append(value_count[2][0])
            return hands
        elif value_count[2][1] == 2:
            if value_count[2][0] < value_count[3][0]:
                t.append(value_count[3][0])
                return hands
            elif value_count[2][0] > value_count[3][0]:
                t.append(value_count[2][0])
                return hands
    ## High Card(1)
    elif value_count[0][1] == 1:
        t.append(1)
        for i in range(5):
            t.append(value_count[i][0])
        return hands
    ## Trips(4)   
    elif value_count[0][1] == 3 and value_count[1][1] == 1:
        t.append(4)
        for i in range(3):
            t.append(value_count[0][0])
        for i in range(1,3):
            t.append(value_count[i][0])
        return hands
    ## Full House(7)   
    elif value_count[0][1] == 3 and value_count[1][1] >= 2:
        t.append(7)
        for i in range(3):
            t.append(value_count[0][0])
        for i in range(2):
            t.append(value_count[1][0])
        return hands
    ## Quads(8)   
    elif value_count[0][1] == 4:
        t.append(8)
        for i in range(4):
            t.append(value_count[0][0])
        if len(value_count) > 2:
            if value_count[1][0] < value_count[2][0]:
                t.append(value_count[2][0])
                return hands
            elif value_count[1][0] > value_count[2][0]:
                t.append(value_count[1][0])
                return hands
        elif len(value_count) == 2:
            t.append(value_count[1][0])
            return hands

def Straight_hand(p_values, p_flush, len_values_set):
    # Return the biggest straight if there exists straight hands in the 5-7 cards
    # Otherwise, return False
    # hands = [ [hands type, the biggest straight] ] in the 5-7 cards
    values_set = sorted(list(set(p_values)), reverse=True)
    t = []
    hands = [t]
    ## Straight(5), Straight Flush(9), or Royal Flush(10)
    for i in range(0, len_values_set-4):
        if values_set[i]-4 == values_set[i+4]:
            if p_flush == 0:
                t.append(5) ## Straight(5)
            elif p_flush == 6:
                if values_set[i] == 13:
                    t.append(10) ## Royal Flush(10)
                else:
                    t.append(9) ## Straight Flush(9)
            for j in range(5):
                t.append(values_set[i+j])
            # hands = [ [hands type, 5 straight card values] ]
            return hands
    ## [5,4,3,2,A] Straight(5) or Straight flush(9)
    if values_set[0] == 13 and values_set[-1] == 1 and values_set[-4] == 4:
        if p_flush == 0:
            t.append(5) ## Straight(5)
        elif p_flush == 6:
            t.append(9) ## Straight flush(9)
        for i in range(4, 0, -1):
            t.append(i)
        t.append(13)
        # hands = [ [hands type, 4, 3, 2, 1, 13] ]
        return hands
    ## No straight!
    else:
        return False            
    
def Plot_shuffled_cards():
    # Plot the shuffled deck of poker cards
    from matplotlib import pyplot as plt
    plt.style.use('dark_background')
    for order, card in enumerate(shuffled_cards, 1):
        if card[1][0] == 1:
            plt.plot(order, card[1][1], 'ro')
        elif card[1][0] == 2:
            plt.plot(order, card[1][1], 'yo')
        elif card[1][0] == 3:
            plt.plot(order, card[1][1], 'go')
        elif card[1][0] == 4:
            plt.plot(order, card[1][1], 'bo')

def Print_shuffled_cards():
    # Print the shuffled deck of poker cards
    for order, card in enumerate(shuffled_cards, 1):
        print('{0:>2d}: {1:s}'.format(order, Dict_card(card[1])))
        
def Print_hole_cards_combinations(choice = ' '):
    # Return the all 1326 combinations of hole cards
    import itertools
    deck_cards = sorted(Build_deck(), reverse = True)
    hole_cards = sorted(itertools.combinations(deck_cards, 2), reverse=True)
    Str_HC = [ Dict_HC(HC) for HC in hole_cards ]
    # Return it
    if choice == 'return':
        return Str_HC
    # Write to a text file
    elif choice == 'write':
        with open('hole_cards_combinations', 'wt') as fout:
            for order, HC in enumerate(Str_HC, 1):
                print('{0:4d},{1:s}'.format(order, HC), file=fout, sep='')
    # Print it
    else:
        for order, HC in enumerate(Str_HC, 1):
            print('{0:4d}: {1:s}'.format(order, HC))
            
def Dict_card(card):
    # Return the text form of card. Ex: '♦A','♣A','♠K', and '♥K' are (2,13),(1,13),(4,12), and (3,12)
    try:
        if len(card) == 2:
            if card[0] in dict_suit.keys() and card[1] in dict_value.keys():
                return dict_suit[card[0]]+dict_value[card[1]]
        else:
            print('Should be integer tuple (i, j) with ranges i = 1-4 and j = 1-13.')
    except:
        print('Should be integer tuple (i, j) with ranges i = 1-4 and j = 1-13.')
        
def Dict_HC(hole_cards):
    # Return the text form of hole cards. Ex: '♦A ♣A' means [(2,13),(1,13)]; '♠K ♥K' means [(4,12),(3,12)]
    try:
        if len(hole_cards) == 2:
            return Dict_card(hole_cards[0])+' '+Dict_card(hole_cards[1])
        else: 
            print('Should be two cards with the form like [(i, j),(k, l)].')
    except:
        print('Should be two cards with the form like [(i, j),(k, l)].')
        
def Sort_HC(HC):
    # Sort the hole cards
    if HC[0][0] < HC[1][0]:
        HC[0], HC[1] = HC[1], HC[0]
    elif HC[0][0] == HC[1][0]:
        if HC[0][1] < HC[1][1]:
            HC[0], HC[1] = HC[1], HC[0]
    return HC

def Run_new_game():
    Shuffle_cards()
    Fill_cards()

def Get_Poker_hands(stage='River'):
    player_AC = Player_all_cards(stage)
    player_AC2 = Player_all_cards2(player_AC)
    return Player_hands(player_AC2)

def Rank_player_hands(player_hands):
    # Rank each player's hands by adding order number. 1 means the biggest hands, 2 is the second one,...etc.
    sorted_hands = sorted(player_hands.items(), key = lambda i: i[1], reverse=True)
    # RK: list of ranked player codes
    RK = [i[0] for i in sorted_hands]
    player_hands[RK[0]].append(1)
    prev_hands = player_hands[RK[0]][0]
    prev_rank = player_hands[RK[0]][1]
    for i in range(1, len(RK)):
        curr_hands = player_hands[RK[i]][0]
        if curr_hands == prev_hands:
            player_hands[RK[i]].append(prev_rank)
        else:
            player_hands[RK[i]].append(i+1)
        prev_hands = curr_hands
        prev_rank = player_hands[RK[i]][1]
    # The single winner ranks 0
    # In the case of two or more than two winners, they are all ranked 1
    if len(player_hands) >= 2:
        if player_hands[RK[1]][1] == 2:
            player_hands[RK[0]][1] = 0
    else:
        player_hands[RK[0]][1] = 0
    
# Card elements: 4 suits and 13 values
dict_suit = {4: '♠', 3: '♥', 2: '♦', 1: '♣'}
dict_value = {13: 'A', 12: 'K', 11: 'Q', 10: 'J', 9: 'T', 8: '9',
               7: '8',  6: '7',  5: '6',  4: '5', 3: '4', 2: '3', 1: '2'}
# Hands Types(HT)
dict_HT = {
    1: 'High Card',
    2: 'Pair',
    3: 'Two Pair',
    4: 'Trips',
    5: 'Straight',
    6: 'Flush',
    7: 'Full House',
    8: 'Quads',
    9: 'Straight Flush',
   10: 'Royal Flush'
}
# ----------------------- Game Parameters --------------------------------
# HC: Hole Cards
# board: couumnity cards at flop(F), turn(T), and river(R) stages
player_number = 10
board_ori = {'F': [], 'T': [], 'R': [] }
player_HC_ori = { 1: [], 2: [], 3: [], 4: [], 5: [], 
                  6: [], 7: [], 8: [], 9: [], 10: [] }
# Initialize card information
Initialization()