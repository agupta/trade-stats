# -*- coding: utf-8 -*-
"""
Created on Thu Aug 5 13:21:00 2021.

@author: anish
"""

import sys  # For custom input/output files.
import csv  # Bit overkill rn but might be worthwhile if adding functionality.
import logging


class SymbolStats:
    """
    Tracks stats for each symbol.

    Only keeps track of these stats for all trades so far:
        last_time_traded,
        max_time_gap,
        total_volume,
        max_trade_price,
        total_value_traded
    These are the minimal values needed to calculate the desired quantities of
    <MaxTimeGap>,<Volume>,<WeightedAveragePrice>,<MaxPrice> at the end.

    """

    def __init__(self, timestamp, quantity, price):
        self.last_time_traded = timestamp
        self.max_time_gap = 0

        self.total_volume = quantity  # TODO rename to volume?
        self.max_trade_price = price
        self.total_value_traded = quantity * price

    def add_trade(self, timestamp, quantity, price):
        """
        Process trade (update stats).

        Updates total_volume, max_time_gap, last_time_traded, max_trade_prce,
        total_value_traded.

        Parameters
        ----------
        timestamp : int
            Number of milliseconds after midnight.
        quantity : int
            Number of units traded.
        price : int
            Price traded at.

        Returns
        -------
        None.

        """
        self.total_volume += quantity

        time_gap = timestamp - self.last_time_traded
        self.max_time_gap = max(self.max_time_gap, time_gap)
        self.last_time_traded = timestamp

        self.max_trade_price = max(self.max_trade_price, price)
        self.total_value_traded += quantity * price

    @property
    def weighted_average_price(self):
        """
        Calculate the weighted average price and truncates to int.

        Formula: floor((Σ price * quantity)/(Σ quantity))

        """
        return int(self.total_value_traded / self.total_volume)


class SymbolStatsList:
    """
    Contains a SymbolStats for each distinct symbol.

    Effectively a wrapper for the dictionary with helper methods.

    """

    def __init__(self):
        self.symbol_stats = {}

    def add_trade(self, timestamp, symbol, quantity, price):
        """Add trade to the dictionary, calls SymbolStats.add_trade."""
        if symbol in self.symbol_stats:
            self.symbol_stats[symbol].add_trade(timestamp, quantity, price)
        else:
            self.symbol_stats[symbol] = SymbolStats(timestamp, quantity, price)

    @staticmethod
    def parse_trade(trade):
        """
        Convert strings in the input to ints where relevant.

        Parameters
        ----------
        trade : list [str,str,str,str]
            <TimeStamp>,<Symbol>,<Quantity>,<Price>

        Returns
        -------
        timestamp : int
        symbol : str
        quantity : int
        price : int

        """
        timestamp_string, symbol, quantity_string, price_string = trade
        timestamp = int(timestamp_string)
        quantity = int(quantity_string)
        price = int(price_string)
        return timestamp, symbol, quantity, price

    def sort_ascending(self):
        """Sort the symbols in ascending alphabetical order."""
        return sorted(self.symbol_stats.items())


if __name__ == "__main__":
    logging.info("trade.py begun executing...")

    symbol_stats_list = SymbolStatsList()

    # Optional custom input/output files
    if len(sys.argv) == 3:
        # custom file usage: python trade.py myinput.csv myoutput.csv
        logging.info(f"Custom input ({sys.argv[1]}) and output ({sys.argv[2]})"
                     f"filepaths provided.")
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        logging.info("No input and output filepaths provided, continuing with"
                     "defaults (input.csv, output.csv).")
        input_filename = "input.csv"
        output_filename = "output.csv"

    # newline="" is explained in https://docs.python.org/3/library/csv.html#id3
    logging.info("Attempting to open input file for reading.")
    with open(input_filename, newline="") as f:
        reader = csv.reader(f)
        lines_read = 0
        # For each trade (row) parse and process it
        for trade in reader:
            parsed_trade = SymbolStatsList.parse_trade(trade)
            symbol_stats_list.add_trade(*parsed_trade)
            lines_read += 1
        logging.info(f"Wrote {lines_read} lines.")

    logging.info("Attempting to open output file for writing")
    with open(output_filename, "w", newline="") as g:
        writer = csv.writer(g)
        lines_written = 0
        # Write a row for each line
        for symbol, symbol_stats in symbol_stats_list.sort_ascending():
            # Required format:
            # <symbol>,<MaxTimeGap>,<Volume>,<WeightedAveragePrice>,<MaxPrice>
            writer.writerow([symbol,
                             symbol_stats.max_time_gap,
                             symbol_stats.total_volume,
                             symbol_stats.weighted_average_price,
                             symbol_stats.max_trade_price])
            lines_written += 1
        logging.info(f"Wrote {lines_written} lines.")
