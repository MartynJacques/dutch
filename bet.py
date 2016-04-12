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

def print_table(odds,
                stake,
                returns,
                refund,
                total_returns,
                total_outlay,
                profit_list):
    results = ["Home", "Draw", "Away"]
    print "Result \t Odds \t Stake \t Ret \t Ref \t TRet \t TOut \t Profit"
    for a in range(0, 3):
        print "{0} \t {1} \t {2} \t {3} \t {4} \t {5} \t {6} \t {7}".format(results[a], odds[a], stake[a], returns[a], refund[a], total_returns[a], total_outlay[a], profit_list[a])


    # print "In play bet: {0}".format(map_to_result(in_play_index))

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

    best_equal_stake = []
    best_equal_profit = []
    best_equal_returns = []
    best_equal_refund = []
    best_equal_total_returns = []
    best_equal_total_outlay = []
    best_equal_total_profit = 0

    best_home_win_profit = 0
    best_home_win_stake = []
    best_home_win_profit_list = []
    best_home_win_returns = []
    best_home_win_refund = []
    best_home_win_total_returns = []
    best_home_win_total_outlay = []

    best_draw_profit = 0
    best_draw_stake = []
    best_draw_profit_list = []
    best_draw_returns = []
    best_draw_refund = []
    best_draw_total_returns = []
    best_draw_total_outlay = []

    best_away_win_profit = 0
    best_away_win_stake = []
    best_away_win_profit_list = []
    best_away_win_returns = []
    best_away_win_refund = []
    best_away_win_total_returns = []
    best_away_win_total_outlay = []

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
                    if difference <= 3 and sum(overall_profit) > best_equal_total_profit:
                        best_equal_stake = stake
                        best_equal_profit = overall_profit
                        best_equal_returns = returns
                        best_equal_refund = refund
                        best_equal_total_returns = total_returns
                        best_equal_total_outlay = total_outlay
                        best_equal_total_profit = sum(best_equal_profit)

                    # Home Win
                    if overall_profit[0] > best_home_win_profit and overall_profit[1] > 8 and overall_profit[2] > 8:
                        best_home_win_profit = overall_profit[0]
                        best_home_win_stake = stake
                        best_home_win_profit_list = overall_profit
                        best_home_win_returns = returns
                        best_home_win_refund = refund
                        best_home_win_total_returns = total_returns
                        best_home_win_total_outlay = total_outlay

                    # Draw
                    if overall_profit[1] > best_draw_profit and overall_profit[0] > 8 and overall_profit[2] > 8:
                        best_draw_profit = overall_profit[1]
                        best_draw_stake = stake
                        best_draw_profit_list = overall_profit
                        best_draw_returns = returns
                        best_draw_refund = refund
                        best_draw_total_returns = total_returns
                        best_draw_total_outlay = total_outlay

                    # Away Win
                    if overall_profit[2] > best_away_win_profit and overall_profit[0] > 8 and overall_profit[1] > 8:
                        best_away_win_profit = overall_profit[2]
                        best_away_win_stake = stake
                        best_away_win_profit_list = overall_profit
                        best_away_win_returns = returns
                        best_away_win_refund = refund
                        best_away_win_total_returns = total_returns
                        best_away_win_total_outlay = total_outlay

    print "\nBest equal profit"
    print_table(odds,
                best_equal_stake,
                best_equal_returns,
                best_equal_refund,
                best_equal_total_returns,
                best_equal_total_outlay,
                best_equal_profit)

    print "\nBest home win"
    print_table(odds,
                best_home_win_stake,
                best_home_win_returns,
                best_home_win_refund,
                best_home_win_total_returns,
                best_home_win_total_outlay,
                best_home_win_profit_list)

    print "\nBest draw"
    print_table(odds,
                best_draw_stake,
                best_draw_returns,
                best_draw_refund,
                best_draw_total_returns,
                best_draw_total_outlay,
                best_draw_profit_list)

    print "\nBest away win"
    print_table(odds,
                best_away_win_stake,
                best_away_win_returns,
                best_away_win_refund,
                best_away_win_total_returns,
                best_away_win_total_outlay,
                best_away_win_profit_list)


if __name__ == "__main__":
    main()
