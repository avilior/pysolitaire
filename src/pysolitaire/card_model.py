from dataclasses import dataclass, field
from enum import Enum, unique
import random
# https://github.com/suryadutta/solitaire/blob/master/solitaire.py


@unique
class CardValue(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __str__(self) -> str:
        if 1 < self.value < 11:
            return str(self.value)
        return self.name[0]


@unique
class CardSuit(Enum):
    SPADES = 1
    CLUBS = 2
    DIAMONDS = 3
    HEARTS = 4

    def isRed(self) -> bool:
        return self in [CardSuit.DIAMONDS, CardSuit.HEARTS]

    def isBlack(self) -> bool:
        return not self.isRed()

    def __str__(self) -> str:
        if self.name == "SPADES":
            return u'\u2660'
        if self.name == "CLUBS":
            return u'\u2663'
        if self.name == "DIAMONDS":
            return u'\u2666'
        if self.name == "HEARTS":
            return u'\u2665'


@dataclass()
class Card:
    value: CardValue
    suit: CardSuit

    def isRed(self) -> bool:
        return self.suit.isRed()

    def isBlack(self) -> bool:
        return self.suit.isBlack()

    def getIntValue(self) -> int:
        return self.value.value

    def __str__(self):
        return f"{self.value}{self.suit}"


@dataclass()
class Deck:
    cards: list[Card] = field(default_factory=list)

    @classmethod
    def build_standard_52_deck(cls):
        card_values = [CardValue.ACE, CardValue.TWO, CardValue.THREE, CardValue.FOUR,
                       CardValue.FIVE, CardValue.SIX, CardValue.SEVEN,
                       CardValue.EIGHT, CardValue.NINE, CardValue.TEN,
                       CardValue.JACK, CardValue.QUEEN, CardValue.KING, ]
        card_suits = [CardSuit.CLUBS, CardSuit.DIAMONDS, CardSuit.SPADES, CardSuit.HEARTS]

        return Deck(cards=[Card(suit=s, value=v) for s in card_suits for v in card_values])

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def size(self) -> int:
        return len(self.cards)

    def peek(self, pos: int = 0) -> Card | None:
        """ take a look at the card at pos.  POS 0 is the first card, POS -1 is the last card"""
        if pos < 0:
            pos = len(self.cards) + pos
        try:
            return self.cards[pos]
        except IndexError:
            return None

    def getOne(self, pos: int = 0) -> Card | None:
        """ Remove card from pos.  POS 0 is top POS -1 is last card"""
        if pos < 0:
            pos = len(self.cards) + pos

        try:
            return self.cards.pop(pos)
        except IndexError:
            return None

    def getManyCount(self, count: int = 1, pos: int = 0) -> list[Card]:
        """ Remove card from pos 0 is top"""
        result: list[Card] = []

        if count < 0:
            return result

        for i in range(count):
            card = self.getOne(pos=pos)
            if card is not None:
                result.append(card)
        return result

    def getManySlice(self, *, start: int = 0, end: int = -1) -> list[Card]:
        result = []

        if end < 0:
            end = len(self.cards) + end
        elif end <= start:
            return result

        result = [self.cards[i] for i in range(start, end+1)]

        del self.cards[start:end+1]

        return result

    def putOne(self, card: Card | None, pos: int = 0) -> None:
        """put card into position pos moving all cards down.  POS 0 is top of deck -1 is last card"""
        if card is None:
            return

        if pos < 0:
            pos = len(self.cards) + pos

        self.cards.insert(pos, card)

    def appendOne(self, card) -> None:
        if card is None:
            return
        self.cards.append(card)

    def appendMany(self, cards: list[Card]) -> None:
        if cards is None:
            return
        if not isinstance(cards, list) or len(cards) == 0:
            return

        self.cards.extend(cards)


"""
Math:

c = [ c0, c1, c2]

putOne(c, 0) <- [ c, c0, c1, c2]
putOne(c, -1)
pos = len() + (-1) = 3 - 1 = 2

"""

"""
# build a deck by inserting a single card with various methods
d = Deck()
d.putOne(Card(value=CardValue.TWO,suit=CardSuit.SPADES))
d.putOne(Card(value=CardValue.ACE,suit=CardSuit.SPADES), pos=0)
d.putOne(Card(value=CardValue.THREE,suit=CardSuit.SPADES), pos=d.size())
d.appendOne(Card(value=CardValue.FOUR,suit=CardSuit.SPADES))

# remove the last card
card = d.getOne(pos=-1)

cards = d.getManySlice(start=1,end=2)
print("done")
"""
