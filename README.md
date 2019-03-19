# multi-time-interval-apriori

This is a pure python implementation of MI-Apriori Algorithm as described in "On mining multi-time-interval sequential patterns" by Ya-Han Hu et. al.[[Paper Link](https://doi.org/10.1016/j.datak.2009.05.003)]

This was implemented as part of the Data Warehousing and Data Mining course during the 7th semester at NITK Surathkal.

As of this writing it is the only known public implementation of the algorithm.

# Running Examples
` $ python mi-apriori.py --example 1 --minsup 0.5`

You can change the example value to 1, 2, 3 and minsup to value between 0 and 1. Execute `$ python mi-apriori.py -h` for help.

# Usage
```python
from config import DB, TIME_INTERVALS # default db and intervals, you can change these
from mi-apriori import MultiTimeIntervalApriori

m = MultiTimeIntervalApriori(db=DB, timeIntervals=TIME_INTERVALS, min_sup=MIN_SUP)
m.run_apriori(max_sequence_length=6, verbose=True)
```

## Authors
    - Kaushik S Kalmady (@kaushiksk)
    - Siddharth V (@siddharthvdn)


