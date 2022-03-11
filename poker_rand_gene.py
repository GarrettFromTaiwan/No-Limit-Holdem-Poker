from poker_odds_calculator import No_Limit_Holdem_Poker as HP

# Card elements: 4 suits and 13 values
HP.dict_suit = {4: '♠', 3: '♥', 2: '♦', 1: '♣'}
HP.dict_value = {13: 'A', 12: 'K', 11: 'Q', 10: 'J', 9: 'T', 8: '9',
                  7: '8',  6: '7',  5: '6',  4: '5', 3: '4', 2: '3', 1: '2'}


# ----------------------- Game Parameters ---------------------------------------------------------------
# Number of players: 1~10
HP.num_players = 6
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

Target_hands_type = 1
Target_rep = 100

game_count = 1
rep = 1
tic = time.time()
c0 = 'Player'
c1 = 'Hole Cards'
c2 = 'Community Cards'
c3 = 'Hands'
c4 = 'Hands Type'
c5 = 'Rank'
Str_col_header = '{0: ^7s} | {1: ^10s} | {2: ^16s} | {3: ^11s} | {4: ^16s} | {5: ^4s} |'
Str_col_data = '{0: ^7} | {1: ^10s} | {2: ^16s} | {3: ^11s} | {4: ^16s} | {5: ^4s} |'
Str_sep_line_1 = '{0:-^81}'
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

#-----------------------------------------------------------------------------------------------------------