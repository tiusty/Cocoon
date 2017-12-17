from Unicorn.settings.Global_Config import price_question_weight


class PriceAlgorithm(object):

    def __init__(self):
        self._max_price = 0
        self._min_price = 0
        self._price_user_scale_factor = 1
        self._price_question_weight = price_question_weight
        super(PriceAlgorithm, self).__init__()

    @property
    def max_price(self):
        """
        Gets the max price in dollars
        :return: The max price in dollars
        """
        return self._max_price

    @max_price.setter
    def max_price(self, new_max_price):
        """
        Sets the max price in dollars
        :param new_max_price: The new max price in dollars
        """
        self._max_price = new_max_price

    @property
    def min_price(self):
        """
        Gets the min price in dollars
        :return: Min price in dollars
        """
        return self._min_price

    @min_price.setter
    def min_price(self, new_min_price):
        """
        Sets the min price in dollars
        :param new_min_price: The new min price in dollars
        """
        self._min_price = new_min_price

    @property
    def price_user_scale_factor(self):
        """
        Gets the price scale factor. (Aka, how much weight the price has)
        :return: An int that is the scale factor
        """
        return self._price_user_scale_factor

    @price_user_scale_factor.setter
    def price_user_scale_factor(self, new_price_scale_factor):
        """
        Sets the price scale factor
        :param new_price_scale_factor: The new scale factor as an int
        """
        self._price_user_scale_factor = new_price_scale_factor

    def compute_price_score(self, home_price):
        """
        Compute the score based off the price. A percent value of how fit the home is returned
        I.E, .67 or .47, etc will be returned. The scaling will be done in the parent class
        :param home_price: The price as an int for the home.
        :return: The percent fit the home is
        """
        home_price_normalized = home_price - self.min_price

        # If the normalized price is less than 0, then return 0 which has no effect
        # The price eliminator should have already marked the home as eliminated since home_price < min_price
        if home_price_normalized < 0:
            return 0

        home_range = self.max_price - self.min_price
        # If the home_range is less than 0, then something went wrong so
        # return 0 to have no effect on the score
        if home_range <= 0:
            return 0

        return 1 - (home_price_normalized / home_range)
