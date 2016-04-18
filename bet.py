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
        return table

    def get_in_play_bet(self):
        return self.teams[self.refunds.index(0)]

    def get_refund(self, index, stake_list):
        if index == 0:
            max_of_pre_match = max([stake_list[1], stake_list[2]])
            if stake_list[0] > 50 and stake_list[1] > 50 and stake_list[2] > 50:
                return_value = 50
            elif stake_list[0] < 50 and max_of_pre_match > stake_list[0]:
                return_value = stake_list[0]
            elif stake_list[0] < 50 and max_of_pre_match < stake_list[0]:
                return_value = max_of_pre_match
            else:
                if max_of_pre_match < 50:
                    return_value = max_of_pre_match
                else:
                    return_value = 50
            return [0, return_value, return_value]

        if index == 1:
            max_of_pre_match = max([stake_list[0], stake_list[2]])
            if stake_list[1] > 50 and stake_list[0] > 50 and stake_list[2] > 50:
                return_value = 50
            elif stake_list[1] < 50 and max_of_pre_match > stake_list[1]:
                return_value = stake_list[1]
            elif stake_list[1] < 50 and max_of_pre_match < stake_list[1]:
                return_value = max_of_pre_match
            else:
                if max_of_pre_match < 50:
                    return_value = max_of_pre_match
                else:
                    return_value = 50
            return [return_value, 0, return_value]

        if index == 2:
            max_of_pre_match = max([stake_list[0], stake_list[1]])
            if stake_list[2] > 50 and stake_list[0] > 50 and stake_list[1] > 50:
                return_value = 50
            elif stake_list[2] < 50 and max_of_pre_match > stake_list[2]:
                return_value = stake_list[1]
            elif stake_list[2] < 50 and max_of_pre_match < stake_list[2]:
                return_value = max_of_pre_match
            else:
                if max_of_pre_match < 50:
                    return_value = max_of_pre_match
                else:
                    return_value = 50
            return [return_value, return_value, 0]

def get_difference(profit_list):
    sorted_list = sorted(profit_list, key=float)
    return (
        (sorted_list[2] - sorted_list[1])
        + (sorted_list[2] - sorted_list[0])
        + (sorted_list[1] - sorted_list[0])
    )

def main():
    teams = [sys.argv[1], sys.argv[2]]
    odds = map(float, sys.argv[3:])

    best_equal_bet = None
    best_equal_total_profit = 0

    best_home_win_profit = 0
    best_home_win_bet = None

    best_draw_profit = 0
    best_draw_bet = None

    best_away_win_profit = 0
    best_away_win_bet = None

    for a in range(10, 110):
        for b in range(10, 110):
            for c in range(10, 110):
                this_bet = MatchedBet(teams, odds, [a, b, c])

                if sum(1 for n in this_bet.profits if n < 0) == 0:
                    # Best equal profit
                    if (get_difference(this_bet.profits) <= 3
                            and sum(this_bet.profits) > best_equal_total_profit):
                        best_equal_bet = this_bet
                        best_equal_total_profit = sum(this_bet.profits)

                    # Home Win
                    if (this_bet.profits[0] > best_home_win_profit
                            and this_bet.profits[1] > 8
                                and this_bet.profits[2] > 8):
                        best_home_win_profit = this_bet.profits[0]
                        best_home_win_bet = this_bet

                    # Draw
                    if (this_bet.profits[1] > best_draw_profit
                            and this_bet.profits[0] > 8
                                and this_bet.profits[2] > 8):
                        best_draw_profit = this_bet.profits[1]
                        best_draw_bet = this_bet

                    # Away Win
                    if (this_bet.profits[2] > best_away_win_profit
                            and this_bet.profits[0] > 8
                                and this_bet.profits[1] > 8):
                        best_away_win_profit = this_bet.profits[2]
                        best_away_win_bet = this_bet

    print "\nBest equal profit"
    print best_equal_bet
    print "In play bet: {0}".format(best_equal_bet.get_in_play_bet())

    print "\nBest home win"
    print best_home_win_bet
    print "In play bet: {0}".format(best_home_win_bet.get_in_play_bet())

    print "\nBest draw"
    print best_draw_bet
    print "In play bet: {0}".format(best_draw_bet.get_in_play_bet())

    print "\nBest away win"
    print best_away_win_bet
    print "In play bet: {0}".format(best_away_win_bet.get_in_play_bet())

if __name__ == "__main__":
    main()
