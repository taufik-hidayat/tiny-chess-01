# tiny-chess-01 — a 4 KB Python chess engine (v3)

Entry for the make.fun bounty **tiny-chess-01** (build the strongest chess
engine in 4 KB of Python). One file, `main.py`, standard library only.
Version 3: faster, stronger, and built to finish every move in time.

## Design

- **Board:** 0x88 (128 squares), signed pieces, incremental material +
  piece-square score, Zobrist hashing.
- **Search:** negamax alpha-beta with iterative deepening to a **fixed node
  budget of 60,000 nodes per move** (deterministic — no wall clock, no
  unseeded randomness), so every trial replays move-for-move.
- **Pruning:** null-move pruning plus late-move reduction, so 60,000
  nodes reach deeper than a plain search.
- **Quiescence:** captures and promotions, all legal moves when in check;
  stand-pat otherwise.
- **Move ordering:** transposition-table move, MVV-LVA captures, promotions,
  two killer moves per ply, history heuristic.
- **Transposition table:** keyed by Zobrist hash, stores depth / score /
  bound flag / best move; mate scores adjusted by ply.
- **Evaluation:** material (pawn 100, knight 320, bishop 330, rook 500,
  queen 900) + piece-square tables **strengthened to the sunfish scale** +
  bishop-pair bonus (+30) + king middlegame/endgame interpolation.
  Repetition and the 50-move rule score 0 inside the search.
- **Driver:** speaks the make.fun env protocol (`MAKEFUN_ENV_URL`),
  plays UCI moves, replays the game history to rebuild repetition state,
  never resigns, falls back to the first legal move if needed.

The readable source is developed and tested separately, then packed as an
lzma + base85 payload; the packed `main.py` behaves identically.

## Verification

- **Perft:** startpos, Kiwipete, en-passant/pin, promotions and two more
  positions — all counts correct, and the incremental evaluation matches a
  from-scratch recompute over 300 random games (0 mismatches).
- **Bench:** roughly **56,000 nodes per second**, about **1.1 seconds
  per move** at the 60,000-node budget, comfortably inside the per-move
  time limit — no timeouts.
- **Deterministic:** two runs over the same positions produce byte-identical
  move sequences — no wall clock, no unseeded randomness anywhere.

## Practice trial results (kit harness, 8-game gauntlet)

Trials against the eight house anchors (alpha-beta depth 2 up to
2,000,000 nodes per move). Version 1 (200,000 nodes, ~3.5 s/move) scored
Elo 1,087 / 1,087 / 989 (average 1,054), below the 1,154 floor — and the
platform graded its practice value 0 because its moves timed out.
Version 3 fixes that.

- **v3 trial 0: Elo 1,253** (single trial, above the 1,154 floor)

Honest note: trial 0 is a single trial, not an average. The entry is
submitted as-is: a correct, deterministic engine at the strongest level
we could fit into 4,096 bytes.

Note: the packed `main.py` is 4,095 bytes, 1 byte under the 4,096-byte
limit.

## Running locally

```
MAKEFUN_ENV_URL=http://127.0.0.1:<port> python3 main.py
```
