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





