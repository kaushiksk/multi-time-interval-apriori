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
from __future__ import print_function
import sys
import logging
from copy import deepcopy as copy

from interval import make_table
from apriori_utils import joinable, joinC2, joinCk
from apriori_utils import contains, generate_one_itemsets
from config import TIME_INTERVALS, MIN_SUP, DB

#time_interval_matrix = make_table(TIME_INTERVALS)
#one_itemsets = generate_one_itemsets(DB, MIN_SUP)
logging.basicConfig(level=logging.DEBUG)

def show(sequences):
    for seq in sequences:
        seq.display()

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

    def getFrequentSequences(self, k=None):
        if k is None:
            return self.__frequentSequences
        return self.__frequentSequences[k]

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

    def run_apriori(self, max_sequence_length=4, verbose=False):
        """Stub function to run the apriori algorithm.

        Arguments:
            max_sequence_length: Maximum multiTimeIntervalSequence length
        """

        print("Generating frequent 2-MTIS")
        self.generateC2(verbose=verbose)

        for k in range(3, max_sequence_length + 1):
            print("Generating {0}-MTIS".format(k))
            # Get all Ck-1 MTIS
            kminus1_sequences = self.__frequentSequences[k-1]
            current_ksequence_list = []

            # Check if two Ck-1 MTIS are joinable and join
            for sequence_1 in kminus1_sequences:
                for sequence_2 in kminus1_sequences:
                    if joinable(sequence_1, sequence_2):
                        # This can generate multiple Ck sequences
                        new_k_sequences = joinCk(sequence_1, sequence_2,
                                                self.__timeIntervalMatrix)
                        current_ksequence_list += new_k_sequences

            logging.debug("Sequences Generated : {0}".format(len(current_ksequence_list)))

            # Choose only frequent Ck MTIS
            current_ksequence_list = [sequence 
                                      for sequence in current_ksequence_list
                                      if self.support(sequence) >= self.__min_sup]

            logging.debug("Frequent Sequences Generated : {0}".format(len(current_ksequence_list)))

            # Prune
            current_ksequence_list = self.prune(current_ksequence_list, k)
            logging.debug("Pruned Sequences Generated : {0}".format(len(current_ksequence_list)))

            self.__frequentSequences[k] = current_ksequence_list

            if verbose:
                show(current_ksequence_list)

    def generateC2(self, verbose=False):
        two_multi_sequences = joinC2(self.__oneItemsets, self.__timeIntervals)
        frequent_two_sequences = [sequence 
                                  for sequence in two_multi_sequences
                                  if self.support(sequence) >= self.__min_sup]

        self.__frequentSequences[2] = frequent_two_sequences
        if verbose:
            show(frequent_two_sequences)

    def prune(self, sequence_list, k):
        """ Returns the pruned list of (k)multiTimeIntervalSequence

        Arguments:
            sequence_list: List of (k)multiTimeIntervalSequence
        """

        def gen_sub_sequences(sequence):
            """ Returns the list of all (k-1)sub_sequence of the give (k)multiTimeIntervalSequence 
            
            Arguments:
                sequence: (k)multiTimeIntervalSequence
            """
            subsequences = []

            for i in range(sequence.length):
                t_items = copy(sequence.items)
                t_intervals = copy(sequence.intervals)

                del t_items[i]

                if i != 0 and i != sequence.length-1:
                    del t_intervals[i-1]

                    for j in range(i-1, len(t_intervals)):
                        del t_intervals[j][i]


                elif i == sequence.length-1:
                    del t_intervals[i-1]

                elif i == 0:
                    del t_intervals[0]

                    for j in range(i, len(t_intervals)):
                        del t_intervals[j][i]
                    

                t_sequence = multiTimeIntervalSequence(t_items, t_intervals)
                subsequences.append(t_sequence)

            return subsequences

        def checkAllSubsequencesExist(sequence, k):
            sub_sequences = gen_sub_sequences(sequence)
            for sub_sequence in sub_sequences:
                if sub_sequence not in self.__frequentSequences[k-1]:
                    return False
            return True

        return [sequence
                for sequence in sequence_list
                if checkAllSubsequencesExist(sequence, k)]



if __name__=="__main__":

    from apriori_utils import multiTimeIntervalSequence
    
    m = MultiTimeIntervalApriori()

    def t(idx):
        return TIME_INTERVALS[idx]

    
    m.run_apriori(max_sequence_length=4, verbose=True)

    


    print("Example 1")
    I1 = ['b', 'e', 'c']
    T1 = [[t(1)], [t(3), t(2)]]
    print(T1)
    seq1 = multiTimeIntervalSequence(I1, T1)
    print("Support for Example 1 : {0}".format(m.support(seq1)))

    print("Example 2")
    I1 = ['a', 'c']
    T1 = [[t(2)]]
    seq1 = multiTimeIntervalSequence(I1, T1)
    print("Support for Example 1 : {0}".format(m.support(seq1)))
    """
    I1 = ['b', 'e', 'c']
    T1 = [[t(1)], [t(3), t(2)]]
    #print(T1)
    seq1 = multiTimeIntervalSequence(I1, T1)
    print(contains(DB[0], seq1))
    """
