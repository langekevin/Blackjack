from os import system, name
from typing import List
from .cards import Card, CardTypes
from .player import Player


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
