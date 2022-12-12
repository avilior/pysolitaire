from card_model import Deck, Card, CardSuit, CardValue
from dataclasses import dataclass
from rich import print as rprint
import copy


class BuildStack:
    def __init__(self):
        self.hidden_deck: Deck = Deck()
        self.visible_deck: Deck = Deck()

    def hidden_size(self) -> int:
        if self.hidden_deck is None:
            return 0
        return self.hidden_deck.size()

    def getVisible(self) -> Deck:
        """retrieves the visible deck the pile"""
        return self.visible_deck

    def peek(self, pos: int = 0) -> Card | None:
        return self.visible_deck.peek(pos)

    def getOne(self, pos: int = 0) -> Card | None:
        """ get the card from the visible. If the visible is empty, get card from hidden deck"""
        visible_card = self.visible_deck.getOne(pos)

        # if visible is empty then we need to move a card from hidden to visible
        if self.visible_deck.size() == 0:
            self.visible_deck.putOne(card=self.hidden_deck.getOne(pos=0))

        return visible_card

    def getMany(self, start: int) -> list[Card]:

        cards = self.visible_deck.getManySlice(start=start, end=-1)

        # if visible is empty then we need to move a card from hidden to visible
        if self.visible_deck.size() == 0:
            self.visible_deck.putOne(card=self.hidden_deck.getOne(pos=0))

        return cards

    def appendOne(self, card) -> None:
        self.visible_deck.appendOne(card)  # append to the end

    def appendMany(self, cards: list[Card]) -> None:
        self.visible_deck.appendMany(cards)

    @staticmethod
    def canAppendRedBlackRule(*, source: Card | None, destination: Card | None) -> bool:
        # if the source card is none then  bail
        if source is None:
            return False

        # King can go on empty buildStack
        if destination is None and source.value == CardValue.KING:
            return True  # moving a king to an open pile

        # if the destination is None then bail
        if destination is None:
            return False

        # check Suit Color
        if source.isRed() and destination.isRed() or source.isBlack() and destination.isBlack():
            return False

        diff = destination.getIntValue() - source.getIntValue()
        if diff == 1:
            return True

        return False


class SuitStack:
    """cards are added to the end of the deck (pos=-1)"""
    def __init__(self, *, suit: CardSuit):
        self.suit = suit
        self.deck = Deck()

    def peekLast(self):
        """look at the last card """
        return self.deck.peek(pos=-1)

    def validateAppend(self, card) -> bool:
        if card is None:
            return False
        if card.suit != self.suit:
            return False
        if self.deck.size() == 0:
            if card.value == CardValue.ACE:
                return True
            return False

        lastCard = self.deck.peek(pos=-1)
        diff = card.getIntValue() - lastCard.getIntValue()
        if diff == 1:
            return True
        return False

    def appendOne(self, card: Card) -> None:
        if self.validateAppend(card):
            self.deck.appendOne(card)

    def getOne(self) -> None:
        return self.deck.getOne(pos=-1)


@dataclass()
class GameState:

    suitstacks: dict[str, SuitStack]
    buildstacks: list[BuildStack]
    talon: Deck
    deal_deck: Deck


class Game:

    def __init__(self, game_state: GameState = None):

        if game_state is None:
            game_state = GameState(
                deal_deck=Deck.build_standard_52_deck(),
                talon=Deck(),  # empty deck
                suitstacks={
                    "c": SuitStack(suit=CardSuit.CLUBS),
                    "d": SuitStack(suit=CardSuit.DIAMONDS),
                    "h": SuitStack(suit=CardSuit.HEARTS),
                    "s": SuitStack(suit=CardSuit.SPADES)
                },
                buildstacks=[BuildStack() for i in range(7)]
            )

        self.game_state = game_state

    def getBuildStack(self, idx: int) -> BuildStack | None:
        try:
            return self.game_state.buildstacks[idx]
        except Exception:
            return None

    def getSuitStack(self, idx: str) -> SuitStack | None:
        try:
            key = idx.lower()
            return self.game_state.suitstacks[key]
        except KeyError:
            return None

    def getTalon(self):
        return self.game_state.talon

    def start(self) -> None:

        self.game_state.deal_deck.shuffle()

        for s in range(7):
            for i in range(s, 7):
                # print(f"{s} -> {i}")
                # get a card from the deal_deck deck TOP
                # put a card on the TOP
                self.game_state.buildstacks[i].hidden_deck.putOne(self.game_state.deal_deck.getOne())

        for i in range(7):
            self.game_state.buildstacks[i].visible_deck.putOne(self.game_state.buildstacks[i].hidden_deck.getOne())

        self.deal()

    def deal(self):

        if self.game_state.deal_deck.size() > 2:

            for i in range(3):
                self.game_state.talon.putOne(self.game_state.deal_deck.getOne())

        else:
            if self.game_state.talon.size() != 0:
                # Make sure the remain cards are added in the correct way so that
                # we continue to cycle

                # get the cards from the talon deck
                cards = self.game_state.talon.cards
                cards.reverse()  # reverse them
                for i in range(self.game_state.deal_deck.size()):
                    cards.insert(0, self.game_state.deal_deck.getOne())
            else:
                print("******   DEAL DECK has 2 or less cards and TALON has 0 cards ******")

            self.game_state.deal_deck = Deck(cards)
            self.game_state.talon = Deck()

            if self.game_state.deal_deck.size() > 2:

                for i in range(3):
                    self.game_state.talon.putOne(self.game_state.deal_deck.getOne())


    def state(self) -> GameState:
        # TODO make a copy
        return self.game_state

