import random

def cartesian_product_for_lists(list_1, list_2):
    '''
    This function takes two lists and outputs the cartesian product of them.
    For example:
    list1 = [1, 2]
    list2 = ['a', 'b']
    A = cartesian_product_for_lists(list1, list2)

    A is [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]1
    '''
    cartesian_product = []
    for i in list_1:
        for j in list_2:
            cartesian_product.append((i, j))
    return cartesian_product

class deck_of_cards:
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

class player:
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

    def bet(self, betting_amount):
        '''
        This function pays the lulo betting amount if the player has enough chips. Else,
        it returns an error.
        '''
        if betting_amount < 0 or betting_amount > self.chips:
            raise ValueError('Incorrect betting amonut! (either negative or too big)')
        self.chips -= betting_amount
        return betting_amount

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

class global_round:
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
    '''

    def deal_hands(self):
        '''
        This function deals the players 3 cards each. It does so IN PLACE.
        '''
        for _player in self.list_of_players:
            _player.recieve_hand(self.deck)
