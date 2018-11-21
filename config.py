#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : config.py
# Author            : Kaushik S Kalmady
# Date              : 21.11.2018
# Last Modified Date: 21.11.2018
# Last Modified By  : Kaushik S Kalmady

# TIME_INTERVALS is list of (start, end) tuples 
# Here (start, end) => start < t <= end
TIME_INTERVALS = [(0, 0), (0, 3), (3, 6), (6, float('inf'))]

# Minimum support to be used in MI-APRIORI algorithm
MIN_SUP = 0.50

# DB should be a collection of transactions
# Each transaction is a (itemid, timestamp) tuple sorted in ascending order of 
# timestamp

DB = [
	 [('a', 1), ('b', 3), ('c', 3), ('a', 5), ('e', 5), ('c', 10)],
	 [('d', 5), ('a', 7), ('b', 7), ('e', 7), ('d', 8), ('e', 8), ('c', 14), ('d', 15)],
	 [('a', 8), ('b', 8), ('e', 11), ('d', 12), ('b', 13), ('c', 13), ('c', 16)],
	 [('b', 15), ('f', 15), ('e', 16), ('b', 17), ('c', 17)]
	 ]