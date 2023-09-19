
import matplotlib.pyplot as plt
q = qmax / (1 + np.exp(r * (tpeak - t)))

while q[-1] - q[-2] >= p_target:
    r = 0.06 # growth rate
import matplotlib.pyplot as plt
q = qmax / (1 + np.exp(r * (tpeak - t)))
t.append(t[-1] + 1) # move one step in time
plt.show()
print('The peak oil year is %d.' % (tpeak))
t = [tpeak, tpeak + 1] # start after the peak year, as yearly production is decreasing
plt.xlabel('Time (year)')
plt.xlim(np.floor(tpeak / 5) * 5, np.ceil(t[-1] / 5) * 5)
def hubbert(t, qmax = qmax, r = r, tpeak = tpeak):
q.append(hubbert(t[-1])) # calculate the new accumulated extraction
tpeak = int(round(np.log(qmax/52.4 - 1) / r + 1956))
plt.ylabel('Cumulative oil extraction (Gbarrel)')
print('Yearly oil production drops below %.2f Gbarrel by year %d.' % (p_target, t[-1]))
q = [hubbert(t[-2]), hubbert(t[-1])]
plt.plot(t, q)
return q
qmax = 200 # total resource base
plt.close()
plt.ylim(q[0], qmax)
import numpy as np

p_target = 1
