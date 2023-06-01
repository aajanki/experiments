import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    # probability of a win in a single trial
    p = 0.9
    # numbers of trials to simulate
    num_trials = [10, 50, 100, 200, 300, 400, 500, 800, 1000]
    # the number of simulations per a trial size
    k = 10000

    data = []
    for n in num_trials:
        print(f'n = {n}')

        for _ in range(k):
            seq = random_binary_sequence(p, n)
            longest_streak = longest_consequtive_ones(seq)
            data.append({
                'p': p,
                'n': n,
                'longest_streak': longest_streak,
                'k': k,
            })

    df = pd.DataFrame(data)
    df.to_csv('simulations.csv', index=False)

    sns.lineplot(df, x='n', y='longest_streak',
                 estimator=np.median,
                 errorbar=p90_range)
    plt.xlabel('Sarjan pituus')
    plt.ylabel('')
    plt.title(f'Pisin voittoputki (p = {p}), mediaani ja 5% - 95% vaihteluväli')
    plt.savefig('longest_streak.png')
    plt.show()


def random_binary_sequence(p, n):
    a = np.random.rand(n)
    return (a < p).astype(int)


def longest_consequtive_ones(seq):
    longest_streak = 0
    current_streak = 0
    for x in seq:
        if x == 1:
            current_streak += 1
        else:
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 0

    if current_streak > longest_streak:
        longest_streak = current_streak
            
    return longest_streak


def p90_range(x):
    return tuple(np.percentile(x, [5, 95]))


if __name__ == '__main__':
    main()
