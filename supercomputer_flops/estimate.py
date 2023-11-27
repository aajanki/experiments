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

plt.plot(df['Year'], df['Floating-Point Operations per Second (GFLOPS)'])
plt.plot(df['Year'], df['yhat'], 'b--')
plt.yscale('log',base=10)
plt.show()
