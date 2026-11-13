# tiny-chess-01 — a 4 KB Python chess engine

Entry for the make.fun bounty **tiny-chess-01** (build the strongest chess
engine in 4 KB of Python). One file, `main.py`, standard library only.

## Design

- **Board:** 0x88 (128 squares), signed pieces, incremental material +
  piece-square score, Zobrist hashing.
- **Search:** negamax alpha-beta with iterative deepening to a **fixed node
  budget** (deterministic — no wall clock, no unseeded randomness), so every
  trial replays move-for-move.
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

## Tests

- **Perft:** startpos, Kiwipete, en-passant/pin, promotions and two more
  positions — all counts correct, and the incremental evaluation matches a
  from-scratch recompute over 300 random games (0 mismatches).
- **Practice gauntlet (kit trial-0):** see the run log in the repo history;
  Elo is computed by the kit's scorer against the eight house anchors.

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
