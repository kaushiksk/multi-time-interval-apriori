#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : apriori_utils.py
# Author            : Kaushik S Kalmady, Siddharth V
# Date              : 11.11.2018
# Last Modified Date: 21.11.2018
# Last Modified By  : Kaushik S Kalmady

from copy import deepcopy as copy
import logging
from interval import get_interval, get_interval_index

logging.basicConfig(level=logging.DEBUG)

class multiTimeIntervalSequence:
    """A multi time interval sequence"""

    def __init__(self, items, intervals):
        self.items = items
        self.intervals = intervals
        self.length = len(items)

    def display(self):
        print(self.items)
        print(self.intervals)

    def __eq__(self, other):
        """Equality operator overloading for Sequence class
        """

        return self.length == other.length and self.items == other.items \
               and self.intervals == other.intervals


def one_item_support(item, db):
    """Returns support of item in DB
    This is equal to number of rows containing atleast one tuple with item
    divided by total number of rows"""

    item_in_rows = 0.0
    num_rows = len(db)

    for row in db:
        if len(filter(lambda x: x[0] == item, row)) > 0:
            item_in_rows += 1

    return item_in_rows/num_rows


def generate_one_itemsets(db, min_sup):
    """Generates one itemsets from a database of data sequences containing
    (item, timestamp) tuples"""


    unique_items = set()

    for row in db:
        for item, timestamp in row:
            unique_items.add(item)

    one_itemsets = filter(lambda x: one_item_support(x, db) >= min_sup, unique_items)

    return one_itemsets


def contains(transaction, sequence):
    """Returns True if sequence is contained in transaction as per multi-time
    interval sequence's "contains" definition.


    Arguments:
        transaction: A transaction from a sequence database containing
        (item, timestamp) tuples sorted according to timestamp
        sequence: A multi time interval sequence
    """

    # Creating copies so that things don't mess up during recursion
    # Python does pass by reference so doing this to be safe
    transaction_copy = copy(transaction)
    unknown_items = copy(sequence.items)
    known_tuples = []

    return recursive_contains(known_tuples, unknown_items,
                              transaction, sequence)


def recursive_contains(known_tuples, unknown_items, transaction, sequence):
    """recursive_contains

    Arguments:
        known_tuples:
        unknown_items:
        transaction:
        sequence:
    """

    if len(unknown_items) == 0:
        return True

    item_tuples_with_idx = find_tuples_with_item(unknown_items[0], transaction)

    # logging.debug("Item")
    # logging.debug(unknown_items[0])
    # logging.debug(item_tuples_with_idx)

    for item_tuple, idx in item_tuples_with_idx:

        if not passes_validity(item_tuple, known_tuples, sequence):
            continue

        cur_known = known_tuples + [item_tuple]
        if recursive_contains(cur_known, unknown_items[1:],
                              transaction[idx+1:], sequence):
            return True

    return False


def find_tuples_with_item(item, transaction):
    """find_tuples_with_item

    Arguments:
        item:
        transaction:
    """

    return [(item_tuple, idx)
            for idx, item_tuple in enumerate(transaction)
            if item_tuple[0] == item]


def passes_validity(item_tuple, known_tuples, sequence):
    """Returns True if item_tuple(item, timestamp) passes the time interval
    validity , i.e the time difference between item and each item in
    known_tuples should belong to the same interval as specified in
    sequence.intervals

    Arguments:
        item_tuple:
        known_tuples:
        sequence:
    """

    cur_item, cur_timestamp = item_tuple

    # Get index of current item in sequence. We need this to find it's
    # corresponding intervals
    cur_idx = sequence.items.index(cur_item)

    for item, timestamp in known_tuples:
        item_idx = sequence.items.index(item)
        cur_interval = get_interval(cur_timestamp - timestamp)

        if cur_interval != sequence.intervals[cur_idx - 1][item_idx]:
            return False

    return True


def joinable(k1, k2):
    """Returns True if the two k-multi-time-interval sequence are joinable into
    a k+1-multi-time-interval sequence

    Arguments:
        k1: k-multi-time-interval
        k2: Another k-multi-time-interval
    """

    if k1.length != k2.length:
        return False


    if k1.items[1:] != k2.items[:-1]:
        return False

    if k1.length == 2: # There wont be any time intervals here to check
        return True

    intervals_1 = []

    for intervals in k1.intervals[1:]:
        intervals_1.append(intervals[1:])

    intervals_2 = k2.intervals[:-1]

    if intervals_1 != intervals_2:
        return False

    return True


def joinCk(k1, k2, timeIntervalMatrix):
    """ Joins two k-multi-time-interval sequences and returns a
    k+1-multi-time-interval sequence

    Arguments:
        k1: k-multi-time-interval
        k2: Another k-multi-time-interval
        timeIntervalMatrix: Time interval matrix constructed using
        time intervals defined
    """

    list_of_sequences = []

    items = copy(k1.items)
    items.append(k2.items[-1])

    intervals = copy(k1.intervals)
    intervals.append(copy(k2.intervals[-1]))

    T_1_kminus1 = k1.intervals[-1][0]
    T_kminus1_k = k2.intervals[-1][-1]

    i = get_interval_index(T_1_kminus1)
    j = get_interval_index(T_kminus1_k)

    if i < j: # Time interval matrix we construct is upper triangular
        i, j = j, i

    # Descending Property + Time Interval Matrix Property
    for interval in timeIntervalMatrix[i][j]:
        # T_1_k should be >= T_2_k
        if get_interval_index(interval) >= get_interval_index(intervals[-1][0]):
            t_intervals = copy(intervals)
            t_intervals[-1].insert(0, interval)
            list_of_sequences.append(multiTimeIntervalSequence(items, t_intervals))

    return list_of_sequences


def joinC2(one_itemsets, time_intervals):
    """ Joins 1-multi-time-interval sequences with itself and returns a
    2-multi-time-interval sequence

    Arguments:
        one_itemsets: frequent one itemsets from the DB
        time_intervals: time intervals defined
    """

    list_of_sequences = []

    for item_1 in one_itemsets:
        for item_2 in one_itemsets:
            t_items = [item_1, item_2]

            for interval in time_intervals:
                t_intervals = [[interval]]
                list_of_sequences.append(multiTimeIntervalSequence(t_items, t_intervals))

    return list_of_sequences

if __name__=="__main__":
    print "Done"
