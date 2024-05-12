import lzma
import re
import numpy as np
import matplotlib.pyplot as plt

# Load the input file from
# https://github.com/aajanki/finnish-word-frequencies/releases/download/v1/finnish-word-frequencies-c4.xz
input_file = 'finnish-word-frequencies-c4.xz'

def main():
    (frequencies, total_count) = load_frequencies()
    values = []
    for i, count in enumerate(frequencies):
        values.append((i + 1, count/total_count))
    X = np.array(values)

    b = 0.04
    plt.style.use('seaborn-v0_8-deep')
    plt.plot([1, 1e8], [b * 1, b * 1e-8], c='C2', ls='--', lw=0.5)
    plt.scatter(X[:, 0], X[:, 1], c='C0', s=3)
    plt.gca().set(xscale='log',
                  yscale='log',
                  xlabel='Järjestysluku',
                  ylabel='Esiintymistodennäköisyys',
                  title='Zipfin laki suomenkielisessä tekstiaineistossa')
    plt.tight_layout()
    plt.savefig('results/zipf-finnish-c4.png')
    plt.show()

def load_frequencies(cutoff=None):
    frequencies = []
    total_count = 0
    with lzma.open(input_file, 'rt') as f:
        for line in f:
            [freq_str, token] = line.strip().split('\t', 1)

            if re.match(r'\w', token):
                freq = int(freq_str)
                frequencies.append(freq)
                total_count += freq

                if cutoff is not None and len(frequencies) >= cutoff:
                    break

    return (frequencies, total_count)

if __name__ == '__main__':
    main()
