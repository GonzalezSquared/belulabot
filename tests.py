import luloapi as lapi

def test_take_card_from_deck():
    deck = lapi.DeckOfCards()
    card = deck.retrieve_card_at_random()
    assert card not in deck.current_deck and card in deck.original_deck

def test_create_player_and_bet():
    player1 = lapi.Player()
    money = player1.bet(50)
    assert money == 50

def test_set_as_dealer():
    player1 = lapi.Player()
    player1.dealer_status = True
    assert player1.is_dealer()

def test_not_bet_negatives():
    player1 = lapi.Player()
    try:
        player1.bet(-5)
    except:
        pass

def test_not_bet_more_than_had():
    player1 = lapi.Player()
    try:
        player1.bet(5001)
    except:
        pass
    
def test_multiple_players_recieving_hands():
    player1 = lapi.Player()
    player2 = lapi.Player()
    player3 = lapi.Player()
    deck = lapi.DeckOfCards()
    player1.recieve_hand(deck)
    player2.recieve_hand(deck)
    player3.recieve_hand(deck)
    for card in player1.hand:
        if card in player2.hand or card in player3.hand:
            assert False
    for card in player2.hand:
        if card in player3.hand:
            assert False
    for card in player1.hand + player2.hand + player3.hand:
        if card in deck.current_deck:
            assert False
