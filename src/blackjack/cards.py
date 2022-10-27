from enum import Enum


class CardTypes(Enum):
    """Enum describes the type of the card.
    - Number (0) is just a simple card which as as many points as
        there are written on the card.
    - Picture (1) is a card that is either a Jack, a Lady or a King
        and has always the value 10
    - The Value of a Ass (2) is either 1 or 11, depending on which case
        gives the player the advantage
    """
    NUMBER = 0
    PICTURE = 1
    ASS = 2


class Card:
    """_summary_
    """
    def __init__(self, value: int, suit: str, card_type: CardTypes) -> None:
        self._value = value
        self._suit = suit
        self._type = card_type

    @property
    def suit(self) -> str:
        """Returns the suit of the card

        Returns:
            str: Card suit
        """
        return self._suit

    @property
    def value(self) -> int:
        """Returns the value of the card

        Returns:
            int: Card value
        """
        return self._value

    @property
    def type(self) -> CardTypes:
        """Returns the type of the card as an enum of
        type CardTypes

        Returns:
            CardTypes: Enum
        """
        return self._type

    @value.setter
    def value(self, value: int) -> None:
        """Sets a new value for this card. This value can only be
        changed if the type of the card is an ass.

        Args:
            value (int): New value of the card
        """
        if self._type == CardTypes.ASS:
            self._value = value

    def __str__(self) -> str:
        return f"Card {self._suit} with a value of {self._value}"
