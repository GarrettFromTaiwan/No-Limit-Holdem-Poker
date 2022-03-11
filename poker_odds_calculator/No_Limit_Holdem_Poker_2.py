import No_Limit_Holdem_Poker as HP

class SD():
    # Class for statistical data(SD): count, win-count, tie-count, win-rate, tie-rate, W/L ratio
    def __init__(self, ip_name, ip_count, ip_win_count, ip_tie_count):
        self.__name = ip_name
        self.__count = ip_count
        self.__win_count = ip_win_count
        self.__tie_count = ip_tie_count
    @property
    def name(self):
        return self.__name
    @property
    def count(self):
        return self.__count
    @property
    def win_count(self):
        return self.__win_count
    @property
    def tie_count(self):
        return self.__tie_count
    @property
    def win_rate(self):
        if self.__count == 0:
            return 0.0
        else:
            if self.__count == self.__win_count:
                return 1.0
            else:
                win_rate = self.__win_count/self.__count
                return win_rate  
    @property
    def tie_rate(self):
        if self.__count == 0:
            return 0.0
        else:
            if self.__count == self.__tie_count:
                return 1.0
            else:
                tie_rate = self.__tie_count/self.__count
                return tie_rate
    @property
    def wl_ratio(self):
        if self.__count == 0 or self.__count == self.__tie_count:
            return 0.0
        else:
            if self.__count == self.__win_count:
                return 'INF'
            else:
                loss_count = self.__count - self.__win_count - self.__tie_count
                wl_ratio = self.__win_count/loss_count
                return wl_ratio        
    @count.setter
    def count(self, ip_count):
        self.__count = ip_count
    @win_count.setter
    def win_count(self, ip_win_count):
        self.__win_count= ip_win_count
    @tie_count.setter
    def tie_count(self, ip_tie_count):
        self.__tie_count = ip_tie_count
        
def Build_HC_statistical_data():
    # Return the dictionary of all 1326 hole cards(HC) with each of its statistical data class(SD)
    list_HC_name = HP.Print_hole_cards_combinations('return')
    statistical_data_HC = {v: SD(v, 0, 0, 0) for v in list_HC_name}
    return statistical_data_HC

def Build_SHC_statistical_data():
    # Return the dictionary of specified hole cards(SHC) with each of its SD
    player_HC_ori = HP.Initialize_HC()
    SHC = [HP.Sort_HC(HC) for HC in player_HC_ori.values() if len(HC) == 2]
    list_SHC_name = [HP.Dict_HC(HC) for HC in SHC]
    statistical_data_HC = {v: SD(v, 0, 0, 0) for v in list_SHC_name}
    return statistical_data_HC

def SD_HT():
    # SD_HT: Return the dictionary of all 10 types of hands(HT) with each of its SD
    stadata_ht = {HT_code: SD(HT_name, 0, 0, 0) for HT_code, HT_name in HP.dict_HT.items()}
    return stadata_ht

def Build_HT_statistical_data():
    # Return the dictionary of SHC with each of its SD_HT
    global stadata_HC
    stadata_HT_HC = {HC_name: SD_HT() for HC_name in stadata_HC.keys()}
    return stadata_HT_HC

# Card elements: 4 suits and 13 values
HP.dict_suit = {4: '♠', 3: '♥', 2: '♦', 1: '♣'}
HP.dict_value = {13: 'A', 12: 'K', 11: 'Q', 10: 'J', 9: 'T', 8: '9',
                  7: '8',  6: '7',  5: '6',  4: '5', 3: '4', 2: '3', 1: '2'}


# ----------------------- Game Parameters --------------------------------------------------------------------------
# Number of players: 1~10
HP.num_players = 3
# Observing stage: 'preflop(P or p)', 'flop(F or f)', 'turn(T or t)', and 'river(R or r)'
HP.observing_stage = 'p'
# Board: community cards at flop(F), turn(T), and river(R) stages
HP.board_ori = { 
    'F': [   (2, 12),   (3, 12),    (1, 7)   ],
    'T': [   (1, 13)   ],
    'R': [   (4, 7)   ]
}
# HC: Hole Cards
HP.player_HC_ori = {
    1: [(4, 13), (4,13)], 2: [(1, 13),(1, 12)], 3: [(2, 7),(3, 7)],
    4: [      ], 5: [      ], 6: [      ],
    7: [      ], 8: [      ], 9: [      ],
   10: [      ] 
}
# Initialize card information
HP.Initialization()
# ----------------------------------------------------------------------------------------------------------------

# Simulation Type (1): Specified hole cards in different situations ----------------------------------------------

# Statistical data class for specified hold cards (refer to HP.player_HC_ori)
stadata_HC = Build_SHC_statistical_data()
# Statistical data class of hands types for each specified hold cards
stadata_HT = Build_HT_statistical_data()

