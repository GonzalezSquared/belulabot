import luloapi as lapi

def test_take_card_from_deck():
    deck = lapi.Deck()
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
    deck = lapi.Deck()
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

def test_compare_cards_for_equality():
    card1 = lapi.Card('o', 3)
    card2 = lapi.Card('o', 3)
    assert card1 == card2

def test_compare_cards_for_equality2():
    card1 = lapi.Card('e', 3)
    card2 = lapi.Card('e', 3)
    assert card1 == card2

def test_comparison_of_cards1():
    card1 = lapi.Card('o', 3)
    card2 = lapi.Card('o', 6)
    showcard = lapi.Card('o', 1)
    assert lapi.compare_cards([card1, card2], showcard) == card1

def test_comparison_of_cards2():
    card1 = lapi.Card('o', 3)
    card2 = lapi.Card('o', 6)
    card3 = lapi.Card('b', 10)
    card4 = lapi.Card('e', 12)
    showcard = lapi.Card('o', 1)
    assert lapi.compare_cards([card1, card2, card3, card4],
                              showcard) == card1

def test_comparison_of_cards3():
    card1 = lapi.Card('b', 10)
    card2 = lapi.Card('o', 6)
    card3 = lapi.Card('b', 1)
    card4 = lapi.Card('e', 12)
    showcard = lapi.Card('b', 2)
    assert lapi.compare_cards([card1, card2, card3, card4],
                              showcard) == card3

def test_comparison_of_cards4():
    showcard = lapi.Card('b', 2)

    card1 = lapi.Card('e', 3)
    card2 = lapi.Card('e', 1)
    card3 = lapi.Card('b', 4)
    card4 = lapi.Card('o', 12)
    
    assert lapi.compare_cards([card1, card2, card3, card4],
                              showcard) == card3

def test_comparison_of_cards5():
    showcard = lapi.Card('o', 1)

    card1 = lapi.Card('e', 3)
    card2 = lapi.Card('e', 1)
    card3 = lapi.Card('o', 3)
    card4 = lapi.Card('o', 7)

    # Here, card4 should win, because it is playing as the ('o', 1).

    assert lapi.compare_cards([card1, card2, card3, card4],
                              showcard) == card4

def test_comparison_of_cards6():
    showcard = lapi.Card('c', 3)

    card1 = lapi.Card('c', 2)
    card2 = lapi.Card('c', 12)
    card3 = lapi.Card('c', 7)
    card4 = lapi.Card('c', 6)

    assert lapi.compare_cards([card1, card2, card3, card4],
                              showcard) == card3

def test_comparison_of_cards7():
    showcard = lapi.Card('c', 3)

    card1 = lapi.Card('c', 4)
    card2 = lapi.Card('c', 5)
    card3 = lapi.Card('c', 6)
    card4 = lapi.Card('c', 9)

    assert lapi.compare_cards([card1, card2, card3, card4],
                              showcard) == card4

def test_is_card_playable1():
    showcard = lapi.Card('c', 3)
    rh_card = lapi.Card('o', 5)
    hand = [lapi.Card('o', 1), lapi.Card('b', 7), lapi.Card('c', 1)]
    assert lapi.is_card_playable(lapi.Card('o', 1),
                                 hand, showcard, [rh_card])

def test_is_card_playable2():
    showcard = lapi.Card('c', 3)
    rh_card = lapi.Card('o', 5)
    hand = [lapi.Card('b', 1), lapi.Card('b', 7), lapi.Card('c', 1)]
    assert not lapi.is_card_playable(lapi.Card('b', 7),
                                 hand, showcard, [rh_card])

def test_is_card_playable3():
    showcard = lapi.Card('c', 3)
    rh_card = lapi.Card('o', 5)
    hand = [lapi.Card('o', 4), lapi.Card('b', 7), lapi.Card('o', 1)]
    assert not lapi.is_card_playable(lapi.Card('o', 4),
                                 hand, showcard, [rh_card])

def test_is_card_playable4():
    showcard = lapi.Card('c', 3)
    rh_card = lapi.Card('o', 5)
    hand = [lapi.Card('o', 4), lapi.Card('b', 7), lapi.Card('o', 1)]
    assert lapi.is_card_playable(lapi.Card('o', 1),
                                 hand, showcard, [rh_card])

def test_is_card_playable5():
    showcard = lapi.Card('e', 5)
    rh_card = lapi.Card('o', 10)
    hand = [lapi.Card('o', 4), lapi.Card('e', 8), lapi.Card('o', 5)]
    assert lapi.is_card_playable(lapi.Card('o', 4),
                                 hand, showcard, [rh_card])

def test_is_card_playable6():
    showcard = lapi.Card('e', 5)
    rh_card = lapi.Card('o', 10)
    past_cards = [rh_card, lapi.Card('e', 1)]
    hand = [lapi.Card('o', 4), lapi.Card('e', 8), lapi.Card('o', 3)]
    assert lapi.is_card_playable(lapi.Card('o', 4),
                                 hand, showcard, past_cards)

def test_is_card_playable7():
    showcard = lapi.Card('e', 5)
    rh_card = lapi.Card('o', 10)
    past_cards = [rh_card, lapi.Card('e', 1)]
    hand = [lapi.Card('c', 4), lapi.Card('e', 8), lapi.Card('c', 3)]
    assert lapi.is_card_playable(lapi.Card('e', 8),
                                 hand, showcard, past_cards)

def test_is_card_playable8():
    showcard = lapi.Card('o', 2)
    rh_card = lapi.Card('b', 6)
    past_cards = [rh_card]
    hand = [lapi.Card('e', 5), lapi.Card('o', 1), lapi.Card('b', 4)]
    assert not lapi.is_card_playable(lapi.Card('o', 1),
                                 hand, showcard, past_cards)

def test_move_the_dealer1():
    player1 = lapi.Player()
    player2 = lapi.Player()
    player3 = lapi.Player()

    player1.dealer_status = True
    list_of_players = [player1, player2, player3]
    lapi.move_dealer(list_of_players, None, None, False)
    assert player2.dealer_status

def test_move_the_dealer2():
    player1 = lapi.Player()
    player2 = lapi.Player()
    player3 = lapi.Player()

    player3.dealer_status = True
    list_of_players = [player1, player2, player3]
    lapi.move_dealer(list_of_players, None, None, False)
    assert player1.dealer_status and not player3.dealer_status

def test_lulo_recolection():
    player1 = lapi.Player()
    player2 = lapi.Player()
    player3 = lapi.Player()

    player1.lulo_status = True
    player2.lulo_status = True
    gro = lapi.GlobalRound([player1, player2, player3], 100)
    gro.collect_money_from_lulo_players()
    assert player1.chips == 4900 and player2.chips == 4900
