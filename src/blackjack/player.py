from typing import List
from .cards import CardTypes, Card


class Player:
    """
    Class for all the things that have to do with the player
    """
    def __init__(self, cards: list = None, is_host: bool = False) -> None:
        if cards is None:
            cards = []
        self.cards = cards
        self._is_host = is_host
        self._score = self.__calc_score()

    @property
    def score(self) -> int:
        """Returns the current score of the player

        Returns:
            int: Score
        """
        return self._score

    @property
    def is_host(self) -> bool:
        """Returns if the player is a host or not

        Returns:
            bool: True if player is the host
        """
        return self._is_host

    def add(self, card: Card) -> None:
        """Adds a card to the list of cards from the player

        Args:
            card (Card): New card from the user
        """
        self.cards.append(card)
        if not self._is_host:
            self.correct_ass_value()
        self._score = self.__calc_score()

    def has_blackjack(self) -> bool:
        """Checks if the user has a blackjack with his first two cards

        Returns:
            bool: True, if user has a blackjack else False
        """
        has_ass = False
        has_picture_or_ten = False
        for card in self.cards[:2]:
            if card.type == CardTypes.ASS:
                has_ass = True
            elif card.value >= 10:
                has_picture_or_ten = True
        return has_ass and has_picture_or_ten

    def correct_ass_value(self) -> None:
        """Corrects the values of the asses in the carddeck of the player
        """
        if CardTypes.ASS not in [card.type for card in self.cards]:
            return

        for card in self.cards:
            if card.type == CardTypes.ASS:
                card.value = 11

        for card in self.cards:
            if card.type == CardTypes.ASS and card.value > 1 and self.__calc_score() >= 21:
                card.value = 1
            elif self.__calc_score() < 21:
                break

    def __calc_score(self) -> int:
        """Calculates the current score of the player

        Returns:
            int: Score of the player
        """
        return sum([card.value for card in self.cards])
