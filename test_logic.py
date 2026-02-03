import unittest
from logic import get_most_common_product

class TestLogic(unittest.TestCase):
    def test_get_most_common_product(self):
        # Scénario: Fournir une liste ["Pomme", "Poire", "Pomme"]
        products = ["Pomme", "Poire", "Pomme"]
        result = get_most_common_product(products)
        
        # Vérifier qu'elle retourne bien "Pomme"
        self.assertEqual(result, "Pomme")
        print("Test 'Top produit' réussi: ['Pomme', 'Poire', 'Pomme'] -> 'Pomme'")

    def test_get_most_common_product_case_insensitive(self):
        # Test supplémentaire pour la casse
        products = ["pomme", "Poire", "Pomme"]
        result = get_most_common_product(products)
        self.assertEqual(result, "Pomme")
        print("Test 'Top produit' (casse) réussi: ['pomme', 'Poire', 'Pomme'] -> 'Pomme'")

    def test_empty_list(self):
        result = get_most_common_product([])
        self.assertIsNone(result)
        print("Test 'Liste vide' réussi: [] -> None")

if __name__ == '__main__':
    unittest.main()
