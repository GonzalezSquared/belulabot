import random

def cartesian_product_for_lists(list_1, list_2):
    '''
    This function takes two lists and outputs the cartesian product of them.
    For example:
    list1 = [1, 2]
    list2 = ['a', 'b']
    A = cartesian_product_for_lists(list1, list2)

    A is [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
    '''
    cartesian_product = []
    for i in list_1:
        for j in list_2:
            cartesian_product.append((i, j))
    return cartesian_product

class Deck_of_cards:
    '''
    A deck_of_cards object represents a usual spanish deck (four pints: oro, copa, espada and basto)
    and 12 numbers for every card. These are represented by tuples of the form ('x', y) where 'x' is
    either 'o', 'c', 'e' or 'b' and y is an integer from 1 to 12.
    '''
    def __init__(self):
        self.current_deck = [(pinta, numero) for (pinta, numero) in cartesian_product_for_lists(
            ['o', 'c', 'e', 'b'], range(1, 13))]
        self.original_deck = self.current_deck.copy()
        self.amount_of_cards = len(self.current_deck)

    def retrieve_card_at_random(self):
        '''
        This function takes a card from the deck at random, removes it and return it.
        '''
        card = random.choice(self.current_deck)
        self.current_deck.remove(card)
        return card

class Player:
    '''
    This class represents a player of lulo.
    To-do:
        - Implement the memory stuff
    '''
    def __init__(self):
        self.chips = 5000
        self.dealer_status = False
        self.right_to_dealer_status = False
        self.lulo_status = False
        self.folded_status = False # How do we let the players (bots) choose?
        self.memory_of_past_cards = []
        self.hand = []

    def recieve_card(self, deck):
        '''
        This function takes a card from the deck and appends it to the players hand.
        '''
        self.hand.append(deck.retrieve_card_at_random())

    def recieve_hand(self, deck):
        '''
        This function takes 3 cards from the deck and appends it to the players hand.
        '''
        self.recieve_card(deck)
        self.recieve_card(deck)
        self.recieve_card(deck)
    
    def recieve_money(self, amount_of_chips):
        '''
        This function lets the player recieved the money he has won. It does so IN PLACE.
        '''
        self.chips += amount_of_chips

    def bet(self, betting_amount):
        '''
        This function pays the lulo betting amount if the player has enough chips. Else,
        it returns an error.
        '''
        if betting_amount < 0 or betting_amount > self.chips:
            raise ValueError('Incorrect betting amonut! (either negative or too big)')
        self.chips -= betting_amount
        return betting_amount

    def play_card(self, card):
        '''
        This function returns said card and removes it from the hand.
        '''
        if card in self.hand:
            self.hand.remove(card)
            return card
        else:
            raise ValueError('card must be in hand!')

    def is_dealer(self):
        '''
        This function returns a boolean, it returns whether the player is the dealer or not.
        '''
        return self.dealer_status

    def is_right_hand(self):
        '''
        This function returns a boolean, it returns whether the player is the right hand or not.
        '''
        return self.right_to_dealer_status

    def is_lulo(self):
        '''
        This function returns a boolean, it returns whether the player is lulo-ed or not.
        '''
        return self.lulo_status

    def set_chips(self, amount):
        '''
        This function sets the amount of chips for the player.
        '''
        self.chips = amount

    def set_lulo_status(self, new_lulo_status):
        '''
        This function sets the new lulo status (i.e. True if the player lost all local rounds and
        false otherwise).
        '''
        if isinstance(new_lulo_status, bool):
            raise ValueError('The new lulo status should be a boolean!')
        self.lulo_status = new_lulo_status

class Global_round:
    '''
    This is the auxiliar functions for the global round of each game.
    '''
    def __init__(self, _list_of_players, _current_lulo_price):
        self.list_of_players = _list_of_players
        self.current_lulo_price = _current_lulo_price
        self.deck = deck_of_cards()
        self.bets = [0, 0, 0]
        self.showcard = self.deck.retrieve_card_at_random()

    def collect_money_from_lulo_players(self):
        '''
        This function iterates over the list of players and collects money from those who
        were lulo-ed last round.

        To-Do:
            -What if a player has no money?
        '''
        all_collected_money = 0
        for _player in self.list_of_players:
            if _player.is_lulo():
                all_collected_money += _player.bet(self.current_lulo_price)
        if all_collected_money == 0:
            # Nobody ended being lulo-ed, so everyone should place a small amount
            for _player in self.list_of_players:
                all_collected_money += _player.bet(int(0.5 * self.current_lulo_price))

        return all_collected_money

    def collect_and_distribute_money(self):
        '''
        This function gets the money from lulo-ed players and distributes (randomly, for now)
        among the head, body and tail. It does it IN PLACE.
        '''
        collected_money = self.collect_money_from_lulo_players()
        head_amount = random.choice(range(collected_money))
        body_amount = random.choice(range(collected_money - head_amount))
        tail_amount = collected_money - head_amount - body_amount
        self.bets = [head_amount, body_amount, tail_amount]

    '''
    Questions:
        - How to deal with the bets of each player? (even in a bot-ish way).
          For now, let's do it randomly. We'll think of a way later on.
        - How do we deal with changing cards.
    '''

    def deal_hands(self):
        '''
        This function deals the players 3 cards each. It does so IN PLACE.
        '''
        for _player in self.list_of_players:
            _player.recieve_hand(self.deck)

def play_global_round(list_of_players, current_lulo_price):
    global_round = Global_round(list_of_players, current_lulo_price)

    # The round starts, the money is collected from past lulos and the hands
    # are dealt.
    global_round.collect_and_distribute_money()
    global_round.deal_hands()

    # We let players fold, depending on what they got in their hands. Temporarily,
    # we do it randomly.
    list_of_not_folded_players = []
    for player in list_of_players:
        if random.uniform(0, 1) >= 0.5:
            player.folded_status = True
        else:
            list_of_not_folded_players.append(player)
    
    # If there's only one player, he wins it all.
    if len(list_of_not_folded_players) == 1:
        player = list_of_not_folded_players[0]
        player.recieve_money(global_round.bets[0] 
                             + global_round.bets[1]
                             + global_round.bets[2])
    
    # We find the index of the dealer (which can be optimized by putting this on
    # the same loop as the one before).
    index_of_dealer = None
    for player in list_of_players:
        if player.is_dealer():
            index_of_dealer = list_of_players.index(player)
    # We find the closest active player (to the right of the dealer) for it to be the
    # right hand.

    for index in range(index_of_dealer, index_of_dealer + len(list_of_players)):
        index = index % len(list_of_players)
        if list_of_players[index] in list_of_not_folded_players:
            list_of_players[index].right_to_dealer_status = True
            right_to_dealer_player = list_of_players[index]
            break
    
    # Now we know who's starting the game. Now we start with the head.
    list_of_played_cards_head = []
    
    # Temporarily, the hand chooses his first card at random.
    first_card_head = right_to_dealer_player.play_card(
                        random.choice(right_to_dealer_player.hand))
    # Ask Oscar how could I build a \leq relation for cards.


class Local_round:
    def __init__(self, _round_type):
        self.round_type = _round_type
        self.winners = set([])
    

def game():
    '''
    This function is the real deal, it starts a game of Lulo.
    '''


        