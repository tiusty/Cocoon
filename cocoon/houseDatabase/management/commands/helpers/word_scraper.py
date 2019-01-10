class WordScraper:

    def __init__(self):
        self.input_description = ""

    def word_scraper(self, input_description):
        self.input_description = input_description.lower()

    def word_finder(self, word):

        if word in self.input_description:
            return True

        return False