# ####################################################################################################################
#
# ####################################################################################################################


def render_card(c: Card) -> str:
    if c is None:
        return "none"
    cardColor = "black"
    if c.isRed():
        cardColor = "red"

    return f"[{cardColor} bold]{str(c)}[/{cardColor} bold]"


def renderState(gs: GameState):
    COMMA = ','
    suitstacks = gs.suitstacks

    rprint(F"[C]lub: {render_card(suitstacks['c'].peekLast())} [D]iamond: {render_card(suitstacks['d'].peekLast())} [S]pade: {render_card(suitstacks['s'].peekLast())} [H]eart: {render_card(suitstacks['h'].peekLast())}")

    for i in range(7, 0, -1):  # 6 5 4 3 2 1 0
        rprint(F"[{i}] BuildStack <{gs.buildstacks[i-1].hidden_size()}>: {COMMA.join([render_card(c) for c in gs.buildstacks[i-1].visible_deck.cards])}")

    rprint(F"[T]alon: {COMMA.join([render_card(c) for c in gs.talon.cards])}")


@dataclass(kw_only=True)
class Action:
    src: str
    dest: str
    src_cards: list[Card]
    dest_card: Card = None

    def display(self):
        return F"{self.src}-{self.dest}"



def computeOptions(state: GameState) -> list[Action]:

    # #################################
    # WITH BuildStack 1 through 7
    # #################################

    actions = []

    for i in range(7):

        source_buildstack = state.buildstacks[i]

        # if the pile is empty move on
        if source_buildstack.visible_deck.size() == 0:
            continue


        ###########################################################
        # BuildStack TO Suitstacks
        ###########################################################

        source_card = source_buildstack.visible_deck.peek(pos=-1)

        for sp_id in ['c', 'd', 's', 'h']:
            suitstack = state.suitstacks[sp_id]
            if suitstack.validateAppend(source_card):
                actions.append(Action(src=str(i+1), dest=sp_id,src_cards=[source_card]))
                break

        ###########################################################
        # Build Stack to Build Stack
        ###########################################################

        # if the BuildStack is empty and the first card is a King then dont move to another BuildStack
        if source_card.value == CardValue.KING and source_buildstack.hidden_deck.size() == 0:
            continue

        for j in range(7):
            if i == j:
                continue

            destination_card = state.buildstacks[j].destination_buildstack.peek(pos=-1)

            for idx in range(source_buildstack.getVisible().size()):
                source_card = source_buildstack.peek(pos=idx)
                # if source_card can be appended to destination card
                canAppend = BuildStack.canAppendRedBlackRule(source=source_card, destination=destination_card)
                if canAppend:
                    actions.append(Action(src=str(i + 1), dest=str(j+1), src_cards=[source_card]))
                    break

    # ################################################################################################################
    #  Talon to SuiteStack
    # ################################################################################################################

    source_card = state.talon.peek(pos=0)

    for sp_id in ['c', 'd', 's', 'h']:
        suitstack = state.suitstacks[sp_id]
        if suitstack.validateAppend(source_card):
            actions.append(Action(src="T", dest=sp_id, src_cards=[source_card]))
            break

    # ################################################################################################################
    #  Talon to BuildStacks
    # ################################################################################################################

    for i in range(7):

        destination_card = state.buildstacks[i].destination_buildstack.peek(pos=-1)

        canAppend = BuildStack.canAppendRedBlackRule(source=source_card, destination=destination_card)
        if canAppend:
            actions.append(Action(src="T", dest=str(i+1), src_cards=[source_card], dest_card=destination_card))

    # ################################################################################################################
    #  SuiteStacks to BuildStacks
    # ################################################################################################################

    for sp_id in ['c', 'd', 's', 'h']:
        source_card = state.suitstacks[sp_id].peekLast()

        for i in range(7):
            destination_buildstack = state.buildstacks[i]
            destination_card = state.buildstacks[i].destination_buildstack.peek(pos=-1)

            if BuildStack.canAppendRedBlackRule(source=source_card, destination=destination_card):
                actions.append(Action(src=sp_id, dest=str(i + 1), src_cards=[source_card], dest_card=destination_card))

    return actions


