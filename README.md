# ♦️ Chkoba – A Simple Python Implementation of the Tunisian Card Game

Chkoba is a traditional Tunisian card game played with a 40‑card deck.
This repository contains a minimal, fully‑documented implementation that can be used for:

- Quick simulations or data analysis (see `chkoba_simulation.ipynb`).
- A starting point for building more advanced game logic or AI.

---

## Project Structure

```
├── deck.py          # Core card/hand/table logic
├── test.ipynb       # Jupyter notebook with a large‑scale simulation
├── README.md        # You are reading it!
└── requirements.txt
```

### `deck.py`

`deck.py` implements the basic building blocks of Chkoba:

| Class | Purpose |
|-------|---------|
| **ChkobaDeck** | Generates a full 32‑card deck, shuffles it, and allows drawing cards. |
| **Table**      | Holds the current cards on the table; handles capture logic when a player plays a card. |
| **PlayerHand** | Represents a player's hand of cards and their captured pile. |

Key functions:

- `ChkobaDeck.create_full_deck()` – builds the 32‑card deck.
- `Table.play_card(player_hand, card_or_index)` – applies the capture rules:
  - Direct value match (single card).
  - Combination of table cards that sum to the played card’s value.
  - If no capture is possible, the card stays on the table.

The implementation uses Python’s built‑in types (`list`, `namedtuple`) and standard library modules (`random`, `collections`, `itertools`). No external dependencies are required for the core logic.

### `chkoba_simulation.ipynb`

`chkoba_simulation.ipynb` demonstrates how to use the module in practice:

1. **Simulation**  
   - Draws a large number of random hands (2 M iterations).
   - Plays a card from the first player onto the table.
   - Records how many cards each played card captures.

2. **Data Analysis**  
   - Uses `numpy` and `matplotlib` to compute mean, standard deviation, and plot distributions for each card value.
   - Includes helper functions (`plot_card_distribution`) for visualizing per‑card statistics.

The notebook is self‑contained; simply open it in Jupyter or VS Code’s Jupyter extension and run the cells. It will produce a series of plots that illustrate capture probabilities across card values.

---

## Installation

```bash
git clone https://github.com/your-username/chkoba.git
cd chkoba
pip install -r requirements.txt
```

> **Tip**: The core logic in `deck.py` has no external dependencies, so you can import it directly without installing the notebook requirements.

---

## Usage Example

```python
from deck import ChkobaDeck, Table, PlayerHand

# Initialise a shuffled deck
deck = ChkobaDeck()
deck.shuffle()

# Create players and table
player1 = PlayerHand()
player2 = PlayerHand()
table   = Table()

# Deal cards
player1.receive_cards(deck.draw(3))
player2.receive_cards(deck.draw(3))
table.add_cards(deck.draw(4))

# Play a card from player1
played_card = player1.hand[0]          # choose first card to play
captured = table.play_card(player1, played_card)

print(f"Captured {len(captured)} cards: {captured}")
```

---

## Contributing

Feel free to open issues or pull requests. Suggestions for additional game features (e.g., multi‑player logic, scoring, AI) are welcome!

---

## License

MIT © 2025
