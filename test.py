import unittest
from formeln import renditerechner

class TestSum(unittest.TestCase):

    def test_steuerberechnung_szenario_1(self):
        vk, ekren, objren = renditerechner()
        self.assertEqual(vk, 209177, "Should be 209177")
        self.assertEqual(ekren, 0.0943, "Should be 9.43%")
        self.assertEqual(objren, 0.0487, "Should be 4.87%")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 5, "Should be 6")

if __name__ == '__main__':
    unittest.main()