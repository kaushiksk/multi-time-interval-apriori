#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : interval.py
# Author            : Kaushik S Kalmady, Siddharth V
# Date              : 21.11.2018
# Last Modified Date: 21.11.2018
# Last Modified By  : Kaushik S Kalmady

from config import TIME_INTERVALS

def get_interval(timestamp):
	"""Returns interval corresponding to given timestamp"""
	timestamp = abs(timestamp)

	for interval in TIME_INTERVALS:
		if timestamp > interval[0] and timestamp <= interval[1]:
			return interval

def get_interval_index(interval):
	"""Returns the index of the interval according to the
	list of intervals"""

	for idx, reference in enumerate(TIME_INTERVALS):
		if interval[0] == reference[0] and interval[1] == reference[1]:
			return idx

	raise Exception("Interval does not exist")



def time2str(intervals):
	time2str_map = dict()
	for i, interval in enumerate(intervals):
		time2str_map[interval] = "t" + str(i)
	return time2str_map


def make_table(ti, show=False):
	"""Create time interval matrix"""
	table = [[[] for i in range(len(ti))] for j in range(len(ti))]

	table[0][0].append(ti[0])

	for i in range(len(ti)):
		for j in range(i + 1):
			l = ti[i][0] + ti[j][0] # lower bound
			r = ti[i][1] + ti[j][1] # upper bound

			for t in ti:
				low = t[0]
				high = t[1]

				if not (high <= l or low >= r):
					table[i][j].append(t)

	if show:
		for i in range(len(ti)):
			for j in range(len(ti)):
				for t in table[i][j]:
					print t,
				print '|',
				print '\t',
			print '\n'

	return table
