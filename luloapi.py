import random

'''
luloapi.py, a python implementation of the classic colombian game Lulo.

To-Do:
    - Implement "el muerto"
'''


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

class Card:
    '''
    Every card is represented by tuples of the form ('x', y) where 'x' is
    either 'o', 'c', 'e' or 'b' and y is an integer from 1 to 12, and it has
    only two attributes: kind (which is the first string of the tuple) and
    number, which is the second.
    '''
    def __init__(self, _kind, _number):
        self.kind = _kind
        self.number = _number

    def __eq__(self, other):
        # print('other\'s type: ' + str(type(other)))
        if not isinstance(other, self.__class__):
            return False

        return self.kind == other.kind and self.number == other.number

    def __repr__(self):
        return '({}, {})'.format(self.kind, self.number)

class DeckOfCards:
    '''
    A DeckOfCards object represents a usual spanish deck (four pints: oro, copa, espada and basto)
    and 12 numbers for every card. 
    '''
    def __init__(self):
        self.current_deck = [Card(kind, numero) for (kind, numero) in cartesian_product_for_lists(
            ['o', 'c', 'e', 'b'], range(1, 13))]
        self.original_deck = self.current_deck.copy()
        self.amount_of_cards = len(self.current_deck)

    def retrieve_card_at_random(self):
        '''
        This function takes a card from the deck at random, removes it and
        returns it.
        '''
        card = random.choice(self.current_deck)
        self.current_deck.remove(card)
        return card

class Player:
    '''
    This class represents a player of lulo.

    It can be initialized with a type (either None (i.e. random), human or bot).
    The type is a tuple (x,y) where x is a string which states 'random', 'human'
    or 'bot' and the second is the bot object if it x == 'bot'. Maybe we could
    pair the second one with the human object.
    To-do:
        - Implement the memory stuff
    '''
    def __init__(self, _type=(None, None), _chips=5000):
        self.chips = _chips
        self.dealer_status = False
        self.folded_status = False # How do we let the players (bots) choose?
        self.hand = []
        self.lulo_status = False
        self.memory_of_past_cards = []
        self.name = None
        self.right_to_dealer_status = False
        self.type = _type

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

    def play_card(self, global_round_object):
        '''
        This function is for the bot (or human) to decide.
        '''
        if self.type[0] == 'random' or self.type[0] == None:
            for card in self.hand:
                if is_card_playable(card):
                    self.hand.remove(card)
                    return card

        if self.type[0] == 'human':
            '''
            Here we need to implement the interface for asking a human to play a card
            and an information object, that stores everything.
            '''
            return ask_human_for_card(information_object)

        if self.type[0] == 'bot':
            bot = self.type[1]
            # How do we deal with the information flow towards the bot.
            return bot.play_card(infomation_object)
        

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

class GlobalRound:
    '''
    This is the auxiliar functions for the global round of each game.
    '''
    def __init__(self, _list_of_players, _current_lulo_price):
        self.list_of_players = _list_of_players
        self.current_lulo_price = _current_lulo_price
        self.deck = DeckOfCards()
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

def compare_cards_of_same_kind(card1, card2, showcard):
    '''
    This function compares two cards of the same kind. It considers the 
    whole 7-as-showcard deal. 
    '''

    if card1.kind != card2.kind:
        raise ValueError('Cards must be of the same kind')

    if card1 == card2:
        # print('cards are equal, so return True')
        return card1

    # The number 7 card of the showcard kind plays as the showcard
    if card1.kind == showcard.kind:
        if card1.number == 7 and (card1.number < showcard.number or showcard.number in [1,3]):
            if compare_cards_of_same_kind(showcard, card2, showcard) == showcard:
                return card1
    if card2.kind == showcard.kind:
        if card2.number == 7 and (card2.number < showcard.number or showcard.number in [1,3]):
            if compare_cards_of_same_kind(card1, showcard, showcard) == showcard:
                return card2

    if card1.number == 1:
        return card1
    if card2.number == 1:
        return card2

    if card1.number == 3:
        return card1
    if card2.number == 3:
        return card2
    # What rests is just making a normal comparison, once 1, 3 and 7 have been
    # discarded

    if card1.number > card2.number:
        return card1
    if card2.number > card1.number:
        return card2

