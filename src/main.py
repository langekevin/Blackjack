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
from random import shuffle
from time import sleep

from blackjack import (
    Balance,
    get_input_int,
    create_card_deck,
    draw_card,
    Player,
    player_plays,
    host_plays,
    clear_screen
)


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
