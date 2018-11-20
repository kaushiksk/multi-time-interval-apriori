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

   

    k1_copy = copy(k1)
    k1_copy.items = k1_copy.items[1:]
    k1_copy.intervals = k1_copy.intervals[1:]
    
    n = len(k1_copy.intervals)

    for i in len(n):
        k1_copy.intervals[i] = k1_copy.intervals[i][1:]

    k2_copy = copy(k2)
    k2_copy.items = k2_copy.items[:-1]
    k2_copy.intervals = k2_copy.intervals[:-1]

    if len(k1_copy.items) != len([i for i, j in zip(k1_copy.items, k2_copy.items) if i == j]):
        return False
  

    for i in len(n):
       for interval_1, interval_2 in zip(k1_copy.intervals[i], k2_copy.intervals[i]):
            if get_interval_index(interval_1) != get_interval_index(interval_2):
                return False

    return True


def joinCk(k1, k2):
    """ Joins two k-multi-time-interval sequences and returns a
    k+1-multi-time-interval sequence

    Arguments:
        k1: k-multi-time-interval
        k2: Another k-multi-time-interval
    """

    list_of_sequences = []

    if not joinable(k1, k2):
        return list_of_sequences

    items = []
    items.append(k1.items)
    items.append(k2.items[-1])

    intervals = []
    intervals.append(k1.intervals)
    intervals.append(k2.intervals[-1])

    T_1k = k1.intervals[-1][0]
    T_k1k = k2.intervals[-1][-1]

    i = get_interval_index(T_1k)
    j = get_interval_index(T_k1k)

    if i<j :
        i, j= j, i

    for interval in table[i][j]:
        if get_interval_index(interval) >= get_interval_index(intervals[-1][0]):
            t_intervals = copy(intervals)
            t_intervals[-1].insert(0, interval)

            s = Sequence(items, t_intervals)

            list_of_sequences.append(s)

    return list_of_sequences 


def joinC1(k1):
    """ Joins 1-multi-time-interval sequences with itself and returns a
    2-multi-time-interval sequence

    Arguments:
        k1: k-multi-time-interval
        k2: Another k-multi-time-interval
    """

    list_of_sequences = []

    for item_1 in k1.items :
        for item_2 in k1.items:
            t_items = [item_1, item_2]

            for interval in TIME_INTERVALS :
                t_intervals = [interval]

                s = Sequence(t_items, t_intervals)

                list_of_sequences.append(s)

    return list_of_sequences







