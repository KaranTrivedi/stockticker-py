#!./venv/bin/python

"""

Docstring should be written for each file.
run `pylint filename.py` to find recommendations on improving format.

"""
import configparser
import json
import logging
from os import execlp
from time import sleep
from random  import randint
import names
import sys
import matplotlib.pyplot as plt

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read("conf/config.ini")
SECTION = "stockticker"

logger = logging.getLogger(SECTION)

STOCKS = [
    {
        "name": "grain",
        "color": "m",
        "values": [1]
    },
    {
        "name": "industrial",
        "color": "b",
        "values": [1]
    },
    {
        "name": "bonds",
        "color": "g",
        "values": [1]
    },
    {
        "name": "oil",
        "color": "k",
        "values": [1]
    },
    {
        "name": "silver",
        "color": "c",
        "values": [1]
    },
    {
        "name": "gold",
        "color": "y",
        "values": [1]
    }]

AMOUNTS = [5, 10, 20]
ROLL_TYPE = ["up", "down", "div"]

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


class Stock:
    """
    Create stock, manage values.
    """

    def __init__(self, name, value, values, color):
        self.name = name
        self.value = value
        self.values = values
        self.color = color

    def __str__(self):
        """
        stringify
        """
        return json.dumps(vars(self), indent=2)

    def get_name(self):
        """
        Return name of stock
        """

        return self.name

    def get_value(self):
        """
        Return value of stock
        """
        return self.value

    def get_values(self):
        """
        Return historic values of stock
        """

        return self.values

    def get_color(self):
        """
        Return color of stock line
        """

        return self.color

    def calculate_worth(self):
        pass

    def update_price(self, change, amount):
        """
        Change the stock value a random amount.
        """

        outcome = None

        if change == "up":
            self.value += amount/100
        elif change =="down":
            self.value -= amount/100
        else:
            if self.value >= 1:
                print(f"------{self.name} ${amount/100:.2f} Dividend!------")

        self.value = round(self.value, 2)

        if self.value >= 2:
            self.value = 1
            outcome = "split"
            print(f"------{self.name} Split!------")
            
        if self.value <= 0:
            self.value = 1
            outcome = "bust"
            print(f"------{self.name} Bust!------")

        # UNCOMMENT
        print(f"{self.name}:{self.value} {change} {amount/100:.2f}")

        return outcome

    def set_values(self):
        """
        Build array of historic values of stocks.        
        """

        self.values.append(self.value)

