import unittest
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from Models.Monastery import Monastery

class TestMonasteryModel(unittest.TestCase):
    def test_monastery_constructor(self) -> None:
        m = Monastery(id = 1, name="Test", location="Nis", year_of_construction=1200)
        self.assertEqual(m.name, "Test")
        self.assertEqual(m.location, "Nis")
        self.assertEqual(m.year_of_construction, 1200)
    
if __name__ == '__main__':
    unittest.main()