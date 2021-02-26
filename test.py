import unittest
from formeln import renditerechner


class Renditeberechnung(unittest.TestCase):
    def test_renditeberechnung_szenario_1(self):
        vk, ekren, objren = renditerechner()
        self.assertEqual(vk, 209177, "Should be 209177")
        self.assertEqual(ekren, 0.0943, "Should be 9.43%")
        self.assertEqual(objren, 0.0487, "Should be 4.87%")

    def test_renditeberechnung_szenario_2(self):
        vk, ekren, objren = renditerechner(alleinstehend=True,)
        self.assertEqual(vk, 209177, "Should be 209177")
        self.assertEqual(ekren, 0.091, "Should be 9.14%")
        self.assertEqual(objren, 0.0467, "Should be 4.67%")

    def test_renditeberechnung_szenario_3(self):
        vk, ekren, objren = renditerechner(baujahr=1918, verkaufsfaktor=20,)
        self.assertEqual(vk, 167341, "Should be 167342")
        self.assertEqual(ekren, 0.088, "Should be 8.85%")
        self.assertEqual(objren, 0.0444, "Should be 4.44%")


if __name__ == "__main__":
    unittest.main()
