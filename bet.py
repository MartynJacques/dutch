"""
    Small program to determine the profits using the dutch method of betting
    on a football match.
"""

import sys

class MatchedBet(object):
    """
        Data structure to hold the contents of a bet.
    """
    def __init__(self, teams, odds, stakes, bet_365_pre_match_bet):
        self.teams = [teams[0], "Draw", teams[1]]
        self.odds = odds
        self.stakes = stakes
        self.bet_365_pre_match_bet_index = self.teams.index(
            bet_365_pre_match_bet
        )
        self.returns = [
            self.stakes[i] * self.odds[i] for i in range(len(stakes))
        ]
        self.refunds = self.get_refund()
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
            "{0:10} {1:>6} {2:>5} {3:>8} {4:>6} {5:>13} {6:>13} {7:>6} {8:10}"
        )
        table = row_format.format(
            "Result",
            "Odds",
            "Stake",
            "Returns",
            "Refund",
            "Total Returns",
            "Total Outlay",
            "Profit",
            "When"
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
                self.profits[a],
                self.get_when()[a]
            )
        return table

    def get_difference(self):
        sorted_list = sorted(self.profits, key=float)
        return (
            (sorted_list[2] - sorted_list[1])
            + (sorted_list[2] - sorted_list[0])
            + (sorted_list[1] - sorted_list[0])
        )

    def get_when(self):
        when = ["Never", "Never", "Never"]
        when[self.get_in_play_bet_index()] = "Bet365 in play"
        when[self.get_other_pre_match_bet()] = "Other pre-match"
        when[self.bet_365_pre_match_bet_index] = "Bet365 pre-match"
        return when

    def get_in_play_bet_index(self):
        return self.odds.index(max(self.odds))

    def get_other_pre_match_bet(self):
        for x in range(0,3):
            if (x != self.get_in_play_bet_index()
                    and x != self.bet_365_pre_match_bet_index):
                return x

    def get_refund(self):
        in_play_index = self.get_in_play_bet_index()
        bet_365_pre_match_stake = self.stakes[self.bet_365_pre_match_bet_index]
        in_play_stake = self.stakes[in_play_index]

        if bet_365_pre_match_stake > 50 and in_play_stake > 50:
            refund_value = 50
        else:
            refund_value = min([bet_365_pre_match_stake, in_play_stake])

        refund_list = [0, 0, 0]
        for i in range(0,3):
            if i != in_play_index:
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
    try:
        teams = [sys.argv[1], sys.argv[2]]
        odds = [float(x) for x in sys.argv[3:6]]
        bet_365_pre_match_bet = sys.argv[6]
    except IndexError as e:
        print "Not enough arguments."
        print(
            "To run the program type 'python bet.py HOME_TEAM AWAY_TEAM '"
            "HOME_TEAM_ODDS DRAW_ODDS AWAY_TEAM_ODDS BET_365_PRE_MATCH_BET'"
        )
        exit(1)

    # Initialise the bets
    best_equal_bet = MatchedBet(teams, odds, [1, 1, 1], bet_365_pre_match_bet)
    best_home_win_bet = MatchedBet(teams, odds, [1, 1, 1], bet_365_pre_match_bet)
    best_draw_bet = MatchedBet(teams, odds, [1, 1, 1], bet_365_pre_match_bet)
    best_away_win_bet = MatchedBet(teams, odds, [1, 1, 1], bet_365_pre_match_bet)

    for a in range(10, 110):
        for b in range(10, 110):
            for c in range(10, 110):
                this_bet = MatchedBet(
                    teams,
                    odds,
                    [a, b, c],
                    bet_365_pre_match_bet
                )

                if not this_bet.has_negative():
                    # Best equal profit
                    if (this_bet.get_difference() <= 2
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
