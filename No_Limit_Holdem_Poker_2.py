import No_Limit_Holdem_Poker as HP
import time

# Card elements
HP.dict_suit = {4: '♠', 3: '♥', 2: '♦', 1: '♣'}
HP.dict_value = {13: 'A', 12: 'K', 11: 'Q', 10: 'J', 9: 'T', 8: '9',
                  7: '8',  6: '7',  5: '6',  4: '5', 3: '4', 2: '3', 1: '2'}
# Game parameters
# HC: player hole cards
# board: public cards at different stages F(flop-3), T(turn-1), R(river-1)
HP.player_number = 1
HP.board_ori = {'F': [], 'T': [], 'R': [] }
HP.player_HC_ori = { 1: [(4, 7), (4, 6)], 2: [], 3: [], 4: [], 5: [],
                  6: [], 7: [], 8: [], 9: [], 10: [] }
# Initialize card information
HP.Initialization()


def Run_new_game():
    HP.Shuffle_cards()
    HP.Fill_cards()

def Get_Poker_hands(stage='River'):
    player_AC = HP.Player_all_cards(stage)
    player_AC2 = HP.Player_all_cards2(player_AC)
    return HP.Player_hands(player_AC2)

count = 1
rep = 1
tic = time.time()
while True:
    Run_new_game()
    player_hands = Get_Poker_hands('River')
    for k, v in player_hands.items():
        if v[0][0] >= 9:
            cards = HP.player_HC[k]+HP.board['F']+HP.board['T']+HP.board['R']
            str_cards = '( '
            for card in cards:
                str_cards += HP.dict_suit[card[0]] + HP.dict_value[card[1]] + ' '
            str_cards += ')'
            print('{0: >8d},{1: >4d}, Cards: {2}, Hands: {3}'.format(count, rep, str_cards, v))
            rep += 1
            break
    
    if rep >= 101:
        toc = time.time()
        print('Running time: {} seconds'.format(round(toc-tic, 3)))
        break
        
    count += 1
    
    