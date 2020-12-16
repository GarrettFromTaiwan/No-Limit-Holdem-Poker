import No_Limit_Holdem_Poker as HP
import time

def Run_new_game():
    HP.Shuffle_cards()
    HP.Fill_cards()

def Get_Poker_hands(stage='River'):
    player_AC = HP.Player_all_cards(stage)
    player_AC2 = HP.Player_all_cards2(player_AC)
    return HP.Player_hands(player_AC2)

class SD_HC():
    # Class for statistical data(SD) of hold cards(HC)
    def __init__(self, ip_name, ip_count, ip_win_count, ip_draw_count):
        self.__name = ip_name
        self.__count = ip_count
        self.__win_count = ip_win_count
        self.__draw_count = ip_draw_count
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
    def draw_count(self):
        return self.__draw_count
    @property
    def win_rate(self):
        if self.__count >= 1:
            win_rate = self.__win_count/self.__count
            return win_rate
        else:
            return None
    @property
    def draw_rate(self):
        if self.__count >= 1:
            draw_rate = self.__draw_count/self.__count
            return draw_rate
        else:
            return None
    @name.setter
    def name(self, ip_name):
        self.__name = ip_name
    @count.setter
    def count(self, ip_count):
        self.__count = ip_count
    @win_count.setter
    def win_count(self, ip_win_count):
        self.__win_count= ip_win_count
    @draw_count.setter
    def draw_count(self, ip_draw_count):
        self.__draw_count = ip_draw_count
        
def Build_all_HC_statistical_data():
    # Return the dictionary of all 1326 hole cards(HC) with each of its statistical data class
    list_HC_name = HP.Print_hole_cards_combinations('return')
    statistical_data_HC = {v: SD_HC(v, 0, 0, 0) for v in list_HC_name}
    return statistical_data_HC

def Build_SHC_statistical_data():
    # Return the dictionary of specified hole cards(SHC) with its statistical data class
    SHC = [HP.Sort_HC(HC) for HC in HP.player_HC_ori.values() if len(HC) == 2]
    list_SHC_name = [HP.Dict_HC(HC) for HC in SHC]
    statistical_data_HC = {v: SD_HC(v, 0, 0, 0) for v in list_SHC_name}
    return statistical_data_HC

# Card elements
HP.dict_suit = {4: '♠', 3: '♥', 2: '♦', 1: '♣'}
HP.dict_value = {13: 'A', 12: 'K', 11: 'Q', 10: 'J', 9: 'T', 8: '9',
                  7: '8',  6: '7',  5: '6',  4: '5', 3: '4', 2: '3', 1: '2'}
# Game parameters
# HC: player hole cards
# board: public cards at different stages F(flop-3), T(turn-1), R(river-1)
HP.player_number = 10
HP.board_ori = {'F': [], 'T': [], 'R': [] }
HP.player_HC_ori = { 1: [(4, 2), (3, 2)], 2: [(2, 1),(1, 1)], 3: [], 4: [],  5: [],
                     6: [], 7: [], 8: [], 9: [], 10: [] }
# Initialize card information
HP.Initialization()

# Statistical data for all 1326 hold cards
#stadata_HC = Build_hold_cards_statistical_data()
# Statistical data for specified hold cards (refer to HP.player_HC_ori)
stadata_HC = Build_SHC_statistical_data()




game_count = 1

tic = time.time()
while True:
    Run_new_game()
    player_hands = Get_Poker_hands('River')
    HP.Rank_player_hands(player_hands)
    # hands = [ [hands type, 5 card values of hands] ]
    for player_code, hands in player_hands.items():
        hands_type = hands[0][0]
        if hands_type >=1:
            sorted_HC = HP.Sort_HC(HP.player_HC[player_code])
            name_HC = HP.Dict_HC(sorted_HC)
            if name_HC in stadata_HC.keys():
                rank = hands[1]
                if rank == 0:
                    stadata_HC[name_HC].win_count += 1
                elif rank == 1:
                    stadata_HC[name_HC].draw_count += 1
                stadata_HC[name_HC].count += 1
            else:
                break
            
            #break
            '''cards = HP.Sort_HC(HP.player_HC[player_code])+HP.board['F']+HP.board['T']+HP.board['R']
            str_cards = '( '
            for card in cards:
                str_cards += HP.dict_suit[card[0]] + HP.dict_value[card[1]] + ' '
            str_cards += ')'
            content = '{0: >8d}.{1: >4d}: Cards: {2}  Player: {3}, Hands: {4}'
            print(content.format(game_count, rep, str_cards, player_code, hands))
            rep += 1
            break'''
    
    if game_count >= 10000:
        toc = time.time()
        print('Running time: {} seconds'.format(round(toc-tic, 3)))
        break
        
    game_count += 1


# Hole Cards | Win-rate | Draw-rate | Count
c1 = 'Hole Cards'
c2 = 'Win-rate'
c3 = 'Draw-rate'
c4 = 'Count'
print('{0: ^10s} | {1: ^8s} | {2: ^9s} | {3: ^6s}'.format(c1, c2, c3, c4))
for HC_name, data in stadata_HC.items():
    print('{0: ^10s} | {1: ^8.3f} | {2: ^9.3f} | {3: ^6d}'.format(
    data.name, data.win_rate, data.draw_rate, data.count))

