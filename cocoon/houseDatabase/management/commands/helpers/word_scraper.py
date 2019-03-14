import re


class WordScraper:

    def __init__(self, input_description):
        self.input_description = input_description.lower()
        self.input_dictionary = self.make_input_dictionary()

    def make_input_dictionary(self):
        """
        Makes a dictionary using input description in lowercase, with "a/c" being replaced with "ac"
        self.input_dictionary : {"word" : [list of indicies of occurrence]}
        uses regex expression to find all words and punctuations
        """
        word_list = re.findall(r"[\w']+|[.,!?;&/]", self.input_description)
        word_dictionary = {}
        for i in range(len(word_list)):
            if word_list[i] in word_dictionary:
                word_dictionary[word_list[i]].append(i)
            else:
                word_dictionary[word_list[i]] = [i]

        return word_dictionary

    def word_finder(self, word_list):
        """
        word_list: (list of strings) input word

        Uses a list of words as input to find words in sequence using their index.
        Case1: if list_index == 0, means that the word could not be found in the input description (FALSE)
        Case2: if len(list_index)==1 and len(word_list) == 1, this means that there is only one word and it has been found (TRUE)
        Case3: all the words in the word_list are present in the input description, and there are more than one. Use the first
        word's indicies and check to see if each of the adjacent words match the index+1, +2, +3..... depending on the number
        of words in the input.
        """

        list_index = []
        for item in word_list:
            if item in self.input_dictionary:
                list_index.append(self.input_dictionary[item])

        if len(list_index) == 0:
            return False
        elif len(list_index) == 1 and len(word_list) == 1:
            return True
        elif len(list_index) == len(word_list) and len(list_index) > 1:
            first_word = list_index[0]

            for word_num in first_word:
                for j in range(1, len(word_list)):
                    if (word_num + j) not in list_index[j]:
                        return False
            return True
        else:
            return False

    def look_for_laundry_in_building(self):
        """
        Looks for laundry in building using multiple synonyms and abbreviations. Returns True if any one of the
        conditions match, returns False otherwise
        """
        if self.word_finder(["laundry", "in", "building"]):
            return True
        if self.word_finder(["laundry", "in", "bldg"]):
            return True
        if self.word_finder(["washer", "dryer", "in", "building"]):
            return True
        if self.word_finder(["washer", "and", "dryer", "in", "building"]):
            return True
        if self.word_finder(["w", "/", "d", "in", "building"]):
            return True
        if self.word_finder(["washer", "&", "dryer", "in", "building"]):
            return True
        if self.word_finder(["wd", "in", "building"]):
            return True
        if self.word_finder(["common", "laundry", "room"]):
            return True
        if self.word_finder(['common', 'laundry']):
            return True
        return False

    def look_for_laundry_in_unit(self):
        """
        Looks for laundry in unit using multiple synonyms and abbreviations. Returns True if any one of the
        conditions match, returns False otherwise
        """
        if self.word_finder(["laundry", "in", "unit"]):
            return True
        if self.word_finder(["in", "unit", "laundry"]):
            return True
        if self.word_finder(["washer", "dryer", "in", "unit"]):
            return True
        if self.word_finder(["in", "unit", "washer", "dryer"]):
            return True
        if self.word_finder(["washer", "and", "dryer", "in", "unit"]):
            return True
        if self.word_finder(["in", "unit", "washer", "and", "dryer"]):
            return True
        if self.word_finder(["w", "/", "d", "in", "unit"]):
            return True
        if self.word_finder(["in", "unit", "w", "/", "d"]):
            return True
        if self.word_finder(["in", "unit", "washer", "&", "dryer"]):
            return True
        if self.word_finder(["in", "unit", "wd"]):
            return True
        if self.word_finder(["personal", "washing", "machine", "and", "dryer"]):
            return True

        return False

    def look_for_hardwood_floors(self):
        """
        Looks for hardwood floors using multiple synonyms and abbreviations. Returns True if any one of the
        conditions match, returns False otherwise
        """

        if self.word_finder(["hardwood"]) \
            or self.word_finder(["hard", "wood"]) \
            or self.word_finder(["wooden", "floors"]) \
            or self.word_finder(["wood", "floors"]):
            return True

        return False

    def look_for_ac(self):
        if (self.word_finder(["air", "conditioning"])) \
                or self.word_finder(["ac"]) \
                or self.word_finder(["a", "/", "c"]):
            return True
        return False

