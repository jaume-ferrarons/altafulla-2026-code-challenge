# Auction Game Prototype

<!-- leaderboard:start -->
## Latest Leaderboard

Last run config: `budget=200000000` `items=20` `min_value=8000000` `max_value=16000000` `seed=random`

| Rank | User | Bot | Win Rate | Wins | Matches | Score |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | jaume | king | 86.7% | 13 | 15 | 3_348_911_034 |
| 2 | miguellobato84 | value_sniper | 80.0% | 12 | 15 | 3_857_091_589 |
| 3 | miguellobato84 | late_raiser | 73.3% | 11 | 15 | 3_823_034_767 |
| 4 | miguellobato84 | scarcity_aware | 66.7% | 10 | 15 | 2_931_618_631 |
| 5 | martin | value_trap | 66.7% | 10 | 15 | 2_781_624_771 |
| 6 | demo-bots | copycat_bidder | 66.7% | 10 | 15 | 2_607_282_438 |
| 7 | miguellobato84 | noisy_opportunist | 60.0% | 9 | 15 | 3_187_907_655 |
| 8 | miguellobato84 | copycat_counterbidder | 53.3% | 8 | 15 | 3_539_459_339 |
| 9 | miguellobato84 | anti_leader | 53.3% | 8 | 15 | 2_807_205_436 |
| 10 | demo-bots | greedy_value | 53.3% | 8 | 15 | 2_769_303_734 |
| 11 | miguellobato84 | balanced_portfolio | 33.3% | 5 | 15 | 3_442_874_442 |
| 12 | miguellobato84 | cash_preserver | 33.3% | 5 | 15 | 2_820_941_501 |
| 13 | demo-bots | steady_bidder | 33.3% | 5 | 15 | 2_605_579_735 |
| 14 | miguellobato84 | early_domination | 20.0% | 3 | 15 | 1_692_860_490 |
| 15 | demo-bots | random_bidder | 13.3% | 2 | 15 | 822_102_368 |
| 16 | miguellobato84 | deterministic_heuristic | 6.7% | 1 | 15 | 1_032_035_795 |

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
