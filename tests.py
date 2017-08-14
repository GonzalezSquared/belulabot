import luloapi as lapi

def test_take_card_from_deck():
    deck = lapi.deck_of_cards()
    card = deck.retrieve_card_at_random()
    assert card not in deck.current_deck and card in deck.original_deck
