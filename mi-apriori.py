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
from apriori_utils import support, one_item_support
from apriori_utils import run_apriori
from config import TIME_INTERVALS, MIN_SUP, DB

import sys

time_interval_matrix = make_table(TIME_INTERVALS)
one_itemsets = generate_one_itemsets(DB, MIN_SUP)


if __name__=="__main__":

	max_sequence_length = sys.argv[1]


	frequent_sequences = run_apriori(DB, TIME_INTERVALS, max_sequence_length, MIN_SUP)