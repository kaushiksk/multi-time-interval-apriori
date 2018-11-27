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
from apriori_utils import joinable, joinC2, joinCk
from apriori_utils import contains, generate_one_itemsets
from config import TIME_INTERVALS, MIN_SUP, DB
from __future__ import print_function
import sys

#time_interval_matrix = make_table(TIME_INTERVALS)
#one_itemsets = generate_one_itemsets(DB, MIN_SUP)

class MultiTimeIntervalApriori:
    """Implements the Multi Time Interval Apriori Algorithm
    multi-time-interval-sequences will be referred to as MTIS in comments"""

    def __init__(self, db=DB, timeIntervals=TIME_INTERVALS, min_sup=MIN_SUP):
        self.__db = db
        self.__timeIntervals = timeIntervals
        self.__timeIntervalMatrix = make_table(self.__timeIntervals)
        self.__min_sup = min_sup
        self.__oneItemsets = generate_one_itemsets(self.__db, self.__min_sup)
        self.__frequentSequences = dict()

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

    def run_apriori(max_sequence_length=4):
        """Stub function to run the apriori algorithm.

        Arguments:
            max_sequence_length: Maximum multiTimeIntervalSequence length
        """

        print("Generating frequent 2-MTIS")
        self.__generateC2()

        for k in range(3, max_sequence_length+1):
            print("Generating {0}-MTIS".format(k))
            # Get all Ck-1 MTIS
            kminus1_sequences = self.__frequentSequences[k-1]
            current_ksequence_list = []

            # Check if two Ck-1 MTIS are joinable and join
            for sequence_1 in kminus1_sequences:
                for sequence_2 in kminus1_sequences:
                    if joinable(sequence_1, sequence_2):
                        new_k_sequence = joinCk(sequence_1, sequence_2,
                                                self.__timeIntervalMatrix)
                        current_ksequence_list.append(new_k_sequence)

            # Choose only frequent Ck MTIS
            current_ksequence_list = filter(lambda x: self.support(x) >= self.__min_sup,
                                           current_ksequence_list)

            # Prune
            current_ksequence_list = self.prune(current_ksequence_list)

            self.__frequentSequences[k] = current_ksequence_list

    def generateC2(self):
        two_multi_sequences = joinC2(self.__one_itemsets, self.__timeIntervals)
        frequent_two_sequences = filter(lambda x: self.support(x) >= self.__min_sup,
                                        two_multi_sequences)
        self.__frequentSequences[2] = frequent_two_sequences

    def prune(self):
        pass
if __name__=="__main__":

	max_sequence_length = sys.argv[1]


	frequent_sequences = run_apriori(DB, TIME_INTERVALS, max_sequence_length, MIN_SUP)
