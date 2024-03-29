from poker_odds_calculator import No_Limit_Holdem_Poker as HP
import time

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

def Rand_game_simulation(num = 100):
    # Simulation Type (2): Show random game
    global Num_Player, board, player_HC
    HP.num_players = Num_Player
    HP.observing_stage = 'r'
    HP.board_ori = board
    HP.player_HC_ori = player_HC
    # Initialize card information
    HP.Initialization()
    Target_hands_type = 1
    Target_rep = num
    game_count = 1
    rep = 1
    c0 = 'Player'
    c1 = 'Hole Cards'
    c2 = 'Community Cards'
    c3 = 'Hands'
    c4 = 'Hands Type'
    c5 = 'Rank'
    Str_col_header = '{0: ^7s} | {1: ^10s} | {2: ^16s} | {3: ^11s} | {4: ^16s} | {5: ^4s} |'
    Str_col_data = '{0: ^7} | {1: ^10s} | {2: ^16s} | {3: ^11s} | {4: ^16s} | {5: ^4s} |'
    Str_sep_line_1 = '{0:-^81}'
    tic = time.time()
    while True:
        HP.Run_New_Game()
        player_hands = HP.Get_Poker_Hands('river')
        HP.Rank_player_hands(player_hands)
        # player_code_HR: player's code with the highest rank
        player_code_HR = [k for k, v in player_hands.items() if v[1] == 0 or v[1] == 1]
        # HR_hands_type: the hands type of the highest rank
        HR_hands_type = player_hands[player_code_HR[0]][0][0]
        # The condition of winner's hands type 
        if HR_hands_type >= Target_hands_type:
            print('{0}-player Game #{1: <8} {4: ^37} {2: >14} #{3: <4}'.format(HP.num_players,
                                                                               game_count,
                                                                               HP.dict_HT[HR_hands_type],
                                                                               rep,
                                                                               ' '))
            print(Str_sep_line_1.format('-'))
            print(Str_col_header.format(c0,c1,c2,c3,c4,c5))
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
                    f = ' '.join([HP.Dict_card(card) for card in HP.board['F']])
                    t = ' '.join([HP.Dict_card(card) for card in HP.board['T']])
                    r = ' '.join([HP.Dict_card(card) for card in HP.board['R']])
                    print(Str_col_data.format(player_code, name_HC, f+' '+t+' '+r, Str_hands, Str_type, Str_rank))
                else:
                    print(Str_col_data.format(player_code, name_HC, ' ', Str_hands, Str_type, Str_rank))
            rep += 1
            print(Str_sep_line_1.format('-'), end='\n'*2)
        #if game_count >= 100:
        if rep >= Target_rep+1:
            toc = time.time()
            print('Running time: {} seconds'.format(round(toc-tic, 3)), end='\n'*3)
            break   
        game_count += 1    
        
# ----------------------- Game Parameters ---------------------------------------------------------------
# Number of players: 1~10
Num_Player = 2
# Board: community cards at flop(F), turn(T), and river(R) stages
board = { 
    'F': [      ],
    'T': [      ],
    'R': [      ]
}
# HC: Hole Cards EX: (4, 13)=♠K, (1, 1)=♣A, (2, 12)=♦Q, (3, 10)=♥T
player_HC = {
    1: [(4, 13),(1, 13)], 
    2: [(2, 1),(3, 1)], 
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
# Number of simulated games
Rand_game_simulation(10)


