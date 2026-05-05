from auction_game.interfaces import AuctionBot, AuctionState, MIN_BID_INCREMENT


class ValueTrapBot(AuctionBot):
    def __init__(self) -> None:
        self._chaser_seen = False
        self._opponent_opened_below_me = False

    def _fair_bid(self, state: AuctionState) -> int:
        return min(state.item.value + MIN_BID_INCREMENT, state.my_budget)

    def _trap_bid(self, state: AuctionState) -> int:
        return min(state.item.value + 18_000_000, state.my_budget)

    def choose_bid_round_1(self, state: AuctionState) -> int:
        trap_bid = self._trap_bid(state)
        if self._chaser_seen and state.opponent_budget >= trap_bid + MIN_BID_INCREMENT:
            return trap_bid
        return self._fair_bid(state)

    def choose_bid_round_2(self, state: AuctionState, my_bid: int, opponent_bid: int) -> int:
        self._opponent_opened_below_me = opponent_bid <= my_bid
        return my_bid

    def choose_bid_round_3(self, state: AuctionState, my_bid: int, opponent_bid: int) -> int:
        if self._opponent_opened_below_me and opponent_bid >= my_bid + MIN_BID_INCREMENT:
            self._chaser_seen = True
        return my_bid


BOT_CLASS = ValueTrapBot
