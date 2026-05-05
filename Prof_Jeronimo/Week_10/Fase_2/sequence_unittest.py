import unittest
from sequence_doctest import sequence

class TestSequence(unittest.TestCase):
    def test_base_cases(self):
        self.assertEqual(sequence(0), [0])
        self.assertEqual(sequence(1), [0, 1])
        
    def test_general_cases(self):
        self.assertEqual(sequence(2), [0, 1, 1])
        self.assertEqual(sequence(3), [0, 1, 1, 4])
        self.assertEqual(sequence(5), [0, 1, 1, 5, 7, 19])

    def test_invalid_input(self):
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