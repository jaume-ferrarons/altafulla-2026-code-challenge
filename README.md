# Auction Game Prototype

<!-- leaderboard:start -->
## Latest Leaderboard

Last run config: `budget=200000000` `items=20` `min_value=8000000` `max_value=16000000` `seed=random`

| Rank | User | Bot | Win Rate | Wins | Matches | Score |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | jaume | codex_fun | 100.0% | 26 | 26 | 5_958_360_888 |
| 2 | ruben-abad | aggressive_bully | 92.3% | 24 | 26 | 5_984_444_371 |
| 3 | blai | mango | 92.3% | 24 | 26 | 5_880_668_580 |
| 4 | jaume | king | 84.6% | 22 | 26 | 5_741_408_888 |
| 5 | ruben-abad | breakpoint_denier | 76.9% | 20 | 26 | 6_305_744_695 |
| 6 | ruben-abad | tit_for_tat | 73.1% | 19 | 26 | 6_342_381_957 |
| 7 | miguellobato84 | late_raiser | 69.2% | 18 | 26 | 6_565_176_923 |
| 8 | miguellobato84 | value_sniper | 69.2% | 18 | 26 | 6_452_895_807 |
| 9 | ruben-abad | budget_aware_bidder | 69.2% | 18 | 26 | 6_071_684_227 |
| 10 | ruben-abad | value_hunter | 61.5% | 16 | 26 | 6_557_514_379 |
| 11 | demo-bots | greedy_value | 61.5% | 16 | 26 | 4_721_126_818 |
| 12 | ruben-abad | zero_intelligence_constrainer_rng | 50.0% | 13 | 26 | 6_481_461_429 |
| 13 | demo-bots | copycat_bidder | 50.0% | 13 | 26 | 5_270_753_204 |
| 14 | miguellobato84 | scarcity_aware | 46.2% | 12 | 26 | 4_759_120_106 |
| 15 | miguellobato84 | noisy_opportunist | 42.3% | 11 | 26 | 5_187_153_542 |
| 16 | ruben-abad | zero_intelligence_constrainer | 38.5% | 10 | 26 | 6_191_117_549 |
| 17 | miguellobato84 | copycat_counterbidder | 38.5% | 10 | 26 | 5_862_087_831 |
| 18 | miguellobato84 | anti_leader | 38.5% | 10 | 26 | 4_837_080_459 |
| 19 | martin | value_trap | 38.5% | 10 | 26 | 4_762_144_167 |
| 20 | ruben-abad | patient_sniper | 30.8% | 8 | 26 | 6_362_491_906 |
| 21 | miguellobato84 | balanced_portfolio | 30.8% | 8 | 26 | 5_893_179_440 |
| 22 | demo-bots | steady_bidder | 30.8% | 8 | 26 | 4_503_468_285 |
| 23 | miguellobato84 | cash_preserver | 23.1% | 6 | 26 | 4_307_449_556 |
| 24 | ruben-abad | category_synergist | 15.4% | 4 | 26 | 5_486_433_362 |
| 25 | miguellobato84 | early_domination | 11.5% | 3 | 26 | 2_935_539_757 |
| 26 | miguellobato84 | deterministic_heuristic | 11.5% | 3 | 26 | 1_704_620_989 |
| 27 | demo-bots | random_bidder | 3.8% | 1 | 26 | 866_785_136 |

<!-- leaderboard:end -->

## What Is This Project About?

This repository contains a lightweight tournament engine for the conference
auction game. It is designed to be fast enough for all-vs-all evaluation on
each submission.

Each bot gets a `200_000_000` budget by default and competes across `20`
auctions. Each item is sold through 3 bidding rounds: a blind opening bid, a
second bid after both opening bids are revealed, and a final third bid after
the second bids are revealed. Item values are generated randomly for each
tournament run within a configured range, and final score is:

```text
sum(won item values) + category bonuses + money left
```

That keeps saving cash relevant without making "buy nothing" dominant, as long
as the total item slate is worth more than the initial budget.

Category bonuses use a soft milestone curve per category. If a bot wins `n`
items in a category with total category value `v`, the bonus rate is:

```text
min(0.06 * max(0, n - 1) + 0.02 * max(0, n - 3), 0.30)
```

So repeated wins in a category matter, but the bonus ramps gradually and caps
at `30%` of that category's total value.

## Setup

```bash
uv sync
```

## Run the demo

```bash
uv run python -m auction_game.main
```

## Bot API

Challenge participants should implement a class that inherits from
`auction_game.AuctionBot` and export it as `BOT_CLASS`.

Bots are discovered from this folder structure:

```text
auction_game/bots/<user-name>/<bot-name>.py
```

Each participant may submit one or more bots under their own `<user-name>`
directory.

The repository includes sample bots under `auction_game/bots/demo-bots/`.

```python
from auction_game import AuctionBot, AuctionState


class MyBot(AuctionBot):
    def choose_bid_round_1(self, state: AuctionState) -> int:
        return min(state.item.value, state.my_budget)

    def choose_bid_round_2(self, state: AuctionState, my_bid: int, opponent_bid: int) -> int:
        return max(my_bid, min(opponent_bid + 1, state.my_budget))

    def choose_bid_round_3(self, state: AuctionState, my_bid: int, opponent_bid: int) -> int:
        return max(my_bid, min(opponent_bid + 1, state.my_budget))


BOT_CLASS = MyBot
```

`AuctionState` includes the current item, both remaining budgets, prior bids,
prior won items, the current round index, and total rounds. In rounds 2 and 3,
bots receive the standing bids explicitly through the method arguments and may
only keep or raise their own previous bid. A raise must beat the opponent's
current standing bid by at least `1_000_000` by default.

## Submission Rules

- Submit only bots under your own directory, using
  `auction_game/bots/<user-name>/<bot-name>.py`. You may submit multiple bot
  files under your own `<user-name>` directory.
- Do not modify the engine, scoring, interfaces, validator, loader, leaderboard,
  demo bots, or other participants' files as part of a ranked submission.
- Your bot may only use the information provided through `AuctionState`,
  `my_bid`, and `opponent_bid`.
- Bots must not modify repository or process state from inside bot code,
  including monkey-patching imported modules, globals, builtins, or
  `sys.modules`.
- Bots must not use the network, shell commands, subprocesses, filesystem
  access, environment variables, or hidden repository data at runtime.
- Submissions should pass `python -m auction_game.validate_bots`.

Full participant and Codex-specific rules are documented in [AGENTS.md](AGENTS.md).
