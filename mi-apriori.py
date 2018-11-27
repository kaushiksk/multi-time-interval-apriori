#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : mi-apriori.py
# Author            : Kaushik S Kalmady, Siddharth V
# Date              : 21.11.2018
# Last Modified Date: 21.11.2018
# Last Modified By  : Kaushik S Kalmady

"""
Implements the multi time interval apriori algorithm
"""

from interval import make_table
from apriori_utils import joinC2, joinCk, contains, generate_one_itemsets
from config import TIME_INTERVALS, MIN_SUP, DB


#time_interval_matrix = make_table(TIME_INTERVALS)
#one_itemsets = generate_one_itemsets(DB, MIN_SUP)

class MultiTimeIntervalApriori:
    """Implements the Multi Time Interval Apriori Algorithm"""

    def __init__(self, db=DB, time_intervals=TIME_INTERVALS, min_sup=MIN_SUP):
        self.__db = db
        self.__time_intervals = time_intervals
        self.__time_interval_matrix = make_table(self.__time_intervals)
        self.__min_sup = min_sup
        self.__one_itemsets = generate_one_itemsets(self.__db, self.__min_sup)
        self.__itemsets = dict()

    def support(self, sequence):
        """Returns support of multiTimeIntervalSequence sequence in db
        This is equal to number of rows containing sequence
        divided by total number of rows"""
        item_in_rows = 0.0
        num_rows = len(self.__db)

        for row in self.__db:
            if contains(row, sequence):
                item_in_rows += 1

        return item_in_rows/num_rows

    def generateC2(self):
        two_multi_sequences = joinC2(self.__one_itemsets, self.__time_intervals)
        frequent_two_sequences = filter(lambda x: self.support(x) >= self.__min_sup,
                                        two_multi_sequences)
        self.__itemsets[2] = frequent_two_sequences


    def run(k=4):
        print "Generating frequent 2-multi-time-iterval-sequences"