import time
game_count = 1
tic = time.time()
while True:
    HP.Run_New_Game()
    player_hands = HP.Get_Poker_Hands('river')
    HP.Rank_player_hands(player_hands)
    # hands = [ [hands type, 5 card values of hands], hands rank ] 
    for player_code, hands in player_hands.items():
        sorted_HC = HP.Sort_HC(HP.player_HC[player_code])
        name_HC = HP.Dict_HC(sorted_HC)
        if name_HC in stadata_HC.keys():
            rank = hands[1]
            code_HT = hands[0][0]
            if rank == 0:
                stadata_HC[name_HC].win_count += 1
                stadata_HT[name_HC][code_HT].win_count += 1
            elif rank == 1:
                stadata_HC[name_HC].tie_count += 1
                stadata_HT[name_HC][code_HT].tie_count += 1
            stadata_HC[name_HC].count += 1
            stadata_HT[name_HC][code_HT].count += 1
        else:
            break
    if game_count >= 10000:
        toc = time.time()
        print('Running time: {} seconds'.format(round(toc-tic, 3)), end='\n'*3)
        break   
    game_count += 1

# Print statistical data of specified hole cards
# Hole Cards | Win | Tie | Win/Loss | Count
c1 = 'Hole Cards'
c2 = 'Win'
c3 = 'Tie'
c4 = 'Win/Loss'
c5 = 'Count'
Str_sep_line = '{0:-^44}'
Str_sep_line_1 = '{0:-^60}'
print('{0}-player game simulation times: {1}'.format(HP.num_players, game_count), end='\n'*2)
f = ' '.join([HP.Dict_card(card) for card in HP.board_ori['F']])
t = ' '.join([HP.Dict_card(card) for card in HP.board_ori['T']])
r = ' '.join([HP.Dict_card(card) for card in HP.board_ori['R']])
print(Str_sep_line.format('-'))
print('{0: ^16} | {1: ^8} | {2: ^4} | {3: ^5} |'.format('Community Cards', 'FLOP', 'TURN', 'RIVER'))
print(Str_sep_line.format('-'))
print('{0: ^16} | {1: ^8} | {2: ^4} | {3: ^5} |'.format(' ', f, t, r), end='\n'*2)
print('Result:')
print(Str_sep_line_1.format('-'))
print('{0: ^10s} | {1: ^9s} | {2: ^9s} | {3: ^9s} | {4: ^9s} |'.format(c1, c2, c3, c4, c5))
print(Str_sep_line_1.format('-'))
for HC_name, data in stadata_HC.items():
    print('{0: ^10s} | {1: ^9.2%} | {2: ^9.2%} | {3: ^9.3} | {4: ^9} |'.format(
    data.name, data.win_rate, data.tie_rate, data.wl_ratio, data.count))

# Print statistical data of each hands type for specified hole cards ------------------------------------------------
from matplotlib import pyplot as plt
plt.style.use('dark_background')

c6 = HP.dict_HT[1]
c7 = HP.dict_HT[2]
c8 = HP.dict_HT[3]
c9 = HP.dict_HT[4]
c10 = HP.dict_HT[5]
c11 = HP.dict_HT[6]
c12 = HP.dict_HT[7]
c13 = HP.dict_HT[8]
c14 = HP.dict_HT[9]
c15 = HP.dict_HT[10]
Str_col_header = '{0: >10} | {1: ^9} | {2: ^9} | \
{3: ^9} | {4: ^9} | {5: ^8} | {6: ^7} | \
{7: ^10} | {8: ^7} | {9: ^14} | {10: ^11} |'
Str_col_rate_1 = '{0: >10} | {1: ^9.1%} | {2: ^9.1%} | \
{3: ^9.1%} | {4: ^9.1%} | {5: ^8.1%} | {6: ^7.1%} | \
{7: ^10.1%} | {8: ^7.1%} | {9: ^14.1%} | {10: ^11.1%} |'
Str_col_rate_2 = '{0: >10} | {1: ^9.2%} | {2: ^9.2%} | \
{3: ^9.2%} | {4: ^9.2%} | {5: ^8.2%} | {6: ^7.2%} | \
{7: ^10.2%} | {8: ^7.2%} | {9: ^14.3%} | {10: ^11.4%} |'
Str_sep_line_2 = '{0:-^135}'
for HC_name, HT_data in stadata_HT.items():
    print(Str_sep_line_2.format('-'))
    print(Str_col_header.format(c1, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15))
    # O: Occurrence percentage of each of Hands types
    # T: Tie percentage...
    # W: Win percentage...
    o = [stadata_HT[HC_name][HT_code].count/ stadata_HC[HC_name].count 
         if stadata_HC[HC_name].count > 0 else 0 for HT_code in HP.dict_HT.keys()]
    t = [stadata_HT[HC_name][HT_code].tie_rate for HT_code in HP.dict_HT.keys()]
    w = [stadata_HT[HC_name][HT_code].win_rate for HT_code in HP.dict_HT.keys()]
    print(Str_sep_line_2.format('-'))
    print(Str_col_rate_2.format('| O',o[0],o[1],o[2],o[3],o[4],o[5],o[6],o[7],o[8],o[9]))
    print(Str_col_rate_1.format(HC_name+' | T',t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9]))
    print(Str_col_rate_1.format('| W',w[0],w[1],w[2],w[3],w[4],w[5],w[6],w[7],w[8],w[9]))
    print(Str_sep_line_2.format('-'))
    
    # Data visualization of hands type distribution
    size = 5
    fig, ax = plt.subplots(figsize=(size*1.618, size))
    x = [name for name in HP.dict_HT.keys()]
    y_o = [i*100 for i in o]
    y_t = [i*100 for i in t]
    y_w = [i*100 for i in w]
    ax.plot(x, y_o, 'g-', linewidth=size/3)
    ax.plot(x, y_t, 'y-', linewidth=size/3)
    ax.plot(x, y_w, 'r-', linewidth=size/3)
    plt.xticks(fontsize= size*3)
    plt.yticks(fontsize= size*3)
    plt.title('Hands Type Distribution', fontsize=size*4.5)
    plt.xlabel('Hands Type Code', fontsize=size*3.5)
    plt.ylabel('Percentage(%)', fontsize=size*3.5)
    plt.legend(['Occurrence', 'Tie', 'Win'], 
               fontsize=size*3, bbox_to_anchor=(1.02, 0.6), loc='upper left')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.axis([1, 10, 0, 100])
    plt.show()
