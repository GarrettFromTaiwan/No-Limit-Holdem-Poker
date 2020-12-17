import No_Limit_Holdem_Poker as HP

def Run_new_game():
    HP.Shuffle_cards()
    HP.Fill_cards()

def Get_Poker_hands(stage='River'):
    player_AC = HP.Player_all_cards(stage)
    player_AC2 = HP.Player_all_cards2(player_AC)
    return HP.Player_hands(player_AC2)

class SD():
    # Class for statistical data(SD)
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
            return 0
    @property
    def draw_rate(self):
        if self.__count >= 1:
            draw_rate = self.__draw_count/self.__count
            return draw_rate
        else:
            return 0
    @property
    def wl_ratio(self):
        loss_count = self.__count - self.__win_count - self.__draw_count
        if loss_count >= 1:
            wl_ratio = self.__win_count/loss_count
            return wl_ratio
        else:
            return 0
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
    statistical_data_HC = {v: SD(v, 0, 0, 0) for v in list_HC_name}
    return statistical_data_HC

def Build_SHC_statistical_data():
    # Return the dictionary of specified hole cards(SHC) with each of its statistical data class
    player_HC_ori = HP.Initialize_HC()
    SHC = [HP.Sort_HC(HC) for HC in player_HC_ori.values() if len(HC) == 2]
    list_SHC_name = [HP.Dict_HC(HC) for HC in SHC]
    statistical_data_HC = {v: SD(v, 0, 0, 0) for v in list_SHC_name}
    return statistical_data_HC

def SD_HT():
    # Return the dictionary of all 10 types of hands(HT) with each of its statistical data class
    stadata_HT = {HT_code: SD(HT_name, 0, 0, 0) for HT_code, HT_name in HP.dict_HT.items()}
    return stadata_HT


# Card elements
HP.dict_suit = {4: '♠', 3: '♥', 2: '♦', 1: '♣'}
HP.dict_value = {13: 'A', 12: 'K', 11: 'Q', 10: 'J', 9: 'T', 8: '9',
                  7: '8',  6: '7',  5: '6',  4: '5', 3: '4', 2: '3', 1: '2'}
# Game parameters
# HC: player hole cards
# board: public cards at different stages F(flop-3), T(turn-1), R(river-1)
HP.player_number = 10
HP.board_ori = { 
    'F': [],
    'T': [],
    'R': []
}
HP.player_HC_ori = {
    1: [(4, 1), (3,1)], 2: [(2,2), (1,2)], 3: [],
    4: [],  5: [], 6: [],
    7: [], 8: [], 9: [],
   10: [] 
}
# Initialize card information
HP.Initialization()
# Statistical data class for all 1326 hold cards
#stadata_HC = Build_hold_cards_statistical_data()
# Statistical data class for specified hold cards (refer to HP.player_HC_ori)
stadata_HC = Build_SHC_statistical_data()
# Statistical data class of hands types for each specified hold cards
stadata_HT = {HC_name: SD_HT() for HC_name in stadata_HC.keys()}

#-----------------------------------------------------------------------------------------------------------
import time

game_count = 1

tic = time.time()
while True:
    Run_new_game()
    player_hands = Get_Poker_hands('River')
    HP.Rank_player_hands(player_hands)
    # hands = [ [hands type, 5 card values of hands] ]
    for player_code, hands in player_hands.items():
        code_HT = hands[0][0]
        if code_HT >=1:
            sorted_HC = HP.Sort_HC(HP.player_HC[player_code])
            name_HC = HP.Dict_HC(sorted_HC)
            if name_HC in stadata_HC.keys():
                rank = hands[1]
                if rank == 0:
                    stadata_HC[name_HC].win_count += 1
                    stadata_HT[name_HC][code_HT].win_count += 1
                elif rank == 1:
                    stadata_HC[name_HC].draw_count += 1
                    stadata_HT[name_HC][code_HT].draw_count += 1
                stadata_HC[name_HC].count += 1
                stadata_HT[name_HC][code_HT].count += 1
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
    
    if game_count >= 100000:
        toc = time.time()
        print('Running time: {} seconds'.format(round(toc-tic, 3)), end='\n'*3)
        break
        
    game_count += 1


