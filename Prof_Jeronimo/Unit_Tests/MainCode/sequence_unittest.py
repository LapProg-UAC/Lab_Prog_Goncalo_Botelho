import unittest
from sequence_main import sequence

class TestSequence(unittest.TestCase):
    
    def test_base_cases(self):
        """Tests the base cases defined in the mathematical formula."""
        self.assertEqual(sequence(0), [0])
        self.assertEqual(sequence(1), [0, 1])
        
    def test_general_cases(self):
        """Tests general valid cases."""
        self.assertEqual(sequence(2), [0, 1, 1])
        self.assertEqual(sequence(3), [0, 1, 1, 4])
        # Fixed the deliberate error (was 5, now correctly 4)
        self.assertEqual(sequence(5), [0, 1, 1, 4, 7, 19])

    def test_invalid_input(self):
        """Tests expected exceptions for invalid data types and negatives."""
        with self.assertRaises(ValueError):
            sequence(-1)
        with self.assertRaises(ValueError):
            sequence(-10)
        with self.assertRaises(ValueError):
            sequence('a')
        with self.assertRaises(ValueError):
            sequence(3.5)

if __name__ == '__main__':
    unittest.main()