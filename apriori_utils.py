#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : apriori_utils.py
# Author            : Kaushik S Kalmady
# Date              : 11.11.2018
# Last Modified Date: 19.11.2018
# Last Modified By  : Kaushik S Kalmady

from copy import copy


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

    for item_tuple, idx in item_tuples_with_idx:

        if not passes_validity(item_tuple, known_tuples, sequence):
            continue

        cur_known = known_tuples + item_tuple
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
    validity , i.e the time difference between item and each other item in
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
        if cur_interval != sequence.interval[cur_idx - 1][item_idx]:
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


def joinCk(k1, k2):
    """ Joins two k-multi-time-interval sequences and returns a
    k+1-multi-time-interval sequence

    Arguments:
        k1: k-multi-time-interval
        k2: Another k-multi-time-interval
    """


    if not joinable(k1, k2):
        return []

    list_of_sequences = []
    items = []
    items += k1.items
    items += k2.items[-1]

    intervals = []
    intervals += copy(k1.intervals)
    intervals += copy(k2.intervals[-1])

    T_1_kminus1 = k1.intervals[-1][0]
    T_kminus1_k = k2.intervals[-1][-1]

    i = get_interval_index(T_1_kminus1)
    j = get_interval_index(T_kminus1_k)

    if i < j: # Time interval matrix we construct is upper triangular
        i, j = j, i

    # Descending Property + Time Interval Matrix Property
    for interval in TIME_INTERVAL_MATRIX[i][j]:
        # T_1_k should be >= T_2_k
        if get_interval_index(interval) >= get_interval_index(intervals[-1][0]):
            t_intervals = copy(intervals)
            t_intervals[-1].insert(0, interval)

            list_of_sequences.append(Sequence(items, t_intervals))

    return list_of_sequences


def joinC2(one_itemsets):
    """ Joins 1-multi-time-interval sequences with itself and returns a
    2-multi-time-interval sequence

    Arguments:
        one_itemsets: frequent one itemsets from the DB
    """

    list_of_sequences = []

    for item_1 in one_itemsets:
        for item_2 in one_itemsets:
            t_items = [item_1, item_2]

            for interval in TIME_INTERVALS:
                t_intervals = [[interval]]
                list_of_sequences.append(Sequence(t_items, t_intervals))

    return list_of_sequences

