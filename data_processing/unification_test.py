import time
from statistics import mean
from multiprocessing import cpu_count

import pyximport; pyximport.install()
from unification import *

'''
def mean_test():
    import unification_old
    new = []
    old = []
    i = 0
    while i < 100:
        t = time.process_time()
        s1 = tuple(unification.test1())
        s2 = tuple(unification.test2())
        t2 = time.process_time() - t
        new.append(t2)
        i += 1
    i = 0
    while i < 100:
        t = time.process_time()
        s1 = tuple(unification_old.test1())
        s2 = tuple(unification_old.test2())
        t2 = time.process_time() - t
        old.append(t2)
        i += 1

    mean_new = mean(new) / 24
    mean_old = mean(old) / 24
    
    print('CPython + regexp: ' + str(mean_old))
    est = (108170 * 9773 * mean_old) / cpu_count()
    print('Estimated long loop time: %.2f s = %.2f m = %.2f h' % (est, est / 60, est / 3600))
    print()
    print('Cython + while: ' + str(mean_new))
    est = (108170 * 9773 * mean_new * 0.25) / cpu_count()
    print('Estimated long loop time: %.2f s = %.2f m = %.2f h' % (est, est / 60, est / 3600))

#mean_test()
#short_test()
'''
