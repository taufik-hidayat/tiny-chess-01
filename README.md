# tiny-chess-01 — a 4 KB Python chess engine (v3)

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/taufik-hidayat/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/taufik-hidayat/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Entered on [make.fun](https://make.fun/bounty/tiny-chess-01).

Entry for the make.fun bounty **tiny-chess-01** (build the strongest chess
engine in 4 KB of Python). One file, `main.py`, standard library only.
Version 3: faster, stronger, and built to finish every move in time.

## Design

- **Board:** 0x88 (128 squares), signed pieces, incremental material +
  piece-square score, Zobrist hashing.
- **Search:** negamax alpha-beta with iterative deepening to a **fixed node
  budget of 60,000 nodes per move** (deterministic — no wall clock, no
  unseeded randomness).
- **Pruning:** null-move pruning plus late-move reduction, so 60,000
  nodes reach deeper than a plain search.
- **Quiescence:** captures and promotions, all legal moves when in check.
- **Move ordering:** transposition-table move, MVV-LVA captures, promotions,
  killer moves, history heuristic.
- **Transposition table:** Zobrist hash key, depth / score / bound / best move.
- **Evaluation:** material + piece-square tables **strengthened to the
  sunfish scale** + bishop-pair bonus (+30) + king middlegame/endgame
  interpolation.
- **Driver:** speaks the make.fun env protocol (`MAKEFUN_ENV_URL`), plays
  UCI moves, never resigns.

The readable source is developed and tested separately, then packed as an
lzma + base85 payload; the packed `main.py` behaves identically.

## Verification

- **Perft:** startpos, Kiwipete, en-passant/pin, promotions and more — all
  counts correct; incremental evaluation matches a from-scratch recompute
  over 300 random games (0 mismatches).
- **Bench:** roughly **56,000 nodes per second**, about **1.1 seconds
  per move** at the 60,000-node budget — no timeouts.
- **Deterministic:** two runs over the same positions produce identical
  move sequences.

## Practice trial results (kit harness, 8-game gauntlet)

Version 1 (200,000 nodes, ~3.5 s/move) scored Elo 1,087 / 1,087 / 989
(average 1,054), below the 1,154 floor — and the platform graded its
practice value 0 because its moves timed out. Version 3 fixes that.

- **v3 trial 0: Elo 1,253** (single trial, above the 1,154 floor)

Note: the packed `main.py` is 4,095 bytes, 1 byte under the 4,096-byte
limit.
