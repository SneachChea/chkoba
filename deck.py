import random
from collections import namedtuple
from itertools import combinations

CARDS = (1, 2, 3, 4, 5, 6, 7, "Q", "J", "K")
VAL_CARDS= {1: 1,
            2: 2,
            3: 3,
            4:4,
            5:5,
            6:6,
            7:7,
            "Q":8,
            "J":9,
            "K":10}

TYPE = ("S", "H", "C", "D")

Card = namedtuple("Card", field_names=["card","type", "val"])


class ChkobaDeck:
    def __init__(self, seed: int | None= None):
        self.deck = self.create_full_deck()
        random.seed(seed)

    @staticmethod
    def create_full_deck() -> list[Card]:
        tmp_val = []
        for card in CARDS:
            for type in TYPE:
                tmp_val.append(Card(card=card, type=type, val=VAL_CARDS[card]))
        return tmp_val

    def __len__(self)->int:
        return len(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self, num_card:int = 1) -> list[Card]:
        if len(self) < num_card:
            raise IndexError("Not enough cards in your deck to draw {num_card} cards")
        draw_cards = []
        for i in range(num_card):
            draw_cards.append(self.deck.pop(0))
        return draw_cards


class Table:
    def __init__(self):
        self.table = []

    def add_cards(self, cards: list[Card] | Card) -> None:
        if isinstance(cards, list):
            self.table.extend(cards)
        elif isinstance(cards, Card):
            self.table.append(cards)
        else:
            raise TypeError("Argument should be either a list of Cards or a single Card")

    def view(self):
        if len(self.table) == 0:
            print('{}')
        else:
            for card in self.table:
                print(f"{card}")

    def __len__(self)->int:
        return len(self.table)

    def get_total_value(self)->int:
        if len(self.table)==0:
            return 0
        return sum(card.val for card in self.table)
    def play_card(self, player_hand: "PlayerHand", card_or_index: Card | int | None = None) -> list[Card]:
        """Play a card from a player's hand to interact with the table.

        The rules:
          - If a table card has the same value as the played card, the player takes that
            table card and the played card; both go to the player's pile.
          - If no single table card matches, the player may take any combination of
            table cards whose values sum exactly to the played card value.
            If several combinations match, the combination with the largest number of
            cards is chosen (greedy for biggest capture).
          - If no match is possible, the played card is simply placed on the table.

        Args:
            player_hand: PlayerHand that will play the card.
            card_or_index: Card object or index in the player's hand to play (or None to
                           play the first card).

        Returns:
            List[Card]: the cards captured (includes the played card); empty list if nothing captured.
        """
        # remove the played card from the player's hand
        played_card = player_hand.use_card(card_or_index)

        # find a direct same-value match on the table
        for table_card in self.table:
            if table_card.val == played_card.val:
                # remove matched table card and collect
                self.table.remove(table_card)
                player_hand.collect_cards([played_card, table_card])
                return [played_card, table_card]

        # Try all combinations of table cards to find sums equal to played_card.val
        cards_on_table = list(self.table)
        matches: list[list[Card]] = []
        for r in range(1, len(cards_on_table) + 1):
            for comb in combinations(cards_on_table, r):
                # Use numpy to compute sum per instructions; convert to python int for comparison
                if int(sum([c.val for c in comb])) == played_card.val:
                    matches.append(list(comb))

        if matches:
            # choose combination with the largest number of cards (deterministic choice)
            best = max(matches, key=len)
            # remove captured cards from the table
            for c in best:
                self.table.remove(c)
            player_hand.collect_cards([played_card] + best)
            return [played_card] + best

        # No capture possible — place the played card on the table
        self.table.append(played_card)
        return []



class PlayerHand:
    def __init__(self, first_card: Card | None = None):
        self.hand = [] if first_card is None else [first_card]
        self.pile: list[Card] = []

    def receive_cards(self, cards: list[Card] | Card):
        if isinstance(cards, list):
            self.hand.extend(cards)
        else:
            self.hand.append(cards)

    def view(self):
        if len(self.hand)==0:
            print("{}")
        else:
            for card in self.hand:
                print(f"{card}")

    def use_card(self, card_or_index: Card | int | None = None) -> Card:
        """
        Remove and return a card from the hand.

        - If `card_or_index` is None, remove and return the first card.
        - If it is an int, remove and return the card at that index.
        - If it is a Card, remove and return that card from the hand.
        Raises IndexError when the hand is empty, ValueError when the requested
        card or index is not present, or TypeError for invalid argument type.
        """
        if len(self.hand) == 0:
            raise IndexError("No cards in hand to use")

        # default: pop the first card (consistent with draw())
        if card_or_index is None:
            return self.hand.pop(0)

        # remove by index
        if isinstance(card_or_index, int):
            if card_or_index < 0 or card_or_index >= len(self.hand):
                raise IndexError(f"Index {card_or_index} out of range")
            return self.hand.pop(card_or_index)

        if isinstance(card_or_index, Card):
            try:
                self.hand.remove(card_or_index)
                return card_or_index
            except ValueError:
                raise ValueError(f"Card {card_or_index} not in hand")

        raise TypeError("Argument must be None, an int (index) or a Card")

    def collect_cards(self, cards: list[Card] | Card) -> None:
        """Add captured cards to player's pile.

        Args:
            cards: single Card or list of Cards to add to pile.
        """
        if isinstance(cards, list):
            self.pile.extend(cards)
        else:
            self.pile.append(cards)