# Chess.OS ♟️

A complete two-player chess game built from scratch in Python and Pygame — no chess libraries, no game engines. Every rule, from piece movement to en passant, is implemented by hand.

![Chess.OS gameplay](screenshot.png)
<!-- Replace with your actual screenshot or GIF filename -->

## Features

- **Full piece movement** — all six piece types with path-blocking and capture logic
- **Check, checkmate, and stalemate detection** — via move simulation across all legal responses
- **Castling** — both wings, with complete legality checks: unmoved king and rook, clear path, not castling out of or through check
- **En passant** — with the one-move capture window tracked via last-move state
- **Pawn promotion** — interactive selection menu (queen, rook, bishop, knight), board freezes until a choice is made
- **Turn system** — enforced alternation with illegal-move rejection (can't move into or leave your king in check)
- **Game-over screen** — dimmed board overlay with result banner and winner announcement

## How to Run

1. Install Python 3.x
2. Install Pygame:
3. Clone this repo and run:
 -python chess.py

Piece images must be in the same directory as the script.

## How to Play

- Click a piece to select it (highlighted in red), click a destination square to move it
- Castle by moving the king two squares toward a rook
- When a pawn reaches the last rank, choose its promotion piece from the left panel

## Known Limitations

Documented deliberately — these are edge cases accepted for scope:

- Checkmate/stalemate detection does not consider en passant captures as escape moves (cannot occur in normal play, only in composed positions)
- Threefold repetition and the fifty-move rule are not automated — draws are agreed between players
- Insufficient-material draws are not auto-detected

## Built With

- Python 3
- Pygame
