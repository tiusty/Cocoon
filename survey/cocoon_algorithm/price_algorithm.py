from Unicorn.settings.Global_Config import price_question_weight


class PriceAlgorithm(object):
    """
    Class computes the score based on the price of a home.
    This class is meant to be used as a child class for an algorithm class
    """
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
        Gets the price scale factor that the user set. (Aka, how much weight the price has)
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

    @property
    def price_question_weight(self):
        """
        Get the price_question weight that is determined by the config file
        :return: THe price quesiton weight as an int
        """
        return self._price_question_weight

    @price_question_weight.setter
    def price_question_weight(self, new_price_question_weight):
        """
        This Function might get deprecated because it shouldn't be changed
        from the config files value
        :param new_price_question_weight:
        :return:
        """
        #TODO determine if this function should not be allowed to be called
        self._price_question_weight = new_price_question_weight

    def compute_price_score(self, home_price):
        """
        Compute the score based off the price. A percent value of the fit of the home is returned
        I.E, .67 or .47, etc will be returned. The scaling will be done in the parent class
        :param home_price: The price as an int for the home.
        :return: The percent fit the home is or -1 if the home should be eliminated
        """
        if home_price < self.min_price:
            return -1
        elif home_price > self.max_price:
            return -1
        else:
            home_price_normalized = home_price - self.min_price
            home_range = self.max_price - self.min_price

            if home_range <= 0:
                # If the home_range is zero and the max_price equals the home
                # price then the home is in the range
                if home_price == self.min_price:
                    return 1
                else:
                    return -1

            return 1 - (home_price_normalized / home_range)
