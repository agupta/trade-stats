# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:54:55 2021

@author: anish
"""
from trade import SymbolStatsList, SymbolStats

import unittest


class TestTrade(unittest.TestCase):
    def test_example_output(self):
        """Test the included example."""
        example = [["57124702", "aaa", "13", "1136"],
                   ["57124702", "aac", "20", "477"],
                   ["57125641", "aab", "31", "907"],
                   ["57127350", "aab", "29", "724"],
                   ["57127783", "aac", "21", "638"],
                   ["57130489", "aaa", "18", "1222"],
                   ["57131654", "aaa", "9", "1077"],
                   ["57133453", "aab", "9", "756"]]
        expected = [["aaa", 5787, 40, 1161, 1222],
                    ["aab", 6103, 69, 810, 907],
                    ["aac", 3081, 41, 559, 638]]

        test_ss_list = SymbolStatsList()

        for trade in example:
            parsed_trade = SymbolStatsList.parse_trade(trade)
            test_ss_list.add_trade(*parsed_trade)

        result = [[symbol,
                   symbol_stats.max_time_gap,
                   symbol_stats.total_volume,
                   symbol_stats.weighted_average_price,
                   symbol_stats.max_trade_price]
                  for symbol, symbol_stats in test_ss_list.sort_ascending()]
        self.assertEqual(result, expected)

    def test_parse_trade(self):
        """Test parse trade"""
        data = ["24755830", "xyz", "100", "10000"]
        expected = (24755830, "xyz", 100, 10000)

        result = SymbolStatsList.parse_trade(data)

        self.assertEqual(result, expected)

    def test_ss_add_trade(self):
        """Test quite easily verifiable functionality."""
        ss = SymbolStats(0, 0, 0)
        ss.add_trade(10, 10, 10)
        ss.add_trade(13, 20, 20)
        ss.add_trade(16, 10, 10)
        self.assertEqual(ss.max_time_gap, 10)
        self.assertEqual(ss.total_volume, 40)
        self.assertEqual(ss.weighted_average_price, 15)
        self.assertEqual(ss.max_trade_price, 20)

    def test_ssl_add_trade(self):
        """Ensure duplicate symbols are not created."""
        ssl = SymbolStatsList()
        for _ in range(1000):
            ssl.add_trade(11820484, "abc", 44, 213)
            ssl.add_trade(13133342, "def", 22, 312)
            ssl.add_trade(25858422, "abc", 11, 312)
        self.assertEqual(len(ssl.symbol_stats), 2)


if __name__ == "__main__":
    unittest.main()
