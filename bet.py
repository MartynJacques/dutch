import sys

class MatchedBet(object):
    def __init__(self, odds, stakes, profits, returns, refunds,
                 total_returns, outlays):
        self.odds = odds
        self.stakes = stakes
        self.profits = profits
        self.returns = returns
        self.refunds = refunds
        self.total_returns = total_returns
        self.outlays = outlays

    def __str__(self):
        results = ["Home", "Draw", "Away"]
        table = "Result \t Odds \t Stake \t Ret \t Ref \t TRet \t TOut \t Profit"
        for a in range(0, 3):
            table += "\n{0} \t {1} \t {2} \t {3} \t {4} \t {5} \t {6} \t {7}".format(
                results[a], self.odds[a], self.stakes[a], self.returns[a],
                self.refunds[a], self.total_returns[a], self.outlays[a],
                self.profits[a]
            )
        return table

    def get_in_play_bet(self):
        results = ["Home", "Draw", "Away"]
        return results[self.refunds.index(0)]

def get_difference(profit_list):
    sorted_list = sorted(profit_list, key=float)
    return (
        (sorted_list[2] - sorted_list[1])
        + (sorted_list[2] - sorted_list[0])
        + (sorted_list[1] - sorted_list[0])
    )

def get_refund(index, stake_list):
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
    elif index == 1:
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
    else:
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

def main():
    odds = map(float, sys.argv[1:])
    index = odds.index(max(odds))

    best_equal_bet = None
    best_equal_total_profit = 0

    best_home_win_profit = 0
    best_home_win_bet = None

    best_draw_profit = 0
    best_draw_bet = None

    best_away_win_profit = 0
    best_away_win_bet = None

    for a in range(10,110):
        for b in range(10,110):
            for c in range(10,110):
                stake = [a, b, c]
                returns = [stake[i] * odds[i] for i in range(len(stake))]
                refund = get_refund(index, stake)
                total_returns = [
                    returns[i] + refund[i] for i in range(len(refund))
                ]
                total_outlay = [sum(stake), sum(stake), sum(stake)]
                overall_profit = [
                    total_returns[i] - total_outlay[i] for i in range(
                        len(total_outlay)
                    )
                ]

                if sum(1 for n in overall_profit if n < 0) == 0:
                    # Best equal profit
                    if (get_difference(overall_profit) <= 3
                            and sum(overall_profit) > best_equal_total_profit):
                        best_equal_bet = MatchedBet(
                            odds,
                            stake,
                            overall_profit,
                            returns,
                            refund,
                            total_returns,
                            total_outlay,
                        )
                        best_equal_total_profit = sum(overall_profit)

                    # Home Win
                    if (overall_profit[0] > best_home_win_profit
                            and overall_profit[1] > 8
                                and overall_profit[2] > 8):
                        best_home_win_profit = overall_profit[0]
                        best_home_win_bet = MatchedBet(
                            odds,
                            stake,
                            overall_profit,
                            returns,
                            refund,
                            total_returns,
                            total_outlay,
                        )

                    # Draw
                    if (overall_profit[1] > best_draw_profit
                            and overall_profit[0] > 8
                                and overall_profit[2] > 8):
                        best_draw_profit = overall_profit[1]
                        best_draw_bet = MatchedBet(
                            odds,
                            stake,
                            overall_profit,
                            returns,
                            refund,
                            total_returns,
                            total_outlay,
                        )

                    # Away Win
                    if (overall_profit[2] > best_away_win_profit
                            and overall_profit[0] > 8
                                and overall_profit[1] > 8):
                        best_away_win_profit = overall_profit[2]
                        best_away_win_bet = MatchedBet(
                            odds,
                            stake,
                            overall_profit,
                            returns,
                            refund,
                            total_returns,
                            total_outlay,
                        )

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
