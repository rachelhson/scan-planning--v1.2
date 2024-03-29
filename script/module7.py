"""score object & analysis- evaluate how many points can be observed from psl"""
#import module1
#from module2 import pts, pt_normal
#from module4_ptcloud import final_psl
from module6 import satisfied
import numpy as np
#from scipy.stats import norm
import matplotlib.pyplot as plt
import time
from collections import Counter
start_time = time.time()

satisfied_object_index = [satisfied[psl_] for psl_ in satisfied.keys()]
#print(satisfied_object_index)
satisfied_index = list(np.concatenate(satisfied_object_index))
# combine all object # captured w/satisfaction
s_count = Counter(satisfied_index) # count
count_data = s_count.values()
#print(count_data)

score_ = np.asarray(list(count_data))
""" Compute average and standard deviation """

mu = np.average(score_)
std = np.std(score_)
_ = plt.hist(score_, bins='auto')
#plt.show()
# mu,std = norm.fit(score_)
# max_score = np.amax(score_)
# p = norm.pdf(score_, mu, std)
# bins = np.arange(0,max_score+1,500)

"""Figure(1)"""
# plt.figure(1)
# plt.hist(score_,bins =bins,alpha=0.6, color='g',rwidth=0.5)
# plt.xlabel('Number of views (Score) ', fontsize=15)
# plt.ylabel('Number of object points', fontsize=15)
# plt.title('Object Points Score Histogram', fontsize=15)
# plt.grid('on')
# plt.show()

"""" Showing the normal distribution """
# mu,std = norm.fit(score_)
# p = norm.pdf(score_, mu, std)
# bins = np.arange(0,max_score+1,50)

"""Figure(2)"""
# plt.figure(2)
# plt.hist(score_, bins= bins, density=True, alpha=0.6, color='g',rwidth=0.50)
# xmin, xmax = plt.xlim()
# x = np.linspace(xmin, xmax, 100)
# p = norm.pdf(x, mu, std)
# plt.plot(x, p, 'k', linewidth=2)
# plt.xlabel('Number of views (Score) ', fontsize=15)
# plt.ylabel('Probability', fontsize=15)
# plt.title('Object Points Score Histogram', fontsize=15)
# plt.grid('on')
# plt.show()
print(f" average of point scores : {mu:.2f} | standard deviation: {std:.2f}")
#print( f'processing time (module7) {time.time()-start_time:.2f} second')
