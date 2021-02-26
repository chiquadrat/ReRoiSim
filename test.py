import unittest
from formeln import renditerechner


class Renditeberechnung(unittest.TestCase):
    def test_renditeberechnung_szenario_1(self):
        ergebnis = renditerechner()
        self.assertEqual(ergebnis["verkaufspreis"], 209177, "Should be 209177")
        self.assertEqual(ergebnis["eigenkapitalrendite"], 0.0943, "Should be 9.43%")
        self.assertEqual(ergebnis["objektrendite"], 0.0487, "Should be 4.87%")

    def test_renditeberechnung_szenario_2(self):
        ergebnis = renditerechner(alleinstehend=True,)
        self.assertEqual(ergebnis["verkaufspreis"], 209177, "Should be 209177")
        self.assertEqual(ergebnis["eigenkapitalrendite"], 0.091, "Should be 9.14%")
        self.assertEqual(ergebnis["objektrendite"], 0.0467, "Should be 4.67%")

    def test_renditeberechnung_szenario_3(self):
        ergebnis = renditerechner(baujahr=1918, verkaufsfaktor=20,)
        self.assertEqual(ergebnis["verkaufspreis"], 167341, "Should be 167342")
        self.assertEqual(ergebnis["eigenkapitalrendite"], 0.088, "Should be 8.85%")
        self.assertEqual(ergebnis["objektrendite"], 0.0444, "Should be 4.44%")


if __name__ == "__main__":
    unittest.main()