#-----------------------------------------------------------------------------------------------------------






# ----------------------- Game Parameters ---------------------------------------------------------------
# Number of players: 1~10
HP.num_players = 9
# Observing stage: 'preflop', 'flop', 'turn', and 'river'
HP.observing_stage = 'r'
# Board: community cards at flop(F), turn(T), and river(R) stages
HP.board_ori = { 
    'F': [      ],
    'T': [      ],
    'R': [      ]
}
# HC: Hole Cards
HP.player_HC_ori = {
    1: [      ], 2: [      ], 3: [      ],
    4: [      ], 5: [      ], 6: [      ],
    7: [      ], 8: [      ], 9: [      ],
   10: [      ] 
}
# Initialize card information
HP.Initialization()
# ----------------------------------------------------------------------------------------------------------------

# Simulation Type (2): Show random game
import time

Target_hands_type = 5
Target_rep = 10

game_count = 1
rep = 1
tic = time.time()
c1 = 'Hole Cards'
c2 = 'Community Cards'
c3 = 'Hands'
c4 = 'Hands Type'
c5 = 'Rank'
Str_col_header = '{0: ^12s} |{1: ^20s} | {2: ^14s} | {3: ^14s} | {4: ^8s} |'
Str_col_data = '{0: ^12s} |{1: ^20s} | {2: ^14s} | {3: ^14s} | {4: ^8s} |'
Str_sep_line_1 = '{0:-^81}'
while True:
    HP.Run_New_Game()
    player_hands = HP.Get_Poker_Hands('river')
    HP.Rank_player_hands(player_hands)
    f = ' '.join([HP.Dict_card(card) for card in HP.board['F']])
    t = ' '.join([HP.Dict_card(card) for card in HP.board['T']])
    r = ' '.join([HP.Dict_card(card) for card in HP.board['R']])
    for player_code, hands in player_hands.items():
        if hands[0][0] >= Target_hands_type:
            print('{0}-player Game #{1: <8} {4: ^37} {2: >14} #{3: <4}'.format(HP.num_players,
                                                                               game_count,
                                                                               HP.dict_HT[hands[0][0]],
                                                                               rep,
                                                                               ' '))
            print(Str_sep_line_1.format('-'))
            print(Str_col_header.format(c1,c2,c3,c4,c5))
            print(Str_sep_line_1.format('-'))
            # hands = [ [hands type, 5 card values of hands], hands rank ]
            for player_code, hands in player_hands.items():
                sorted_HC = HP.Sort_HC(HP.player_HC[player_code])
                name_HC = HP.Dict_HC(sorted_HC)
                Str_hands = ' '.join([ HP.dict_value[v] for v in hands[0][1:] ])
                Str_type = HP.dict_HT[hands[0][0]]
                if hands[1] == 0:
                    Str_rank = 'Win'
                else:
                    Str_rank = str(hands[1])
                # Print community cards and each player's hole cards, hands, hands type, and rank
                # Hole Cards | Community Cards | Hands | Hands Type | Rank
                if Str_rank == 'Win' or Str_rank == '1':
                    print(Str_col_data.format(name_HC, f+' '+t+' '+r, Str_hands, Str_type, Str_rank))
                else:
                    print(Str_col_data.format(name_HC, ' ', Str_hands, Str_type, Str_rank))
            rep += 1
            print(Str_sep_line_1.format('-'), end='\n'*2)
            break
    #if game_count >= 100:
    if rep >= Target_rep+1:
        toc = time.time()
        print('Running time: {} seconds'.format(round(toc-tic, 3)), end='\n'*3)
        break   
    game_count += 1    

#-----------------------------------------------------------------------------------------------------------