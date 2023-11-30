# Estimating the year-to-year compute power increase of supercomputer
# computing power.

import numpy as np
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt

# Downloaded from https://ourworldindata.org/grapher/supercomputer-power-flops?time=earliest..2022
# Data source: TOP500 Supercomputer Database (2023)
# OurWorldInData.org/technological-change | CC BY
df = pd.read_csv('supercomputer-power-flops.csv')

df['log_gflops'] = np.log(df['Floating-Point Operations per Second (GFLOPS)'])

regress = scipy.stats.linregress(df.index, df['log_gflops'])

print(f'intercept: {regress.intercept}')
print(f'slope: {regress.slope}')
print(f'exp(slope): {np.exp(regress.slope)}')

df['yhat'] = np.exp(regress.intercept + df.index*regress.slope)


### optimize

#df2 = 


### plots

plt.figure()
plt.plot(df['Year'], df['Floating-Point Operations per Second (GFLOPS)'])
plt.plot(df['Year'], df['yhat'], 'b--')
plt.yscale('log', base=10)


plt.figure(figsize=(8, 4))

# How long does it take to get an answer to a calculation that takes
# 10 million years in year 0 computer if we first wait for n years and
# then run the computation on that year's model?

a = 10_000_000
x = 1.0/np.exp(regress.slope)
n = np.arange(50)
total_time = n + a * x**n

plt.step(n, total_time, where='post')
plt.yscale('log', base=10)
plt.gca().set_yticks([100, 1000, 10_000, 100_000, 1_000_000, 10_000_000])
plt.gca().set_yticklabels(['100', '1 000', '10 000', '100 000', '1 milj', '10 milj'])
plt.xlabel('Odotusaika ennen laskennan aloittamista (vuosia)')
plt.ylabel('Vastaukseen saamiseen kuluva aika (vuosia)')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.savefig('laskenta-aika.png', dpi=100)

plt.show()

