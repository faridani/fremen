
# tests/test_core.py
import unittest
from fremen import Fremen

class TestFremen(unittest.TestCase):
    def setUp(self):
        self.fremen = Fremen()
    
    def test_greet(self):
        self.assertEqual(self.fremen.greet(), "Greetings from Fremen!")

if __name__ == '__main__':
    unittest.main()
