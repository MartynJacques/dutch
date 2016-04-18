class MatchedBet(object):
    """docstring for MatchedBet"""
    def __init__(self, stakes, profits, returns, refunds,
                 total_returns, outlays):
        self.stakes = stakes
        self.profits = profits
        self.returns = returns
        self.refunds = refunds
        self.total_returns = total_returns
        self.outlays = outlays

    def __str__(self):
        return "Test"
