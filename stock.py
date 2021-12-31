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
