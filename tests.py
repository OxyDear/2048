import unittest
from funcs import get_number, zero_in_mas


class Test_2048(unittest.TestCase):

    def test_1(self):
        self.assertEqual(get_number(1, 2), 7)

    def test_2(self):
        self.assertEqual(get_number(3, 2), 15)

    def test_3(self):
        mas = [[1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1],
                ]

    def test_4(self):
        mas = [[1, 1, 1, 1],
               [1, 0, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1],
               ]

        self.assertEqual(zero_in_mas(mas), True)