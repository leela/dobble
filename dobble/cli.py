from argparse import ArgumentParser, Namespace, Action
from collections.abc import Sequence
from typing import Any

from dobble.main import generate_dobble_cards, generate_dobble_game
from dobble import symbols


class CSVToSeqStore(Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: str | Sequence[Any] | None, option_string: str | None = None) -> None:
        values_seq = values.strip().split(",")
        setattr(namespace, self.dest, values_seq)

def add_list_cards_command(sub_parsers):
    list_cards_parser = sub_parsers.add_parser("list-cards", help="List card wise symbols")
    list_cards_parser.add_argument("-n", "--symbols-per-card", type=int, help="Numeric value", default=8)
    list_cards_parser.add_argument("-s", "--symbols", 
        help="comma seperated strings", 
        action=CSVToSeqStore, 
        default=symbols.ENGLISH_57_SYMBOLS
    )
    list_cards_parser.set_defaults(func=generate_dobble_cards)

def add_create_cards_command(sub_parsers):
    create_cards_parser = sub_parsers.add_parser("create-cards", help="Create PDF of dobble cards")
    create_cards_parser.add_argument("-n", "--symbols-per-card", type=int, help="Numeric value", default=8)
    create_cards_parser.add_argument("-s", "--symbols", 
        help="comma seperated strings", 
        action=CSVToSeqStore, 
        default=symbols.ENGLISH_57_SYMBOLS
    )
    create_cards_parser.set_defaults(func=generate_dobble_game)


def main():
    global_parser = ArgumentParser(
        prog="dobble",
        description="Generate dobble cards"
    )

    sub_parsers = global_parser.add_subparsers(
        title="sub-commands", 
        help="Card based commands"
    )
    add_list_cards_command(sub_parsers)
    add_create_cards_command(sub_parsers)
    args = global_parser.parse_args()
    if 'func' in args:
        res = args.func(args.symbols_per_card, args.symbols, True)

if __name__ == "__main__":
    main()