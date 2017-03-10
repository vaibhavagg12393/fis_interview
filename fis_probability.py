import random
from itertools import groupby
import numpy
import math
import operator
import pandas as pd

# Probability Solutions
# 1.) The expected number of groups after 10 tosses is 5.316580.
# 2.) The expected number of groups after 500 tosses is 240.577060.
# 3.) The probability of (strictly) exceeding 6 groups after 10 tosses is 0.226520.
# 4.) The probability of (strictly) exceeding 250 groups after 500 tosses is 0.196400.
# 5.) The probability of (strictly) exceeding 6 groups given we (strictly) exceeded 5 groups after 10 tosses is 0.502328.
# 6.) The probability of (strictly) exceeding 250 groups given we (strictly) exceeded 240 groups after 500 tosses is 0.391025.
# 7.) The probability of (strictly) exceeding 5 groups and (strictly) exceeding 5 heads after 10 tosses is 0.239930.
# 8.) The probability of (strictly) exceeding 100 groups and (strictly) exceeding 100 heads after 200 tosses is 0.292570.

my_list = ['H']*60 + ['T']*40

def probability(toss,lower_limit,upper_limit,head_count):
    total=0
    total_lower = 0
    total_upper = 0
    total_head = 0
    for j in xrange(100000):
        random.shuffle(my_list)
        arr_toss=[]
        for i in range(toss):
            arr_toss.append(random.choice(my_list))
        grouped_arr = [(k,sum(1 for m in g)) for k,g in groupby(arr_toss)]
        total += len(grouped_arr)
        if len(grouped_arr)>lower_limit:
            total_lower += 1
            if arr_toss.count('H') > head_count:
                total_head += 1
            if len(grouped_arr)>upper_limit:
                total_upper += 1
    return float(total)/(j+1), float(total_upper)/(j+1), float(total_upper)/total_lower, float(total_head)/(j+1)

probability_sol1, probability_sol3, probability_sol5, probability_sol7 = probability(10,5,6,5)
probability_sol2, probability_sol4, probability_sol6,temp = probability(500,240,250,501)
probability_sol8 = probability(200,100,201,100)[3]

print "Probability Solutions"
print "1.) The expected number of groups after 10 tosses is %f."%probability_sol1
print "2.) The expected number of groups after 500 tosses is %f."%probability_sol2
print "3.) The probability of (strictly) exceeding 6 groups after 10 tosses is %f."%probability_sol3
print "4.) The probability of (strictly) exceeding 250 groups after 500 tosses is %f."%probability_sol4
print "5.) The probability of (strictly) exceeding 6 groups given we (strictly) exceeded 5 groups after 10 tosses is %f."%probability_sol5
print "6.) The probability of (strictly) exceeding 250 groups given we (strictly) exceeded 240 groups after 500 tosses is %f."%probability_sol6
print "7.) The probability of (strictly) exceeding 5 groups and (strictly) exceeding 5 heads after 10 tosses is %f."%probability_sol7
print "8.) The probability of (strictly) exceeding 100 groups and (strictly) exceeding 100 heads after 200 tosses is %f."%probability_sol8