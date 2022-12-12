def test_deal_1():
    cards = [Card(suit=CardSuit.SPADES, value=CardValue.ACE),
             Card(suit=CardSuit.SPADES, value=CardValue.TWO),
             Card(suit=CardSuit.SPADES, value=CardValue.THREE),
             Card(suit=CardSuit.SPADES, value=CardValue.FOUR),
             Card(suit=CardSuit.SPADES, value=CardValue.FIVE),
             Card(suit=CardSuit.SPADES, value=CardValue.SIX),
             Card(suit=CardSuit.SPADES, value=CardValue.SEVEN),
             Card(suit=CardSuit.SPADES, value=CardValue.EIGHT),
             Card(suit=CardSuit.SPADES, value=CardValue.NINE),
             Card(suit=CardSuit.SPADES, value=CardValue.TEN),
             Card(suit=CardSuit.SPADES, value=CardValue.JACK),
             Card(suit=CardSuit.SPADES, value=CardValue.QUEEN),
             Card(suit=CardSuit.SPADES, value=CardValue.KING),
            ]
    game_state = GameState(
        deal_deck=Deck(cards=cards),
        talon=Deck(),  # empty deck
        suitstacks={
            "c": SuitStack(suit=CardSuit.CLUBS),
            "d": SuitStack(suit=CardSuit.DIAMONDS),
            "h": SuitStack(suit=CardSuit.HEARTS),
            "s": SuitStack(suit=CardSuit.SPADES)
        },
        buildstacks=[BuildStack() for i in range(7)]
    )
    game = Game(game_state=game_state)

    game.deal()
    state = game.state()
    renderState(state)
    # 3♠,2♠,A♠

    game.deal()
    state = game.state()
    renderState(state)
    # 6♠,5♠,4♠,3♠,2♠,A♠

    game.deal()
    state = game.state()
    renderState(state)
    # 9♠,8♠,7♠,6♠,5♠,4♠,3♠,2♠,A♠

    game.deal()
    state = game.state()
    renderState(state)
    # Q♠,J♠,10♠,9♠,8♠,7♠,6♠,5♠,4♠,3♠,2♠,A♠

    game.deal()
    state = game.state()
    renderState(state)
    # 2♠,A♠,K♠

    game.deal()
    state = game.state()
    renderState(state)
    # 5♠,4♠,3♠,2♠,A♠,K♠
    game.deal()
    state = game.state()
    renderState(state)
    # 8♠,7♠,6♠,5♠,4♠,3♠,2♠,A♠,K♠
    game.deal()
    state = game.state()
    renderState(state)
    # J♠,10♠,9♠,8♠,7♠,6♠,5♠,4♠,3♠,2♠,A♠,K♠
    game.deal()
    state = game.state()
    renderState(state)
    # A♠,K♠,Q♠

    # play T-s

    executeInput(game, firstToken = 'T', secondToken= 's')
    state = game.state()
    renderState(state)
    # [C]lub: none [D]iamond: none [S]pade: A♠ [H]eart: none
    # K♠,Q♠

    executeInput(game, firstToken='X')
    state = game.state()
    renderState(state)
    #
    # 4♠,3♠,2♠,K♠,Q♠

    executeInput(game, firstToken='X')
    state = game.state()
    renderState(state)
    #
    # 7♠,6♠,5♠,4♠,3♠,2♠,K♠,Q♠

    executeInput(game, firstToken='X')
    state = game.state()
    renderState(state)
    #
    # 10♠,9♠,8♠,7♠,6♠,5♠,4♠,3♠,2♠,K♠,Q♠

    executeInput(game, firstToken='X')
    state = game.state()
    renderState(state)
    #
    # K♠,Q♠,J♠

    print("Done")

def test_deal_2():
    cards = [
             Card(suit=CardSuit.SPADES, value=CardValue.THREE),
             Card(suit=CardSuit.SPADES, value=CardValue.TWO),
             Card(suit=CardSuit.SPADES, value=CardValue.ACE),
             Card(suit=CardSuit.SPADES, value=CardValue.SIX),
             Card(suit=CardSuit.SPADES, value=CardValue.FIVE),
             Card(suit=CardSuit.SPADES, value=CardValue.FOUR),
    ]

    game_state = GameState(
        deal_deck=Deck(cards=cards),
        talon=Deck(),  # empty deck
        suitstacks={
            "c": SuitStack(suit=CardSuit.CLUBS),
            "d": SuitStack(suit=CardSuit.DIAMONDS),
            "h": SuitStack(suit=CardSuit.HEARTS),
            "s": SuitStack(suit=CardSuit.SPADES)
        },
        buildstacks=[BuildStack() for i in range(7)]
    )
    game = Game(game_state=game_state)

    executeInput(game, firstToken='X')
    state = game.state()
    renderState(state)
    #
    # A♠,2♠,3♠

    executeInput(game, firstToken='T', secondToken='s')
    state = game.state()
    renderState(state)
    # [C]lub: none [D]iamond: none [S]pade: A♠ [H]eart: none
    # 2♠,3♠

    executeInput(game, firstToken='T', secondToken='s')
    state = game.state()
    renderState(state)
    # [C]lub: none [D]iamond: none [S]pade: 2♠ [H]eart: none
    # [T]alon: 3♠

    executeInput(game, firstToken='T', secondToken='s')
    state = game.state()
    renderState(state)
    # [C]lub: none [D]iamond: none [S]pade: 3♠ [H]eart: none
    # [T]alon:

    executeInput(game, firstToken='X')
    state = game.state()
    renderState(state)
    # [C]lub: none [D]iamond: none [S]pade: 3♠ [H]eart: none
    # 4♠,5♠,6♠

    executeInput(game, firstToken='T', secondToken='s')
    state = game.state()
    renderState(state)
    # [C]lub: none [D]iamond: none [S]pade: 4♠ [H]eart: none
    # [T]alon: 5♠,6♠

    executeInput(game, firstToken='T', secondToken='s')
    state = game.state()
    renderState(state)
    # [C]lub: none [D]iamond: none [S]pade: 5♠ [H]eart: none
    # [T]alon: 6♠

    executeInput(game, firstToken='T', secondToken='s')
    state = game.state()
    renderState(state)
    # [C]lub: none [D]iamond: none [S]pade: 6♠ [H]eart: none
    # [T]alon:
    print("Done")