# Hole Cards | Win Rate | Draw Rate | W/L Ratio |Count
c1 = 'Hole Cards'
c2 = 'Win Rate'
c3 = 'Draw Rate'
c4 = 'W/L Ratio'
c5 = 'Count'
print('{0}-player game simulation times: {1}'.format(HP.player_number, game_count), end='\n'*2)
f = ' '.join([HP.Dict_card(card) for card in HP.board_ori['F']])
t = ' '.join([HP.Dict_card(card) for card in HP.board_ori['T']])
r = ' '.join([HP.Dict_card(card) for card in HP.board_ori['R']])
print('{0: ^16} | {1: ^8} | {2: ^4} | {3: ^5}'.format('Specified Cards:', 'FLOP', 'TURN', 'RIVER'))
print('{0: ^16} | {1: ^8} | {2: ^4} | {3: ^5}'.format(' ', f, t, r), end='\n'*2)
print('Result:', end='\n'*2)
print('{0: ^10s} | {1: ^8s} | {2: ^9s} | {3: ^9s} | {4: ^8s}'.format(c1, c2, c3, c4, c5))
print('{0:-^55}'.format('-'))
for HC_name, data in stadata_HC.items():
    print('{0: ^10s} | {1: ^8.2%} | {2: ^9.2%} | {3: ^9.3} | {4: ^8}'.format(
    data.name, data.win_rate, data.draw_rate, data.wl_ratio, data.count))


#-----------------------------------------------------------------------------------------------------------
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
Str_col = '{0: >10} | {1: ^9} | {2: ^6} | \
{3: ^8} | {4: ^6} | {5: ^8} | {6: ^7} | \
{7: ^10} | {8: ^7} | {9: ^14} | {10: ^11}'
print(Str_col.format(c1, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15))
print('{0:-^126}'.format('-'))

Str_col2 = '{0: >10} | {1: ^9.1%} | {2: ^6.1%} | \
{3: ^8.1%} | {4: ^6.1%} | {5: ^8.1%} | {6: ^7.1%} | \
{7: ^10.1%} | {8: ^7.1%} | {9: ^14.1%} | {10: ^11.1%}'
for HC_name, HT_data in stadata_HT.items():
    # a: Appearance rate of each of Hands types 
    # w: Win rate of...
    # d: Draw rate of...
    a = [stadata_HT[HC_name][HT_code].count/ stadata_HC[HC_name].count 
         if stadata_HC[HC_name].count > 0 else 0 for HT_code in HP.dict_HT.keys()]
    w = [stadata_HT[HC_name][HT_code].win_rate for HT_code in HP.dict_HT.keys()]
    d = [stadata_HT[HC_name][HT_code].draw_rate for HT_code in HP.dict_HT.keys()]
    print(Str_col2.format('| a',a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9]))
    print(Str_col2.format(HC_name+' | w',w[0],w[1],w[2],w[3],w[4],w[5],w[6],w[7],w[8],w[9]))
    print(Str_col2.format('| d',d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9]))
    print('{0:-^126}'.format('-'))
    
    size = 5
    fig, ax = plt.subplots(figsize=(size*1.618, size))
    x = [name for name in HP.dict_HT.keys()]
    y_a = [i*100 for i in a]
    y_w = [i*100 for i in w]
    y_d = [i*100 for i in d]
    ax.plot(x, y_a, 'g-', linewidth=size/4)
    ax.plot(x, y_w, 'r-', linewidth=size/4)
    ax.plot(x, y_d, 'y-', linewidth=size/4)
    plt.xticks(fontsize= size*2.5)
    plt.yticks(fontsize= size*2.5)
    plt.title('Hands Type Distribution', fontsize=size*4)
    plt.xlabel('Hands type code', fontsize=size*3)
    plt.ylabel('(%)', fontsize=size*3)
    plt.legend(['Appearance Rate', 'Win Rate', 'Draw Rate'], 
               fontsize=size*2.5, bbox_to_anchor=(1.02, 0.6), loc='upper left')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.axis([1, 10, 0, 100])
    plt.show()
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------