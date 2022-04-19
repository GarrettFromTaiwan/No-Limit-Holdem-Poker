from poker_odds_calculator import No_Limit_Holdem_Poker as HP
import time

class SD():
    # Class for statistical data(SD): count, win-count, tie-count, win-rate, tie-rate, Loss/Win ratio
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
    def lw_ratio(self):
        if self.__win_count == 0:
            return 'INF'
        else:
            loss_count = self.__count - self.__win_count - self.__tie_count
            if loss_count == 0:
                return 0.0
            else:
                return loss_count/self.__win_count
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

def Shift_card_value(card_dict):
    # Value Shift: 1->13, 13->12, 12->11, ..., 3->2, 2->1 for data processing
    for k, v in card_dict.items():
        for i in range(len(v)):
            if v[i]:
                tem = list(card_dict[k][i])
                tem[1] -= 1
                if tem[1] == 0:
                    tem[1] = 13
                card_dict[k][i] = tuple(tem)
    return card_dict

def Game_simulation(stage = 'r'):
    # Simulation Type (1): Specified hole cards in different situations ----------------------------------------------
    global Num_Player, board, player_HC, stadata_HC
    HP.num_players = Num_Player
    HP.observing_stage = stage
    HP.board_ori = board
    HP.player_HC_ori = player_HC
    # Initialize card information
    HP.Initialization()
    # Statistical data class for specified hold cards (refer to HP.player_HC_ori)
    stadata_HC = Build_SHC_statistical_data()
    # Statistical data class of hands types for each specified hold cards
    stadata_HT = Build_HT_statistical_data()

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
    # Hole Cards | Win | Tie | Loss/Win | Count
    c1 = 'Hole Cards'
    c2 = 'Win'
    c3 = 'Tie'
    c4 = 'Loss/Win'
    c5 = 'Count'
    Str_sep_line = '{0:-^44}'
    Str_sep_line_1 = '{0:-^60}'
    print('{0}-player game simulation times: {1}'.format(HP.num_players, game_count), end='\n'*2)
    if HP.observing_stage.lower() in {'p', 'preflop'}:
        f = ' '.join([HP.Dict_card(card) for card in [ ] ])
        t = ' '.join([HP.Dict_card(card) for card in [ ] ])
        r = ' '.join([HP.Dict_card(card) for card in [ ] ])
    elif HP.observing_stage.lower() in {'f', 'flop'}:
        f = ' '.join([HP.Dict_card(card) for card in HP.board_ori['F']])
        t = ' '.join([HP.Dict_card(card) for card in [ ] ])
        r = ' '.join([HP.Dict_card(card) for card in [ ] ])
    elif HP.observing_stage.lower() in {'t', 'turn'}:
        f = ' '.join([HP.Dict_card(card) for card in HP.board_ori['F']])
        t = ' '.join([HP.Dict_card(card) for card in HP.board_ori['T']])
        r = ' '.join([HP.Dict_card(card) for card in [ ] ])
    elif HP.observing_stage.lower() in {'r', 'river'}:
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
        data.name, data.win_rate, data.tie_rate, data.lw_ratio, data.count))

    # Print statistical data of each hands type for specified hole cards ------------------------------------------------
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
    Str_col_header = '{0: >10} | {1: ^9} | {2: ^9} | {3: ^9} | {4: ^9} | {5: ^8} | {6: ^7} | {7: ^10} | {8: ^7} | {9: ^14} | {10: ^11} |'
    Str_col_rate_1 = '{0: >10} | {1: ^9.1%} | {2: ^9.1%} | {3: ^9.1%} | {4: ^9.1%} | {5: ^8.1%} | {6: ^7.1%} | {7: ^10.1%} | {8: ^7.1%} | {9: ^14.1%} | {10: ^11.1%} |'
    Str_col_rate_2 = '{0: >10} | {1: ^9.2%} | {2: ^9.2%} | {3: ^9.2%} | {4: ^9.2%} | {5: ^8.2%} | {6: ^7.2%} | {7: ^10.2%} | {8: ^7.2%} | {9: ^14.3%} | {10: ^11.4%} |'
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
        print(Str_sep_line_2.format('-'), end='\n'*4)
        '''
        # Data visualization of hands type distribution
        from matplotlib import pyplot as plt
        plt.style.use('dark_background')
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
        '''
# ----------------------- Game Parameters --------------------------------------------------------------------------
# Number of players: 1~10
Num_Player = 2
# Board: community cards at flop(F), turn(T), and river(R) stages
board = { 
    'F': [   (2, 2), (2, 4), (1, 11)   ],
    'T': [   (3, 13)   ],
    'R': [   (4, 2)   ]
}
# HC: Hole Cards EX: (4, 13)=♠K, (1, 1)=♣A, (2, 12)=♦Q, (3, 10)=♥T
player_HC = {
    1: [(4, 13),(1, 13)], 
    2: [      ], 
    3: [      ],
    4: [      ], 
    5: [      ], 
    6: [      ],
    7: [      ], 
    8: [      ], 
    9: [      ],
   10: [      ] 
}
# Value Shift: 1->13, 13->12, 12->11, ..., 3->2, 2->1 for data processing
board = Shift_card_value(board)
player_HC = Shift_card_value(player_HC)
# Observing stage: 'preflop(P or p)', 'flop(F or f)', 'turn(T or t)', and 'river(R or r)'
Game_simulation('p')
Game_simulation('f')
Game_simulation('t')
Game_simulation('r')


