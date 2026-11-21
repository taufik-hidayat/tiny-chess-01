# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/taufik-hidayat/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/taufik-hidayat/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Entry for the make.fun bounty **tiny-chess-01** — build the strongest chess
engine in 4 KB of Python. One file, `main.py`, Python 3 standard library
only, at most 4,096 bytes as committed.

## The engine

A 0x88-board negamax search with alpha-beta pruning and iterative deepening
on a fixed budget of 60,000 nodes per move (deterministic: no wall clock, no
unseeded randomness). Null-move pruning (R=3), late-move reductions with a
full-depth re-search when a reduced move beats alpha, a quiescence search
over captures, and move ordering by transposition-table move then MVV-LVA
captures. The transposition table is keyed on the board tuple plus side,
castling rights and en-passant square. The evaluation is material plus a
pawn-advance term. It talks to the trial env at `MAKEFUN_ENV_URL`
(`POST /game`, `/move`, `/resign`) and plays all 8 games of the gauntlet,
one against each house engine.

## Run it

```sh
python3 main.py
```

It needs `MAKEFUN_ENV_URL` set to the env of a trial; without it, it exits.

## Results

Practice trial-0 (local grade, kit's sealed env, 21 Nov 2026):

- **W2 D1 L5, 2.5 points, Elo 1173** (final floor 1,154 — passed)
- Wins vs depth-2 (855) as white and depth-3 (1,073) as black, both by
  checkmate; draw vs nodes-250k (1,497) as white by threefold repetition;
  losses vs depth-4 (1,199), nodes-100k (1,392), nodes-500k (1,596),
  nodes-1M (1,667), nodes-2M (1,712)
- Game plies: 75 / 98 / 144 / 35 / 71 / 97 / 110 / 103
- Spare budget: 9 bytes under the 4,096-byte cap (`main.py` is 4,087 bytes)
- Perft passes on startpos, kiwipete, and the four promotion positions
  (depth 3, plus depth-4 startpos 197,281); two runs on the same position
  return the same move (deterministic)

---

<sub>Entered on [make.fun](https://make.fun/?ref=2z9vc20p&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