def executeInput(game: Game, firstToken: str, secondToken:str = None) -> bool:

    suitStackDesignators = ['c', 'C', 'd', 'D', 'S', 's', 'h', 'H', ]
    buildStackDesignators = ["1", "2", "3", "4", "5", "6", "7", ]

    if firstToken == 'E':  # Exit Command
        return True

    if firstToken in ['X', 'x']:  # Deal Command
        game.deal()
        return False

    # ########################################################################################
    # from talon Deck -- Tallon
    # ########################################################################################
    if firstToken in ['T', 't']:
        # from talon deck
        source = game.getTalon()

        if secondToken in suitStackDesignators:
            # to SuitStack
            destination = game.getSuitStack(secondToken)

            if destination.validateAppend(source.peek()):
                destination.appendOne(source.getOne())

        else:
            # to Piles 1 through 7
            destination = game.getBuildStack(int(secondToken)-1)

            if BuildStack.canAppendRedBlackRule(source=source.peek(), destination=destination.peek(pos=-1)):
                destination.appendOne(source.getOne())
            else:
                print("Illegal move")

    # ###############################################################################
    # moving from BuildStacks TO: .....
    # ###############################################################################
    if firstToken in buildStackDesignators:

        source = game.getBuildStack(int(firstToken)-1)

        if secondToken in suitStackDesignators:
            # to suitPile
            destination = game.getSuitStack(secondToken)

            if destination.validateAppend(source.peek(pos=-1)):
                destination.appendOne(source.getOne(pos=-1))

        elif secondToken in buildStackDesignators:
            destination = game.getBuildStack(int(secondToken)-1)
            destination_card = destination.peek(pos=-1)

            for idx in range(source.getVisible().size()):
                source_card = source.peek(pos=idx)
                # if source_card can be appended to destination card
                canAppend = BuildStack.canAppendRedBlackRule(source=source_card, destination=destination_card)
                if canAppend:
                    # take all the rest of the visibile pile and append it to the destination card
                    cards = source.getMany(start=idx)  # take from index to the end
                    destination.appendMany(cards)

                    break

                # if not then look at the next position

    # ###############################################################################
    # moving from BuildStacks TO: .....
    # ###############################################################################
    if firstToken in suitStackDesignators:

        source = game.getSuitStack(firstToken)

        if secondToken in buildStackDesignators:
            destination = game.getBuildStack(int(secondToken)-1)

            if BuildStack.canAppendRedBlackRule(source=source.peekLast(), destination=destination.peek(-1)):
                destination.appendOne(source.getOne())

    return False

# ####################################################################################################################
#
# ####################################################################################################################

def main():

    game1 = Game()
    game1.start()

    while True:
        state = game1.state()
        renderState(state)
        options = computeOptions(state)
        for o in options:

            print(o.display())

            # play this option
            state_copy = copy.deepcopy(state)
            new_game = Game(game_state=state_copy)
            new_done = executeInput(new_game, firstToken=o.src, secondToken=o.dest)
            next_options = computeOptions(new_game.state())
            for oo in next_options:
                print(f" +--- {oo.display()}")

        user_input = input(F"User input -- {state.deal_deck.size()+state.talon.size()} [E-xit, X deal]:")

        tokens = user_input.split('-')
        firstToken = tokens[0]
        secondToken = tokens[1] if len(tokens) > 1 else None
        done = executeInput(game1, firstToken=firstToken, secondToken=secondToken)
        if done:
            break
    print("Done")


if __name__ == '__main__':
    #test_deal_1()
    #test_deal_2()
    main()