def randomize_order(player, stocks):
    """
    Decide wether AI wants to buy or sell and weather it wants to.
    """

    # Decide if AI wants to buy
    if [True, True, True, True, False][randint(0,4)] and player.get_coh() > 0:
        # if buy, set how many stocks to buy.
        for _ in range(randint(1, len(stocks))):
            # select stock to buy.
            stock = stocks[randint(0, len(stocks)-1)]
            if player.get_coh() > stock.get_value()*500:
                # Buy some amount.
                val = (randint(500, int(player.get_coh()/stock.get_value())))

                # Set amount to buy and round down to lower 500
                buy_count = 500*( val //500)
                player.buy_stock(stock, buy_count)

    # Decide if AI wants to sell
    if [True, False][randint(0,1)] and len(player.holdings.keys()):
        # if sell, set how many stocks to sell.
        for _ in range(randint(1, len(player.holdings.keys()))):
            index = randint(0,len(player.holdings.keys())-1)

            # Find randomly assigned stock
            stock = [_stock for _stock in stocks if _stock.get_name() == list(player.holdings.keys())[index]][0]
            sell_count = 500*(randint(1, list(player.holdings.values())[index]/500))
            player.sell_stock(stock, sell_count)

def show_stocks(stocks):
    """
    List stocks and prices.

    Args:
        stocks ([type]): [description]
    """

    print("**** Market outlook ****")

    for i in range(len(stocks)):
        print(f"{i}: {stocks[i].get_name()}@{stocks[i].get_value()}")

def show_available(player, stocks):
    """
    Shows max number of stocks to buy based on coh.

    Args:
        player ([type]): [description]
        stocks ([type]): [description]
    """
    for index in range(len(stocks)):
        print(f"{index}: MAX {500*( int(player.get_coh()/stocks[int(index)].get_value()) //500)} {stocks[index].get_name()} available @{stocks[int(index)].get_value()}")

def main():
    """
    Main function.
    """

    logging.basicConfig(filename=CONFIG[SECTION]["log"],
                    level=CONFIG[SECTION]["level"],
                    format="%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s",
                    datefmt="%Y-%m-%dT%H:%M:%S%z")


    # Intiate stonk with values.
    stocks = []
    players = []

    # player_counts = input("Enter number of Human and AI players (Example: 1, 5): ").split(",")
    player_counts = "1, 10".split(",")

    for _ in range(int(player_counts[1])):
        players.append(Player("AI_" + names.get_full_name(), 5000))

    for _ in range(int(player_counts[0])):
        # name = input("Input Human player name: ")
        name = "Karan Trivedi"
        players.append(Player(name, 5000))

    print(f"{int(player_counts[0]) + int(player_counts[1])} Players in game:")
    for player in players:
        print(player.get_name())

    for _stock in STOCKS:
        stocks.append(Stock(_stock["name"], 1, _stock["values"], _stock["color"]))

    turn_num = 0
    x = [0]
    action = 0

    print("########## Game starts ##########")
    while True:

        # ROLL/Update val.
        roll, value, stock = ROLL_TYPE[randint(0, 2)], AMOUNTS[randint(0,2)], stocks[randint(0, len(STOCKS)-1)]

        outcome = stock.update_price(roll, value)

        for _stock in stocks:
            _stock.set_values()

        # UPDATE PLAYER VALUES.
        for player in players:
            # only need to update coh if there is a dividend payout
            if roll == "div" and stock.get_value() >= 1:
                player.set_coh(stock, value)

            player.set_market_value(stocks)
            player.set_net_worth()
            # print(f"{player.get_name()}:${player.get_net_worth()}")

            player.split_bust(outcome, stock)

        turn_num += 1
        x.append(turn_num)

        plt.xlabel('Number of Turns')
        plt.ylabel('Stock value')
        plt.legend(["grain", "industrial", "bonds", "oil", "silver", "gold"])
        plt.title('Stock Value over time')
        plt.ylim(ymin = 0, ymax = 2)

        for _stock in stocks:
            plt.plot(x, _stock.get_values(), _stock.get_color())

        # plt.savefig('stock.png', dpi=1200)
        plt.savefig('data/stock.png')

        # Every 10 turns, players can purchase.
        if turn_num % 10 == 0:

            print("############# AI Players will take turns #####################")

            # Players make moves
            for i in range(int(player_counts[1])):
                randomize_order(players[i], stocks)

            print("############# Human Players will take turns #####################")

            for i in range(int(player_counts[0])):

                print(f"{players[int(player_counts[1]) + i].get_name()}'s turn.")
                player.show_coh()

                show_stocks(stocks)
                player.show_holdings(stocks)

                while True:
                    action = input("Select action: buy = b, sell s, finish = q, end game = gg, show standings: SS, show holdings: h, show market: m: ")
                    if action == "q" or action == "gg":
                        break

                    if action == "m":
                        show_stocks(stocks)

                    if action == "h":
                        player.show_holdings(stocks)

                    if action == "b":
                        show_stocks(stocks)
                        show_available(player, stocks)
                        stocks_to_buy = input("List stocks to purchase (Ex. 1 or 0, 3, 5): ")
                        if stocks_to_buy == "-1": continue
                        for i in stocks_to_buy.split(","):

                            # loop will reset if indec is out of range..
                            try:
                                if int(i) not in range(len(stocks)): continue
                            except:
                                continue

                            inp_str = f"How much of {stocks[int(i)].get_name()} to buy? MAX {500*( int(player.get_coh()/stocks[int(i)].get_value()) //500)} available @{stocks[int(i)].get_value()}: "
                            buy_count = input(inp_str)
                            buy_count = 500*( int(buy_count) //500)
                            if buy_count: player.buy_stock(stocks[int(i)], buy_count)
                            player.show_coh()

                    if action == "s":
                        player.show_holdings(stocks)

                        stocks_to_sell = input("List stocks to sell (Ex. 1 or 0, 3, 5): ")
                        if stocks_to_sell == "-1": continue

                        for index in stocks_to_sell.split(","):

                            stock = stocks[int(index)]
                            try:
                                inp_str = f"How much of {stock.get_name()} to sell? Available {player.get_holdings()[stock.get_name()]}: "
                                sell_count = int(input(inp_str))

                                # stock = [_stock for _stock in stocks if _stock.get_name() == list(player.holdings.keys())[int(i)]][0]

                                player.sell_stock(stock, sell_count)
                                player.show_coh()
                            except:
                                print(f"{stock.get_name()} not in holdings")

                    # if action == "SS":
                    #     tmp_players = sorted(players, key=lambda x: x.net_worth, reverse=True)
                    #     for player in tmp_players:
                    #         player.set_market_value(stocks)
                    #         player.set_net_worth()
                    #         player.show_net_worth()

        # if turn_num > 100 or action == "gg":
        if action == "gg":
            break

        # sleep(0.1)

    print("########## Game ended! ##########")

    # players[-1].show_holdings(stocks)
    # players[-1].show_coh()
    # players[-1].show_market_value()
    # players[-1].show_net_worth()

    players.sort(key=lambda x: x.net_worth, reverse=True)

    for player in players:

        player.set_market_value(stocks)
        player.set_net_worth()
        player.show_net_worth()



if __name__ == "__main__":
    main()
