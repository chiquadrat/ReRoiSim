import unittest
from simulation_immo_kapitalanlage import renditerechner
from steuerberechnung import steuerberechnung_immo


class Steuertarif2026(unittest.TestCase):
    def test_basic_allowance(self):
        self.assertEqual(steuerberechnung_immo(12_348, False, 2026), 0)

    def test_tariff_at_50000_euros(self):
        self.assertEqual(steuerberechnung_immo(50_000, False, 2026), 10_548)

    def test_splitting_tariff(self):
        self.assertEqual(
            steuerberechnung_immo(100_000, True, 2026),
            2 * steuerberechnung_immo(50_000, False, 2026),
        )


class Renditeberechnung(unittest.TestCase):
    def test_renditeberechnung_szenario_1(self):
        ergebnis = renditerechner(steuerjahr=2023)
        self.assertEqual(int(ergebnis["verkaufspreis"][0]), 209177, "Should be 209177")
        self.assertEqual(
            round(ergebnis["eigenkapitalrendite"][0], 4), 0.0946, "Should be 9.46%"
        )
        self.assertEqual(
            round(ergebnis["objektrendite"][0], 4), 0.0489, "Should be 4.89%"
        )

    def test_renditeberechnung_szenario_2(self):
        ergebnis = renditerechner(alleinstehend=True, steuerjahr=2023)
        self.assertEqual(int(ergebnis["verkaufspreis"][0]), 209177, "Should be 209177")
        self.assertEqual(
            round(ergebnis["eigenkapitalrendite"][0], 4), 0.0915, "Should be 9.15%"
        )
        self.assertEqual(
            round(ergebnis["objektrendite"][0], 4), 0.047, "Should be 4.70%"
        )

    def test_renditeberechnung_szenario_3(self):
        ergebnis = renditerechner(
            afasatz_gebaeude=0.025, verkaufsfaktor=20, steuerjahr=2023
        )
        self.assertEqual(int(ergebnis["verkaufspreis"][0]), 167341, "Should be 167342")
        self.assertEqual(
            round(ergebnis["eigenkapitalrendite"][0], 4), 0.0883, "Should be 8.83%"
        )
        self.assertEqual(
            round(ergebnis["objektrendite"][0], 4), 0.0446, "Should be 4.46%"
        )


if __name__ == "__main__":
    unittest.main()
