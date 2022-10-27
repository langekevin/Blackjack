"""Blackjack card game
Name: Kevin Lange


Rules:
    - A shuffled card deck with 52 cards exists
    - The player gets two cards at the beginning
    - The player has to decide if he wants to draw a card or to stop
    - The player can draw cards as long as he has less than 21 points
    - If the player has finished and did not lose, the host continues
    - He draws cards as long as his score is below 17
    - After the host is finished, the cards will be compared
    - If either the player or the host gets a blackjack (picture card and ass)
      the person with the blackjack wons
    - There is the possibility of investing money at the beginning and
      using the money during the game
"""
from os import system, name
from random import shuffle
from enum import Enum
from typing import List
from dataclasses import dataclass
from time import sleep


@dataclass
class Balance:
    """
    Balance of the player
    """
    player_balance: int


def get_input_int(user_message: str, min_input: int = 1, max_input: int = 999999) -> int:
    """Asks for an integer input from the user.

    Args:
        user_message (str): Message for the user

    Returns:
        int: Integer that the user puts in.
    """
    val = 0
    while True:
        _input = input(user_message)
        try:
            val = int(_input)
        except:
            print("This was not a valid integer. Please try again.")
            continue

        if min_input <= val <= max_input:
            return val
        
        if min_input > val:
            print(f"The entered value should exceed {min_input}")
        else:
            print(f"The maximum input should not exceed {max_input}")


def clear_screen() -> int:
    """
    Clears the screen of the user.
    """
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    return 0


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


def create_card_deck() -> List[Card]:
    """Creates the card deck and returns it

    Returns:
        List[Card]: List with instances of type Card
    """
    cards = []
    for i in range(13):
        for suit in ['Red diamond', 'Black clubs', 'Red heart', 'Black spade']:
            if i < 9:
                cards.append(Card(i + 2, f"{suit} {i + 2}", CardTypes.NUMBER))
            elif i == 9:
                cards.append(Card(10, f'{suit} Jack', CardTypes.PICTURE))
            elif i == 10:
                cards.append(Card(10, f'{suit} Lady', CardTypes.PICTURE))
            elif i == 11:
                cards.append(Card(10, f'{suit} King', CardTypes.PICTURE))
            else:
                cards.append(Card(11, f'{suit} Ass', CardTypes.ASS))
    return cards


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


def draw_card(player: Player, cards: List[Card]) -> None:
    """Function draws a card and adds it to the card deck
    of the player.

    Args:
        player (Player): Object of class Player
        cards (List[Card]): List of cards
    """
    new_card = cards.pop()
    if player.is_host:
        print(f"The host got a new card:     {new_card}")
    else:
        print(f"You got a new card:          {new_card}")
    player.add(new_card)


def player_plays(player: Player, cards: List[Card]) -> bool:
    """Function asks the user for decisions until the user
    has stopped or is busted.

    Args:
        player (Player): Instance of class Player
        cards (List[Card]): List with elements of class Card

    Returns:
        bool: True, if user has not lost
    """
    decision = "y"
    while decision != 'n':
        print(f"\nYour current score is: {player.score}\nYou have the following cards:")
        for card in player.cards:
            print(f"\t{str(card)}")

        decision = input("Do you want to draw a card or stop (y/n)?").lower()
        if decision == 'y':
            draw_card(player, cards)
            if player.score >= 21:
                print("You lost")
                return False
        else:
            print("You decided to end the game")
            print(f"You have a score of {player.score}")
            return True


def host_plays(host: Player, cards: List[Card]) -> True:
    """Function that plays for the host.

    Args:
        host (Player): Object of class Player
        cards (list): List of cards

    Returns:
        True: True if Host has not lost the game
    """
    done = False
    while not done:
        if host.score < 17:
            draw_card(host, cards)
            for card in host.cards:
                print(f"\t{str(card)}")
        elif host.score >= 17:
            return True

        if host.has_blackjack():
            print("Host has a blackjack! He won!")
            return True

        if host.score >= 21:
            print(f"Host has a score of {host.score}. You won")
            return False


def main(balance: Balance) -> None:
    """
    Main function starts the game.

    Args:
        balance (Balance): object of class Balance that represents
            the current balance (money) of the player.
    """

    this_rounds_invest = get_input_int(f'You have {balance.player_balance} in your bank. How much money do you want to invest this round? ', 1, balance.player_balance)

    cards = create_card_deck()
    shuffle(cards)

    player = Player()
    host = Player(is_host=True)
    draw_card(player, cards)
    draw_card(host, cards)
    draw_card(player, cards)

    if player.has_blackjack():
        print("Blackjack! You won!")
        balance.player_balance += this_rounds_invest * .5
        return

    result_player = player_plays(player, cards)
    if not result_player:
        balance.player_balance -= this_rounds_invest
        return

    print('\nThe host is playing now:\n')

    result_host = host_plays(host, cards)

    if not result_host:
        balance.player_balance += this_rounds_invest
        print("The host lost the game")
    elif player.score > host.score:
        balance.player_balance += this_rounds_invest
        print("You won")
    elif host.score > player.score:
        balance.player_balance -= this_rounds_invest
        print("You lost")
    else:
        print("The host and you got the same points")


if __name__ == '__main__':
    clear_screen()
    print("WELCOME TO BLACKJACK!")
    sleep(2)
    clear_screen()

    total_money_spend = get_input_int('Enter the amount of money you want to invest: ', 1, 100_000)
    balance = Balance(total_money_spend)

    while True:
        main(balance)

        if balance.player_balance <= 0:
            print("Your broke. Go home!")
            break
        else:
            print(f"You now have CHF {balance.player_balance} in your bank.")

        if input('Do you want to play again? ') != 'y':
            break
        else:
            clear_screen()
