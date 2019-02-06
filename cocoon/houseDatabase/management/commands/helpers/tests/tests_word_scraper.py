from cocoon.houseDatabase.management.commands.helpers.word_scraper import WordScraper
from django.test import TestCase

class TestWordScraper(TestCase):

    def setUp(self):

        basic_test_1 = "laundry in unit, air conditioning available, dogs allowed, cats allowed, hardwood floors"
        basic_test_2 = "laundry in building, ac, dogs allowed, unfurnished, gym in building, balcony, hot tub"
        basic_test_3 = "laundromat nearby, a/c, cats allowed, furnished, storage unit"
        hard_test_1 = "laundromat near unit, no AC, dogs not allowed, fitness center, pool in leasing office"
        hard_test_2 = "no laundry in unit or building, air conditioning available, not furnished, no patio, no storage"
        hard_test_3 = "laundry in building, air conditioned unit, no hardwood floors, pool closed permanently"

        self.scraper1_easy = WordScraper(basic_test_1)
        self.scraper2_easy = WordScraper(basic_test_2)
        self.scraper3_easy = WordScraper(basic_test_3)

        self.scraper1_hard = WordScraper(hard_test_1)
        self.scraper2_hard = WordScraper(hard_test_2)
        self.scraper3_hard = WordScraper(hard_test_3)

    def test_word_laundry_in_unit(self):

        specific_test = "Wide-screen TV, wifi speaker, coffee maker, In-unit washer& dryer."
        specific_test2 = "Wide-screen TV, wifi speaker, coffee maker, In-unit w/d. "
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.look_for_laundry_in_unit():
            scraper_1_basic = True
        if self.scraper2_easy.look_for_laundry_in_unit():
            scraper_2_basic = True
        if self.scraper3_easy.look_for_laundry_in_unit():
            scraper_3_basic = True

        if self.scraper1_hard.look_for_laundry_in_unit():
            scraper1_hard = True
        if self.scraper2_hard.look_for_laundry_in_unit():
            scraper2_hard = True
        if self.scraper3_hard.look_for_laundry_in_unit():
            scraper3_hard = True

        self.assertTrue(WordScraper(specific_test).look_for_laundry_in_unit())
        self.assertTrue(WordScraper(specific_test2).look_for_laundry_in_unit())

        self.assertEqual(scraper_1_basic, True)
        self.assertEqual(scraper_2_basic, False)
        self.assertEqual(scraper_3_basic, False)

        self.assertEqual(scraper1_hard, False)
        self.assertEqual(scraper2_hard, True) # EDGE CASE
        self.assertEqual(scraper3_hard, False) # EDGE CASE

    def test_word_laundry_in_building(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.look_for_laundry_in_building():
            scraper_1_basic = True
        if self.scraper2_easy.look_for_laundry_in_building():
            scraper_2_basic = True
        if self.scraper3_easy.look_for_laundry_in_building():
            scraper_3_basic = True

        if self.scraper1_hard.look_for_laundry_in_building():
            scraper1_hard = True
        if self.scraper2_hard.look_for_laundry_in_building():
            scraper2_hard = True
        if self.scraper3_hard.look_for_laundry_in_building():
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, False)
        self.assertEqual(scraper_2_basic, True)
        self.assertEqual(scraper_3_basic, False)

        self.assertEqual(scraper1_hard, False)
        self.assertEqual(scraper2_hard, False)  # EDGE CASE
        self.assertEqual(scraper3_hard, True)

    def test_word_laundromat_nearby(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.word_finder(["laundromat","nearby"]):
            scraper_1_basic = True
        if self.scraper2_easy.word_finder(["laundromat","nearby"]):
            scraper_2_basic = True
        if self.scraper3_easy.word_finder(["laundromat","nearby"]):
            scraper_3_basic = True

        if self.scraper1_hard.word_finder(["laundromat","nearby"]):
            scraper1_hard = True
        if self.scraper2_hard.word_finder(["laundromat","nearby"]):
            scraper2_hard = True
        if self.scraper3_hard.word_finder(["laundromat","nearby"]):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, False)
        self.assertEqual(scraper_2_basic, False)
        self.assertEqual(scraper_3_basic, True)

        self.assertEqual(scraper1_hard, False) # EDGE CASE
        self.assertEqual(scraper2_hard, False)
        self.assertEqual(scraper3_hard, False)

    def test_word_air_conditioning(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.word_finder(["air","conditioning"])  \
                or self.scraper1_easy.word_finder(["ac"])\
                or self.scraper1_easy.word_finder(["a", "/", "c"]):
            scraper_1_basic = True
        if self.scraper2_easy.word_finder(["air","conditioning"]) \
                or self.scraper2_easy.word_finder(["ac"])\
                or self.scraper2_easy.word_finder(["a", "/", "c"]):
            scraper_2_basic = True
        if self.scraper3_easy.word_finder(["air","conditioning"])  \
                or self.scraper3_easy.word_finder(["ac"])\
                or self.scraper3_easy.word_finder(["a", "/", "c"]):
            scraper_3_basic = True

        if self.scraper1_hard.word_finder(["air","conditioning"]) \
            or self.scraper1_hard.word_finder(["ac"]) \
            or self.scraper1_hard.word_finder(["a", "/", "c"]):
            scraper1_hard = True
        if self.scraper2_hard.word_finder(["air","conditioning"])  \
                or self.scraper2_hard.word_finder(["ac"])\
                or self.scraper2_hard.word_finder(["a", "/", "c"]):
            scraper2_hard = True
        if self.scraper3_hard.word_finder(["air","conditioning"])  \
                or self.scraper3_hard.word_finder(["ac"])\
                or self.scraper3_hard.word_finder(["a", "/", "c"]):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, True)
        self.assertEqual(scraper_2_basic, True)
        self.assertEqual(scraper_3_basic, True)

        self.assertEqual(scraper1_hard, True) # EDGE CASE
        self.assertEqual(scraper2_hard, True)
        self.assertEqual(scraper3_hard, False) # EDGE CASE

    def test_word_dogs(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if (self.scraper1_easy.word_finder(["dogs","allowed"])):
            scraper_1_basic = True
        if (self.scraper2_easy.word_finder(["dogs","allowed"])):
            scraper_2_basic = True
        if (self.scraper3_easy.word_finder(["dogs","allowed"])):
            scraper_3_basic = True

        if (self.scraper1_hard.word_finder(["dogs","allowed"])):
            scraper1_hard = True
        if (self.scraper2_hard.word_finder(["dogs","allowed"])):
            scraper2_hard = True
        if (self.scraper3_hard.word_finder(["dogs","allowed"])):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, True)
        self.assertEqual(scraper_2_basic, True)
        self.assertEqual(scraper_3_basic, False)

        self.assertEqual(scraper1_hard, False) # EDGE CASE
        self.assertEqual(scraper2_hard, False)
        self.assertEqual(scraper3_hard, False)

    def test_word_cats(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if (self.scraper1_easy.word_finder(["cats","allowed"])):
            scraper_1_basic = True
        if (self.scraper2_easy.word_finder(["cats","allowed"])):
            scraper_2_basic = True
        if (self.scraper3_easy.word_finder(["cats","allowed"])):
            scraper_3_basic = True

        if (self.scraper1_hard.word_finder(["cats","allowed"])):
            scraper1_hard = True
        if (self.scraper2_hard.word_finder(["cats","allowed"])):
            scraper2_hard = True
        if (self.scraper3_hard.word_finder(["cats","allowed"])):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, True)
        self.assertEqual(scraper_2_basic, False)
        self.assertEqual(scraper_3_basic, True)

        self.assertEqual(scraper1_hard, False)
        self.assertEqual(scraper2_hard, False)
        self.assertEqual(scraper3_hard, False)

    def test_word_hardwood_floors(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.look_for_hardwood_floors():
            scraper_1_basic = True
        if self.scraper2_easy.look_for_hardwood_floors():
            scraper_2_basic = True
        if self.scraper3_easy.look_for_hardwood_floors():
            scraper_3_basic = True

        if self.scraper1_hard.look_for_hardwood_floors():
            scraper1_hard = True
        if self.scraper2_hard.look_for_hardwood_floors():
            scraper2_hard = True
        if self.scraper3_hard.look_for_hardwood_floors():
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, True)
        self.assertEqual(scraper_2_basic, False)
        self.assertEqual(scraper_3_basic, False)

        self.assertEqual(scraper1_hard, False)
        self.assertEqual(scraper2_hard, False)
        self.assertEqual(scraper3_hard, True) # EDGE CASE

    def test_word_furnished(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.word_finder(["furnished"]):
            scraper_1_basic = True
        if self.scraper2_easy.word_finder(["furnished"]):
            scraper_2_basic = True
        if self.scraper3_easy.word_finder(["furnished"]):
            scraper_3_basic = True

        if self.scraper1_hard.word_finder(["furnished"]):
            scraper1_hard = True
        if self.scraper2_hard.word_finder(["furnished"]):
            scraper2_hard = True
        if self.scraper3_hard.word_finder(["furnished"]):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, False)
        self.assertEqual(scraper_2_basic, False) # EDGE CASE
        self.assertEqual(scraper_3_basic, True)

        self.assertEqual(scraper1_hard, False)
        self.assertEqual(scraper2_hard, True) # EDGE CASE
        self.assertEqual(scraper3_hard, False)

    def test_word_gym(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.word_finder(["gym"]):
            scraper_1_basic = True
        if self.scraper2_easy.word_finder(["gym"]):
            scraper_2_basic = True
        if self.scraper3_easy.word_finder(["gym"]):
            scraper_3_basic = True

        if self.scraper1_hard.word_finder(["gym"]):
            scraper1_hard = True
        if self.scraper2_hard.word_finder(["gym"]):
            scraper2_hard = True
        if self.scraper3_hard.word_finder(["gym"]):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, False)
        self.assertEqual(scraper_2_basic, True)
        self.assertEqual(scraper_3_basic, False)

        self.assertEqual(scraper1_hard, False) # EDGE CASE
        self.assertEqual(scraper2_hard, False)
        self.assertEqual(scraper3_hard, False)

    def test_word_balcony_patio(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.word_finder(["balcony"]) or self.scraper1_easy.word_finder(["patio"]):
            scraper_1_basic = True
        if self.scraper2_easy.word_finder(["balcony"]) or self.scraper2_easy.word_finder(["patio"]):
            scraper_2_basic = True
        if self.scraper3_easy.word_finder(["balcony"]) or self.scraper3_easy.word_finder(["patio"]):
            scraper_3_basic = True

        if self.scraper1_hard.word_finder(["balcony"]) or self.scraper1_hard.word_finder(["patio"]):
            scraper1_hard = True
        if self.scraper2_hard.word_finder(["balcony"]) or self.scraper2_hard.word_finder(["patio"]):
            scraper2_hard = True
        if self.scraper3_hard.word_finder(["balcony"]) or self.scraper3_hard.word_finder(["patio"]):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, False)
        self.assertEqual(scraper_2_basic, True)
        self.assertEqual(scraper_3_basic, False)

        self.assertEqual(scraper1_hard, False)
        self.assertEqual(scraper2_hard, True) # EDGE CASE
        self.assertEqual(scraper3_hard, False)

    def test_word_pool_hot_tub(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.word_finder(["pool"]) or self.scraper1_easy.word_finder(["hot","tub"]):
            scraper_1_basic = True
        if self.scraper2_easy.word_finder(["pool"]) or self.scraper2_easy.word_finder(["hot","tub"]):
            scraper_2_basic = True
        if self.scraper3_easy.word_finder(["pool"]) or self.scraper3_easy.word_finder(["hot","tub"]):
            scraper_3_basic = True

        if self.scraper1_hard.word_finder(["pool"]) or self.scraper1_hard.word_finder(["hot","tub"]):
            scraper1_hard = True
        if self.scraper2_hard.word_finder(["pool"]) or self.scraper2_hard.word_finder(["hot","tub"]):
            scraper2_hard = True
        if self.scraper3_hard.word_finder(["pool"]) or self.scraper3_hard.word_finder(["hot","tub"]):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, False)
        self.assertEqual(scraper_2_basic, True)
        self.assertEqual(scraper_3_basic, False)

        self.assertEqual(scraper1_hard, True)
        self.assertEqual(scraper2_hard, False)
        self.assertEqual(scraper3_hard, True) # EDGE CASE

    def test_word_storage(self):
        scraper_1_basic = False
        scraper_2_basic = False
        scraper_3_basic = False

        scraper1_hard = False
        scraper2_hard = False
        scraper3_hard = False

        if self.scraper1_easy.word_finder(["storage"]):
            scraper_1_basic = True
        if self.scraper2_easy.word_finder(["storage"]):
            scraper_2_basic = True
        if self.scraper3_easy.word_finder(["storage"]):
            scraper_3_basic = True

        if self.scraper1_hard.word_finder(["storage"]):
            scraper1_hard = True
        if self.scraper2_hard.word_finder(["storage"]):
            scraper2_hard = True
        if self.scraper3_hard.word_finder(["storage"]):
            scraper3_hard = True

        self.assertEqual(scraper_1_basic, False)
        self.assertEqual(scraper_2_basic, False)
        self.assertEqual(scraper_3_basic, True)

        self.assertEqual(scraper1_hard, False)
        self.assertEqual(scraper2_hard, True) # EDGE CASE
        self.assertEqual(scraper3_hard, False)

