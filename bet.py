"""
    Small program to determine the profits using the dutch method of betting
    on a football match.
"""

import sys

class MatchedBet(object):
    """
        Data structure to hold the contents of a bet.
    """
    def __init__(self, teams, odds, stakes):
        self.teams = [teams[0], "Draw", teams[1]]
        self.odds = odds
        self.stakes = stakes
        self.returns = [
            self.stakes[i] * self.odds[i] for i in range(len(stakes))
        ]
        self.refunds = self.get_refund(
            self.odds.index(max(self.odds)), self.stakes
        )
        self.total_returns = [
            self.returns[i] + self.refunds[i] for i in range(len(self.refunds))
        ]
        self.outlay = sum(self.stakes)
        self.profits = [
            self.total_returns[i] - self.outlay for i in range(
                len(self.total_returns)
            )
        ]

    def __str__(self):
        row_format = (
            "{0:10} {1:>6} {2:>5} {3:>8} {4:>6} {5:>13} {6:>13} {7:>6}"
        )
        table = row_format.format(
            "Result",
            "Odds",
            "Stake",
            "Returns",
            "Refund",
            "Total Returns",
            "Total Outlay",
            "Profit"
        )
        for a in range(0, 3):
            table += '\n'
            table += (
                row_format
            ).format(
                self.teams[a],
                self.odds[a],
                self.stakes[a],
                self.returns[a],
                self.refunds[a],
                self.total_returns[a],
                self.outlay,
                self.profits[a]
            )
        table += "\nIn play bet: {0}".format(self.get_in_play_bet())
        table += "\nB365 pre-match bet: {0}".format(self.get_bet_365_pre_match_bet())
        table += "\nOther pre-match bet: {0}".format(self.get_other_pre_match_bet())
        return table

    def get_in_play_bet(self):
        return self.teams[self.refunds.index(0)]

    def get_difference(self):
        sorted_list = sorted(self.profits, key=float)
        return (
            (sorted_list[2] - sorted_list[1])
            + (sorted_list[2] - sorted_list[0])
            + (sorted_list[1] - sorted_list[0])
        )

    def get_bet_365_pre_match_bet(self):
        pre_match_bets = list(self.stakes)
        del pre_match_bets[self.refunds.index(0)]
        if sum(1 for n in pre_match_bets if n > 50) == 2:
            return "Any"
        max_of_pre_match = max(pre_match_bets)
        return self.teams[self.stakes.index(max_of_pre_match)]

    def get_other_pre_match_bet(self):
        pre_match_bets = list(self.stakes)
        del pre_match_bets[self.refunds.index(0)]
        if sum(1 for n in pre_match_bets if n > 50) == 2:
            return "Any"
        min_of_pre_match = min(pre_match_bets)
        return self.teams[self.stakes.index(min_of_pre_match)]

    def get_refund(self, index, stake_list):
        pre_match_bets = list(stake_list)
        del pre_match_bets[index]
        in_play_bet_value = stake_list[index]
        max_of_pre_match = max(pre_match_bets)
        if sum(1 for n in stake_list if n > 50) == 3:
            refund_value = 50
        elif in_play_bet_value < 50 and max_of_pre_match > in_play_bet_value:
            refund_value = in_play_bet_value
        elif in_play_bet_value < 50 and max_of_pre_match < in_play_bet_value:
            refund_value = max_of_pre_match
        elif max_of_pre_match < 50:
            refund_value = max_of_pre_match
        else:
            refund_value = 50

        refund_list = [0, 0, 0]
        for i in range(0,3):
            if i != index:
                refund_list[i] = refund_value
        return refund_list

    def has_negative(self):
        if sum(1 for n in self.profits if n < 0) == 0:
            return False
        return True

    def sum_of_profits(self):
        return sum(self.profits)

    def home_win_profit(self):
        return self.profits[0]

    def draw_profit(self):
        return self.profits[1]

    def away_win_profit(self):
        return self.profits[2]

def main():
    teams = [sys.argv[1], sys.argv[2]]
    odds = [float(x) for x in sys.argv[3:]]

    # Initialise the bets
    best_equal_bet = MatchedBet(teams, odds, [1, 1, 1])
    best_home_win_bet = MatchedBet(teams, odds, [1, 1, 1])
    best_draw_bet = MatchedBet(teams, odds, [1, 1, 1])
    best_away_win_bet = MatchedBet(teams, odds, [1, 1, 1])

    for a in range(10, 110):
        for b in range(10, 110):
            for c in range(10, 110):
                this_bet = MatchedBet(teams, odds, [a, b, c])

                if not this_bet.has_negative():
                    # Best equal profit
                    if (this_bet.get_difference() <= 3
                            and this_bet.sum_of_profits()
                                > best_equal_bet.sum_of_profits()):
                        best_equal_bet = this_bet

                    # Home Win
                    if (this_bet.home_win_profit()
                            > best_home_win_bet.home_win_profit()
                                and this_bet.draw_profit() > 8
                                    and this_bet.away_win_profit() > 8):
                        best_home_win_bet = this_bet

                    # Draw
                    if (this_bet.draw_profit() > best_draw_bet.draw_profit()
                            and this_bet.home_win_profit() > 8
                                and this_bet.away_win_profit() > 8):
                        best_draw_bet = this_bet

                    # Away Win
                    if (this_bet.away_win_profit()
                            > best_away_win_bet.away_win_profit()
                                and this_bet.home_win_profit() > 8
                                    and this_bet.draw_profit() > 8):
                        best_away_win_bet = this_bet

    print "\nBest equal profit"
    print best_equal_bet

    print "\nBest home win"
    print best_home_win_bet

    print "\nBest draw"
    print best_draw_bet

    print "\nBest away win"
    print best_away_win_bet

if __name__ == "__main__":
    main()
