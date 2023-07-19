import sys
import string
import random
from pprint import pprint
import pathlib

from dobble import utils

def generate_numbered_cards(symbols_per_card):
    """Generate Dobble cards using numbers. This uses symbols as numbers from 0 to n*(n-1), where n is symbols_per_card. 
    Dobble game contains a group of cards with fixed number of symbols per card, and there will be exactly one common 
    symbol between any two cards.
    
    This code is a building block to generate dobble cards with any type of symbols.

    HOW DOES IT WORKS:
    * Lets start with the first card, that contains 0 to n-1 symbols (n is symbols_per_card).
    * Any card that we create from now on, should have one symbol from first card(according to common symbol rule).
      So, we need to create set of cards for each symbol of the first card.
    * How can we make a set of cards for "one symbol"?
        - We know that, one symbol from first card will be in all cards in that specific set, 
            with (n-1)*(n-1) new symbols we can make (n-1) cards in a set.
        - By transposing and shifting/rolling those  (n-1)*(n-1) symbols, we can make (n-1) cards for every 
            symbol from the first card and those obey common symbol rule.
    """
    if symbols_per_card < 3:
        print("Dobble generator expects atleast 3 symbols per card.")
        return

    s = symbols_per_card

    cards = []
    first_card = list(range(s))
    cards.append(first_card)
    remaining_symbols = utils.create_matrix(rows=s-1, cols=s-1, use_num_sequence=True, seq_start_from=s)

    # Add transposed combination    
    cards.extend([[first_card[0]] + each for each in utils.transpose(remaining_symbols)])

    # add shifted combinations
    combinations = utils.get_diagonal_shifted_y_matrix_combs(remaining_symbols)
    for symbol, comb in zip(first_card[1:], combinations):
        cards.extend([[symbol] + each for each in comb])

    return cards


def generate_dobble_cards(symbols_per_card, symbols, shuffle_symbols):
    """Generate dobble cards for the given symbols (Make sure that symbols are unique).

    Rules to create Dobble cards:
    1. There will be exactly one common symbol between any two cards.
    2. Each card has equal number of symbols.
    3. No two symbols on a card are same.
    """

    if symbols_per_card < 3:
        sys.exit(utils.colored_text("Dobble generator expects atleast 3 symbols per card."))

    if not utils.is_prime(symbols_per_card-1):
        sys.exit(utils.colored_text(
            f"Implementation expects n - 1 to be a prime number where n is 'no of symbols per card'(Here n-1 ({symbols_per_card-1}) is not prime).")
        )

    no_of_symbols = symbols_per_card*(symbols_per_card-1) + 1
    no_of_cards = no_of_symbols

    if len(symbols) < no_of_symbols:
        sys.exit(utils.colored_text(
            f"Needed {no_of_symbols} symbols to make {symbols_per_card} symbols per card dobble set but given only {len(symbols)} symbols.")
        )

    numbered_cards = generate_numbered_cards(symbols_per_card)
    shuffled_symbols = random.sample(symbols, no_of_symbols) if shuffle_symbols else symbols
    mapping = dict(zip(range(no_of_symbols), shuffled_symbols))

    print(utils.colored_text(f"Total symbols used: {no_of_symbols}", "green"))
    print(utils.colored_text(f"Symbols per card: {symbols_per_card}", "green"))
    print(utils.colored_text(f"Total number of cards created: {no_of_cards}", "green"))

    symbol_cards = []
    for card in numbered_cards:
        symbol_cards.append([mapping.get(num) for num in card])

    pprint(symbol_cards)
    return symbol_cards


def cards_to_pdf(cards):
    """Convert list of given cards into pdf format
    """
    card_images = [utils.create_card(random.sample(card_symbols, len(card_symbols))) for card_symbols in cards]
    pdf_location = utils.get_unique_path(pathlib.Path.cwd() / "print", "dobble_{:02d}.pdf")
    if not card_images:
        return

    first_card = card_images[0]
    first_card.save(pdf_location, save_all=True, append_images=card_images[1:])
    return pdf_location


def generate_dobble_game(symbols_per_card, symbols = string.ascii_lowercase, shuffle_symbols=False):
    game_cards = generate_dobble_cards(symbols_per_card, symbols, shuffle_symbols)
    location = cards_to_pdf(game_cards)
    print(f"PDF is stored @ {location}")
    return location