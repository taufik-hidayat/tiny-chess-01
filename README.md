# tiny-chess-01 — a 4 KB Python chess engine

Entry for the make.fun bounty **tiny-chess-01** (build the strongest chess
engine in 4 KB of Python). One file, `main.py`, standard library only.

## Design

- **Board:** 0x88 (128 squares), signed pieces, incremental material +
  piece-square score, Zobrist hashing.
- **Search:** negamax alpha-beta with iterative deepening to a **fixed node
  budget of 200,000 nodes per move** (deterministic — no wall clock, no
  unseeded randomness), so every trial replays move-for-move.
- **Quiescence:** captures and promotions, all legal moves when in check;
  stand-pat otherwise.
- **Move ordering:** transposition-table move, MVV-LVA captures, promotions,
  two killer moves per ply, history heuristic (quiet moves ordered by a
  16K-entry table of past beta-cutoff bonuses).
- **Transposition table:** keyed by Zobrist hash, stores depth / score /
  bound flag / best move; mate scores adjusted by ply.
- **Evaluation:** material (pawn 100, knight 320, bishop 330, rook 500,
  queen 900) + piece-square tables (pawn advance/centre, knight/bishop/rook/
  queen centrality, king centralisation) + bishop-pair bonus (+30) +
  king middlegame/endgame interpolation. Repetition and the 50-move rule
  score 0 inside the search.
- **Driver:** speaks the make.fun env protocol (`MAKEFUN_ENV_URL`),
  plays UCI moves, replays the game history to rebuild repetition state,
  never resigns, falls back to the first legal move if needed.

Because the source is packed as an lzma + base85 payload to fit the
4,096-byte limit, the readable source is developed and tested separately
and then packed; the packed `main.py` is byte-identical in behaviour.

## Verification

- **Perft:** startpos, Kiwipete, en-passant/pin, promotions and two more
  positions — all counts correct, and the incremental evaluation matches a
  from-scratch recompute over 300 random games (0 mismatches).
- **Bench:** roughly **45,000–57,000 nodes per second**, about **3.5 seconds
  per move** at the 200,000-node budget, comfortably inside the 10-second
  per-move limit.
- **Deterministic:** two runs over the same positions produce byte-identical
  move sequences — no wall clock, no unseeded randomness anywhere.

## Practice trial results (kit harness, 8-game gauntlet)

Three practice trials against the eight house anchors (alpha-beta depth 2
up to 2,000,000 nodes per move):

- Trial 1: **Elo 1,087**
- Trial 2: **Elo 1,087**
- Trial 3: **Elo 989**
- **Average Elo: 1,054**

Honest note: this is **below the 1,154 Elo floor** required to qualify for
the final set. The engine beats the depth-2/3/4 anchors and loses to the
high-node anchors; the 4 KB size cap is the binding constraint, not the
search design. The entry is submitted as-is: a correct, deterministic,
well-tested engine that plays legal chess at the strongest level we could
fit into 4,096 bytes.

Note: the packed `main.py` is 4,088 bytes, 8 bytes under the 4,096-byte
limit, so the engine fits the size rule with a small margin.

## Running locally

The engine reads `MAKEFUN_ENV_URL` and plays the env protocol, e.g. with
the kit's practice harness:

```
MAKEFUN_ENV_URL=http://127.0.0.1:<port> python3 main.py
```

Or grade it with the kit (requires Docker):

```
node cli/makefun.mjs grade-local --kit . --bot <repo> --driver docker
```