def compare_cards(list_of_cards, showcard, rh_card):
    '''
    This function compares the list of cards depending on what the showcard and
    the right-to-dealer card is. It returns the one that should win the round.
    '''
    if rh_card not in list_of_cards:
        raise ValueError('The asked card must be in the list somewhere')
    current_winning_card = rh_card
    for card in list_of_cards:
        # print('card\'s type: ' + str(type(card)))
        # print('showcard\'s type: ' + str(type(showcard)))
        # print('rh_card\'s type: ' + str(type(rh_card)))
        if card.kind == current_winning_card.kind:
            # print('Comparing {} with {}'.format(card, current_winning_card))
            current_winning_card = compare_cards_of_same_kind(card, current_winning_card, showcard)
            # print(current_winning_card)
            # print('winning card\'s type: ' + str(type(current_winning_card)))
            # print('Winner is: {}'.format(current_winning_card))
        if card.kind == showcard.kind and current_winning_card.kind != showcard.kind:
            # print('Comparing {} with {}'.format(card, current_winning_card))
            current_winning_card = card
            # print('Winner is: {}'.format(current_winning_card))
    return current_winning_card

#To-Do: implement ask_human_for_card function.

def is_card_playable(card, hand, showcard, rh_card, past_cards):
    '''
    This function detemines if a player can play a certain card, i.e. he's not
    "surrendering" by leaving a card of the same kind of the showcard or the
    rh_card.

    To-Do:
        - Reimpelement this with the public info class.
    '''
    if card not in hand:
        raise ValueError('Card must be in the player\'s hand')

    list_of_rh_kind_cards = [c for c in hand if c.kind == rh_card.kind]
    list_of_showcard_kind_cards = [c for c in hand if c.kind == showcard.kind]
    playable_cards = []

    if list_of_rh_kind_cards != []:
        for _card in list_of_rh_kind_cards:
            # Play to win: if the card wins, it is playable.
            if compare_cards(past_cards + [_card], showcard, rh_card) != compare_cards(past_cards, showcard, rh_card):
                print('card ' + str(_card) + ' affects!')
                playable_cards.append(_card)
        if playable_cards == []:
            # If no rh-like-card wins, then they all can be played.
            print('No card affected!')
            playable_cards += list_of_rh_kind_cards
            print('Playable cards: ' + str(playable_cards))

        if card in playable_cards:
            return True
        else:
            return False

    if list_of_rh_kind_cards == [] and list_of_showcard_kind_cards != []:
        for _card in list_of_showcard_kind_cards:
            if compare_cards(past_cards + [_card], showcard, rh_card) != compare_cards(past_cards, showcard, rh_card):
                playable_cards.append(_card)
            if playable_cards == []:
                playable_cards += list_of_showcard_kind_cards

        if card in playable_cards:
            return True
        else:
            return False

    if list_of_rh_kind_cards == [] and list_of_showcard_kind_cards == []:
        return True







def play_global_round(list_of_players, current_lulo_price):
    global_round = GlobalRound(list_of_players, current_lulo_price)

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

    if index_of_dealer == None:
        raise ValueError('No player was the dealer, WAT?!')
    # We find the closest active player (to the right of the dealer) for it to be the
    # right hand.

    for index in range(index_of_dealer, index_of_dealer + len(list_of_players)):
        index = index % len(list_of_players)
        if list_of_players[index] in list_of_not_folded_players:
            list_of_players[index].right_to_dealer_status = True
            right_to_dealer_player = list_of_players[index]
            index_of_rh_player = index
            break
    
    # Now we know who's starting the game. Now we start with the head.
    list_of_played_cards_head = [None for active_player in list_of_not_folded_players]

    for index in range(index_of_rh_player + len(list_of_not_folded_players)):
        index = index % len(list_of_not_folded_players)
        player = list_of_not_folded_players[index]
        list_of_played_cards_head[index] = player.play_card()
    # To-Do: how the hell do we let the player pick a card depending on
    # the current state of the game?


def game():
    '''
    This function is the real deal, it starts a game of Lulo.
    '''
    pass


        