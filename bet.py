import sys

def map_to_result(index):
    if index == 0:
        return "Home"
    elif index == 1:
        return "Draw"
    else:
        return "Away"

def get_difference(profit_list):
    sorted_list = sorted(profit_list, key=float)
    # print sorted_list
    a = sorted_list[2] - sorted_list[1]
    b = sorted_list[2] - sorted_list[0]
    c = sorted_list[1] - sorted_list[0]
    # print a + b + c
    return a + b + c

def not_negative(profit_list):
    if profit_list[0] < 0.0 or profit_list[1] < 0.0 or profit_list[2] < 0.0:
        return False
    return True

def get_refund(index, stake_list):
    if index == 0:
        min_of_two_pre_match = min(stake_list[1:])
        if min_of_two_pre_match > 50:
            min_of_two_pre_match = 50
        return [0, min_of_two_pre_match, min_of_two_pre_match]
    elif index == 1:
        min_of_two_pre_match = min([stake_list[0], stake_list[2]])
        if min_of_two_pre_match > 50:
            min_of_two_pre_match = 50
        return [min_of_two_pre_match, 0, min_of_two_pre_match]
    else:
        min_of_two_pre_match = min(stake_list[:1])
        if min_of_two_pre_match > 50:
            min_of_two_pre_match = 50
        return [min_of_two_pre_match, min_of_two_pre_match, 0]

def print_stake_and_profit(stakes, profits, in_play_index):
    results = ["Home", "Draw", "Away"]
    print "Result \t Stake \t Profit"
    for a in range(0, 3):
        print "{0} \t {1} \t {2}".format(results[a], stakes[a], profits[a])
    print "Total stake: \t {0}".format(sum(stakes))
    print "In play bet: {0}".format(map_to_result(in_play_index))

def main():
    odds = map(float, sys.argv[1:])
    index = odds.index(max(odds))

    best_profit = []
    best_stake = []
    best_total = 0

    best_home_win_profit = 0
    best_home_win_profits = []
    best_home_win_stake = []

    best_draw_profit = 0
    best_draw_profits = []
    best_draw_stake = []

    best_away_win_profit = 0
    best_away_win_profits = []
    best_away_win_stake = []

    for a in range(10,110):
        for b in range(10,110):
            for c in range(10,110):
                # print "Odds: {0}".format(odds)
                stake = [a, b, c]
                # print "Stake: {0}".format(stake)
                returns = [stake[i] * odds[i] for i in range(len(stake))]
                # print "Returns: {0}".format(returns)
                # print "Stake: {0}".format(stake)
                refund = get_refund(index, stake)

                # print "Refund: {0}".format(refund)
                total_returns = [returns[i] + refund[i] for i in range(len(refund))]
                # print "Total Returns: {0}".format(total_returns)
                total_outlay = [sum(stake), sum(stake), sum(stake)]
                # print "Total Outlay: {0}".format(total_outlay[0])
                overall_profit = [total_returns[i] - total_outlay[i] for i in range(len(total_outlay))]
                # print "Overall profit: {0}".format(overall_profit)

                if not_negative(overall_profit):
                    difference = get_difference(overall_profit)
                    if difference <= 3 and sum(overall_profit) > best_total:
                        # print "Even profits: {0} Total: {1}".format(overall_profit, sum(overall_profit))
                        # print "With Stakes: {0} Total {1}".format(stake, sum(stake))
                        best_profit = overall_profit
                        best_stake = stake
                        best_total = sum(best_profit)

                    # Home Win
                    if overall_profit[0] > best_home_win_profit and overall_profit[1] > 8 and overall_profit[2] > 8:
                        best_home_win_profit = overall_profit[0]
                        best_home_win_profits = overall_profit
                        best_home_win_stake = stake

                    # Draw
                    if overall_profit[1] > best_draw_profit and overall_profit[0] > 8 and overall_profit[2] > 8:
                        best_draw_profit = overall_profit[1]
                        best_draw_profits = overall_profit
                        best_draw_stake = stake

                    # Away Win
                    if overall_profit[2] > best_away_win_profit and overall_profit[0] > 8 and overall_profit[1] > 8:
                        best_away_win_profit = overall_profit[2]
                        best_away_win_profits = overall_profit
                        best_away_win_stake = stake

    print "\nBest equal profit"
    print_stake_and_profit(best_stake, best_profit, index)

    print "\nBest home win"
    print_stake_and_profit(best_home_win_stake, best_home_win_profits, index)

    print "\nBest draw"
    print_stake_and_profit(best_draw_stake, best_draw_profits, index)

    print "\nBest away win"
    print_stake_and_profit(best_away_win_stake, best_away_win_profits, index)


if __name__ == "__main__":
    main()
