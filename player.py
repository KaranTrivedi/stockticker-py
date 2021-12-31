class Player:
    """
    Create sample class
    """

    def __init__(self, name, coh):
        self.name = name
        self.market_value = 0
        self.market_value_ot = [0]

        self.coh = coh
        self.coh_ot = [coh]

        self.net_worth = coh
        self.net_worth_ot = [coh]

        self.holdings = {}

    def __str__(self):
        """
        stringify
        """
        return json.dumps(vars(self), indent=2)

    def calculate_worth(self):
        pass

    def buy_stock(self, stock, buy_count):
        """
        Buy stock for player.
        update coh, networth

        Args:
            stock ([type]): [description]
            buy_count ([type]): [description]
        """

        print(f"{self.name} bought {buy_count} of {stock.get_name()}")
        self.coh -= stock.get_value()*buy_count

        if stock.get_name() in self.holdings.keys():
            self.holdings[stock.get_name()] += buy_count
        else:
            self.holdings[stock.get_name()] = buy_count

    def sell_stock(self, stock, sell_count):
        """
        Sell given stock from holdings. Function does nothing if stock not in holdings!

        Args:
            stock ([type]): [description]
            stock_val ([type]): [description]
            buy_count ([type]): [description]
        """

        try:
            self.holdings[stock.get_name()] -= sell_count
            self.coh += stock.get_value()*sell_count

            if self.holdings[stock.get_name()] == 0:
                del self.holdings[stock.get_name()]

            print(f"{self.name} sold {sell_count} of {stock.get_name()}")

        except:
            pass

    def split_bust(self, outcome, stock):
        """
        Split and bust behaviour for updating player holdings.

        Args:
            outcome ([type]): [description]
            stock ([type]): [description]
        """

        if outcome == "bust":
            try:
                del self.holdings[stock.get_name()]
            except:
                pass
        if outcome == "split":
            try:
                self.holdings[stock.get_name()] *= 2
            except:
                pass

    def get_name(self):
        """
        Return name of stock
        """

        return self.name

    def get_net_worth(self):
        """
        Returns networth of player
        """

        return self.coh + self.market_value

    def show_net_worth(self):
        """
        Returns networth of player
        """

        print(f"{self.name}'s net worth is: {self.coh + self.market_value}")

    def get_coh(self):
        """
        

        Returns:
            [type]: [description]
        """
        return self.coh

    def show_coh(self):
        """
        

        Returns:
            [type]: [description]
        """

        print(f"{self.name} has ${self.coh} on hand")

    def get_holdings(self):
        """
        
        """

        return self.holdings

    def get_market_value(self):
        """

        Returns:
            [type]: [description]
        """

        return self.market_value

    def show_market_value(self):
        """

        """
        print(f"{self.name} market value is: {self.market_value}")

    def show_holdings(self, stocks):
        """
        
        """

        print(f"{self.name} Holdings:\n-------------------------------")

        for index in range(len(stocks)):
            try:
                print(f"{index}: {stocks[index].get_name()}: {self.holdings[stocks[index].get_name()]}, worth ${self.holdings[stocks[index].get_name()]*stocks[index].get_value()}")
            except:
                print(f"{index}: {stocks[index].get_name()}: 0, worth $0")

        self.show_coh()
        self.show_net_worth()

    def set_coh(self, stock, val):
        """
        Calculate cash on hand based on existing currenct and dividends.

        Args:
            stocks ([type]): [description]
            outcome ([type]): [description]
            stock ([type]): [description]
        """

        if stock.get_name() in self.holdings.keys():
            self.coh += val*self.holdings[stock.get_name()]/100

    def set_market_value(self, stocks):
        """
        Based on holdings, calculate market value.

        Args:
            stocks ([type]): [description]
        """

        self.market_value = 0

        for key, val in self.holdings.items():
            self.market_value += [stock.value for stock in stocks if stock.name == key][0]*val

    def set_net_worth(self):
        """
        Calculates networth of player
        """

        self.net_worth = self.coh + self.market_value
