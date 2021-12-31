#!./venv/bin/python

"""

Docstring should be written for each file.
run `pylint filename.py` to find recommendations on improving format.

"""
import configparser
import logging
from random import randint

import matplotlib.pyplot as plt
import names

from player import Player
from stock import Stock

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

    for index, stock in enumerate(stocks):
        print(f"{index}: {stock.get_name()}@{stock.get_value()}")

def show_available(player, stocks):
    """
    Shows max number of stocks to buy based on coh.

    Args:
        player ([type]): [description]
        stocks ([type]): [description]
    """

    for index, stock in enumerate(stocks):
        print(f"{index}: MAX {500*( int(player.get_coh()/stock.get_value()) //500)} {stock.get_name()} available @{stock.get_value()}")

def draw(x_axis, stocks):
    """
    Function to draw graph.

    Args:
        x ([type]): [description]
        stocks ([type]): [description]
    """

    plt.xlabel('Number of Turns')
    plt.ylabel('Stock value')

    legend_str = [f"{index}: {stock.get_name()}" for index, stock in enumerate(stocks)]

    plt.legend(legend_str)
    plt.title('Stock Value over time')
    plt.ylim(ymin = 0, ymax = 2)

    for _stock in stocks:
        plt.plot(x_axis, _stock.get_values(), _stock.get_color())

    # plt.savefig('stock.png', dpi=1200)
    plt.savefig('data/stock.png')

def player_turn(player, stocks):
    """
    Logic for human plauer turn.

    Args:
        player ([type]): [description]
        stocks ([type]): [description]
    """

    player.show_coh()

    show_stocks(stocks)
    player.show_holdings(stocks)

    while True:
        action = input("Select action: buy = b, sell s, finish = q, end game = gg, show standings: SS, show holdings: h, show market: m: ")
        if action in ("q", "gg"):
            break

        if action == "m":
            show_stocks(stocks)

        if action == "h":
            player.show_holdings(stocks)

        if action == "b":
            if player_buy(player, stocks) == -1:
                continue

        if action == "s":
            if player_sell(player, stocks) == -1:
                continue

        # if action == "SS":
        #     tmp_players = sorted(players, key=lambda x: x.net_worth, reverse=True)
        #     for player in tmp_players:
        #         player.set_market_value(stocks)
        #         player.set_net_worth()
        #         player.show_net_worth()

        player.set_market_value(stocks)

        return action

def player_buy(player, stocks):
    """
    Human player buy stock function

    Args:
        player ([type]): [description]
        stocks ([type]): [description]

    Returns:
        [type]: [description]
    """

    show_stocks(stocks)
    show_available(player, stocks)
    stocks_to_buy = input("List stocks to purchase (Ex. 1 or 0, 3, 5): ")
    if stocks_to_buy == "-1":
        return -1

    for i in stocks_to_buy.split(","):

        # loop will reset if index is out of range..
        try:
            if int(i) not in range(len(stocks)):
                continue
        except:
            continue

        inp_str = f"How much of {stocks[int(i)].get_name()} to buy? MAX {500*( int(player.get_coh()/stocks[int(i)].get_value()) //500)} available @{stocks[int(i)].get_value()}: "
        try:
            buy_count = input(inp_str)
        except:
            print("Bad input")
            return -1

        buy_count = 500*( int(buy_count) //500)

        if buy_count:
            player.buy_stock(stocks[int(i)], buy_count)

        player.show_coh()

        return 0

def player_sell(player, stocks):
    """
    Human player sell stocks function.

    Args:
        player ([type]): [description]
        stocks ([type]): [description]

    Returns:
        [type]: [description]
    """
    player.show_holdings(stocks)

    stocks_to_sell = input("List stocks to sell (Ex. 1 or 0, 3, 5): ")
    if stocks_to_sell == "-1":
        return -1

    for index in stocks_to_sell.split(","):

        try:
            stock = stocks[int(index)]
        except:
            print("bad index")
            return -1
        try:
            inp_str = f"How much of {stock.get_name()} to sell? Available {player.get_holdings()[stock.get_name()]}: "
            try:
                sell_count = int(input(inp_str))
            except:
                print("Bad input")
                return -1

            # stock = [_stock for _stock in stocks if _stock.get_name() == list(player.holdings.keys())[int(i)]][0]

            player.sell_stock(stock, sell_count)
            player.show_coh()
        except:
            print(f"{stock.get_name()} not in holdings")

        return 0

def game_loop(players, stocks, player_counts):
    """
    Main game loop.

    Args:
        players ([type]): [description]
        stocks ([type]): [description]
        player_counts ([type]): [description]
    """

    x_axis = [0]
    action = 0
    turn_num = 0

    print("########## Game starts ##########")
    while True:

        # ROLL/Update val.
        roll, value, stock = ROLL_TYPE[randint(0, 2)], AMOUNTS[randint(0,2)], stocks[randint(0, len(STOCKS)-1)]

        outcome = stock.update_price(roll, value)

        for _stock in stocks:
            _stock.set_values()

        # UPDATE PLAYER VALUES.
        for player in players:
            # Only need to update coh if there is a dividend payout
            if roll == "div" and stock.get_value() >= 1:
                player.set_coh(stock, value)

            player.set_market_value(stocks)
            player.set_net_worth()
            # print(f"{player.get_name()}:${player.get_net_worth()}")

            player.split_bust(outcome, stock)

        turn_num += 1
        x_axis.append(turn_num)

        # Every 10 turns, players can purchase.
        if turn_num % 10 == 0:

            draw(x_axis, stocks)

            print("############# AI Players will take turns #####################")

            # Players make moves
            for i in range(int(player_counts[1])):
                randomize_order(players[i], stocks)

            print("############# Human Players will take turns #####################")

            for i in range(int(player_counts[0])):
                print(f"{players[int(player_counts[1]) + i].get_name()}'s turn.")
                action = player_turn(players[int(player_counts[1]) + i], stocks)

        # if turn_num > 100 or action == "gg":
        if action == "gg":
            break
    return turn_num

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

    player_counts = input("Enter number of Human and AI players (Example: 1, 5): ").split(",")
    # player_counts = "1, 10".split(",")

    for _ in range(int(player_counts[1])):
        players.append(Player("AI_" + names.get_full_name(), 5000))

    for _ in range(int(player_counts[0])):
        name = input("Input Human player name: ")
        # name = "Karan Trivedi"
        players.append(Player(name, 5000))

    print(f"{int(player_counts[0]) + int(player_counts[1])} Players in game:")
    for player in players:
        print(player.get_name())

    for _stock in STOCKS:
        stocks.append(Stock(_stock["name"], 1, _stock["values"], _stock["color"]))

    turn_num = game_loop(players, stocks, player_counts)

    print("########## Game ended! ##########")
    print(f"Game lasted: {turn_num} Turns")

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
