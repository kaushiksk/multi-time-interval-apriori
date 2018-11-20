"""
Implements the multi time interval apriori algorithm
"""

TIME_INTERVALS = [(0,0), ( 0,3 ), ( 3,6 ), ( 6, 100 )]
INTERVAL_2_STR = time2str(TIME_INTERVALS)
MIN_SUP = 0.75
DB = None


class Sequence:
	"""A multi time interval sequence"""

	def __init__(self, items, intervals):
		self.items = items
		self.intervals = intervals
		self.length = len(items)

    def __eq__(self, other):
        """Equality operator overloading for Sequence class
        """

        return self.length == other.length and self.items == other.items
           and self.intervals == other.intervals



def get_interval(timestamp):
	"""Returns interval corresponding to given timestamp"""
	timestamp = min(100, abs(timestamp))

	for interval in TIME_INTERVALS:
		if timestamp > interval[0] and timestamp <= interval[1]:
			return interval

def get_interval_index(interval):
	"""Returns the index of the interval according to the
	list of intervals"""

	for idx, reference in enumerate(TIME_INTERVALS):
		if interval[0] == reference[0] and interval[1] == reference[1]:
			return idx

	return -1



def time2str(intervals=TIME_INTERVALS):
	time2str_map = dict()
	for i, interval in enumerate(TIME_INTERVALS):
		time2str_map[interval] = "t" + str(i)
	return time2str_map

def make_table(ti, show=False):
	"""Create time interval matrix"""
	table = [ [ [] for i in range(len(ti))] for j in range(len(ti))]

	table[0][0].append(ti[0])

	for i in range(len(ti)):
		for j in range(i+1):
			l = min((ti[i][0] + ti[j][0]), 100)
			r = min((ti[i][1] + ti[j][1]), 100)
			print "l = ", l , "r = ", r
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
				print 'break',
				print '\t',
			print '\n'

	return table


def one_item_support(item, db=DB):
	"""Returns support of item in DB
	This is equal to number of rows containing atleast one tuple with item
	divided by total number of rows"""

	item_in_rows = 0.0
	num_rows = len(db)

	for row in db:
		if len(filter(lambda x: x[0] == item, row)) > 0:
			item_in_rows += 1

	return item_in_rows/num_rows


def generate_one_itemsets(db=DB):
	"""Generates one itemsets from a database of data sequences containing
	(item, timestamp) tuples"""


	unique_items = set()

	for row in db:
		for item, timestamp in row:
			unique_items.add(item)

	one_itemsets = filter(lambda x: one_item_support(x) >= MIN_SUP, unique_items)

	return one_itemsets





