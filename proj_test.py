import unittest
from proj import *

# class TestDbResults(unittest.TestCase):
#
#     def test_db_search(self):
#         results = Veggie().process_restaurants('Chicago')
#         self.assertEqual(len(results), 264)
#         self.assertEqual(results[263][0], 'Snap Kitchen')
#
#         results = Veggie().process_fast_food_restaurants('Omaha')
#         self.assertNotEqual(len(results), 51)
#         self.assertNotEqual(results[11][0], 'Pizza Hut')
#
#         results = Veggie().process_fast_food_restaurants('New York')
#         self.assertEqual(len(results), 36)
#
#
# class TestIdApi(unittest.TestCase):
#
#     def test_id_search(self):
#         results = get_id_for_location('Whataburger', '670 Old San Antonio Rd Buda, TX, 78610')
#         self.assertEqual(results['Whataburger'], 'aOGMsboJELr1j1ueeM2P1g')
#
#         results = get_id_for_location('Boston Market', '3808 Secor Road Toledo, OH, 43606')
#         self.assertEqual(results['Boston Market'], 'SuHNbW8BczVa1K_PuxyTGw')
#
#         results = get_id_for_location('Taco Del Mar', '12311 Lake City Way N E Seattle, WA, 98125')
#         self.assertEqual(results['Taco Del Mar'], 'dUqwJJpaxDecIqufozeoJQ')
#
#         results = get_id_for_location('Blind Faith Cafe', '525 W Dempster St Evanston, IL, 60201')
#         self.assertEqual(results['Blind Faith Cafe'], 'tFipyFczXfQB_4m1ySD1NA')
#
#         results = get_id_for_location('Pita Jungle', '2530 W Happy Valley Rd Phoenix, AZ, 85085')
#         self.assertEqual(results['Pita Jungle'], 'cnfYugAYBFKgwDCTAVdViA')

class TestZipcodeResults(unittest.TestCase):

    def test_zipcode(self):
        results = Veggie().process_city_veg_chart('Evanston')
        self.assertEqual(results[0][0], '60201')

        results = Veggie().process_city_veg_chart('Baton Rouge')
        self.assertEqual(results[0][4], '70815')
        self.assertEqual(results[0][2], '70809')

        results = Veggie().process_fast_food_restaurants('Rawlins')
        self.assertEqual(results[2][4], 82301)

        results = Veggie().process_restaurants('Savannah')
        self.assertEqual(results[5][4], 31401)

        results = Veggie().process_fast_food_restaurants('Oak Park')
        self.assertEqual(results[1][4], 60302)

unittest.main()
