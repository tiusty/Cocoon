import re

class WordScraper:

    def __init__(self, input_description):
        self.input_description = input_description.lower().replace("a/c","ac")
        self.input_dictionary = self.make_input_dictionary()

    def make_input_dictionary(self):
        word_list = re.findall(r"[\w']+|[.,!?;]", self.input_description)
        word_dictionary = {}
        for i in range(len(word_list)):
            if word_list[i] in word_dictionary:
                word_dictionary[word_list[i]].append(i)
            else:
                word_dictionary[word_list[i]] = [i]

        return word_dictionary

    def word_finder(self, word_list):

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







