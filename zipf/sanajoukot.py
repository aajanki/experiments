import lzma
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load the input file from
# https://github.com/aajanki/finnish-word-frequencies/releases/download/v1/finnish-word-frequencies-c4.xz
input_file = 'finnish-word-frequencies-c4.xz'

def main():
    wordsets = {
        'viikonpäivät': frozenset([
            'maanantai', 'tiistai', 'keskiviikko', 'torstai', 'perjantai', 'lauantai', 'sunnuntai'
        ]),
        'kuukaudet': frozenset([
            'tammikuu', 'helmikuu', 'maaliskuu', 'huhtikuu', 'toukokuu', 'kesäkuu',
            'heinäkuu', 'elokuu', 'syyskuu', 'lokakuu', 'marraskuu', 'joulukuu'
        ]),
        'planeetat': frozenset([
            'merkurius', 'venus', 'maa', 'mars', 'jupiter', 'saturnus', 'uranus', 'neptunus'
        ]),
        'lukusanat': frozenset([
            'nolla', 'yksi', 'kaksi', 'kolme', 'neljä', 'viisi',
            'kuusi', 'seitsemän', 'kahdeksan', 'yhdeksän', 'kymmenen',
            'yksitoista', 'kaksitoista', 'kolmetoista', 'neljätoista', 'viisitoista',
            'kuusitoista', 'seitsemäntoista', 'kahdeksantoista', 'yhdeksäntoista',
            'kaksikymmentä',
            'kaksikymmentäyksi', 'kaksikymmentäkaksi', 'kaksikymmentäkolme', 'kaksikymmentäneljä', 'kaksikymmentäviisi',
            'kaksikymmentäkuusi', 'kaksikymmentäseitsemän', 'kaksikymmentäkahdeksan', 'kaksikymmentäyhdeksän',
            'kolmekymmentä',
            'kolmekymmentäyksi', 'kolmekymmentäkaksi', 'kolmekymmentäkolme', 'kolmekymmentäneljä', 'kolmekymmentäviisi',
            'kolmekymmentäkuusi', 'kolmekymmentäseitsemän', 'kolmekymmentäkahdeksan', 'kolmekymmentäyhdeksän',
            'neljäkymmentä',
            'neljäkymmentäyksi', 'neljäkymmentäkaksi', 'neljäkymmentäkolme', 'neljäkymmentäneljä', 'neljäkymmentäviisi',
            'neljäkymmentäkuusi', 'neljäkymmentäseitsemän', 'neljäkymmentäkahdeksan', 'neljäkymmentäyhdeksän',
            'viisikymmentä',
            'viisikymmentäyksi', 'viisikymmentäkaksi', 'viisikymmentäkolme', 'viisikymmentäneljä', 'viisikymmentäviisi',
            'viisikymmentäkuusi', 'viisikymmentäseitsemän', 'viisikymmentäkahdeksan', 'viisikymmentäyhdeksän',
            'kuusikymmentä',
            'kuusikymmentäyksi', 'kuusikymmentäkaksi', 'kuusikymmentäkolme', 'kuusikymmentäneljä', 'kuusikymmentäviisi',
            'kuusikymmentäkuusi', 'kuusikymmentäseitsemän', 'kuusikymmentäkahdeksan', 'kuusikymmentäyhdeksän',
            'seitsemänkymmentä',
            'seitsemänkymmentäyksi', 'seitsemänkymmentäkaksi', 'seitsemänkymmentäkolme', 'seitsemänkymmentäneljä', 'seitsemänkymmentäviisi',
            'seitsemänkymmentäkuusi', 'seitsemänkymmentäseitsemän', 'seitsemänkymmentäkahdeksan', 'seitsemänkymmentäyhdeksän',
            'kahdeksankymmentä',
            'kahdeksankymmentäyksi', 'kahdeksankymmentäkaksi', 'kahdeksankymmentäkolme', 'kahdeksankymmentäneljä', 'kahdeksankymmentäviisi',
            'kahdeksankymmentäkuusi', 'kahdeksankymmentäseitsemän', 'kahdeksankymmentäkahdeksan', 'kahdeksankymmentäyhdeksän',
            'yhdeksänkymmentä',
            'yhdeksänkymmentäyksi', 'yhdeksänkymmentäkaksi', 'yhdeksänkymmentäkolme', 'yhdeksänkymmentäneljä', 'yhdeksänkymmentäviisi',
            'yhdeksänkymmentäkuusi', 'yhdeksänkymmentäseitsemän', 'yhdeksänkymmentäkahdeksan', 'yhdeksänkymmentäyhdeksän',
            'sata',
        ]),
        'lukusanat ilman kymppejä': frozenset([
            'yksi', 'kaksi', 'kolme', 'neljä', 'viisi',
            'kuusi', 'seitsemän', 'kahdeksan', 'yhdeksän',
            'yksitoista', 'kaksitoista', 'kolmetoista', 'neljätoista', 'viisitoista',
            'kuusitoista', 'seitsemäntoista', 'kahdeksantoista', 'yhdeksäntoista',
            'kaksikymmentäyksi', 'kaksikymmentäkaksi', 'kaksikymmentäkolme', 'kaksikymmentäneljä', 'kaksikymmentäviisi',
            'kaksikymmentäkuusi', 'kaksikymmentäseitsemän', 'kaksikymmentäkahdeksan', 'kaksikymmentäyhdeksän',
            'kolmekymmentäyksi', 'kolmekymmentäkaksi', 'kolmekymmentäkolme', 'kolmekymmentäneljä', 'kolmekymmentäviisi',
            'kolmekymmentäkuusi', 'kolmekymmentäseitsemän', 'kolmekymmentäkahdeksan', 'kolmekymmentäyhdeksän',
            'neljäkymmentäyksi', 'neljäkymmentäkaksi', 'neljäkymmentäkolme', 'neljäkymmentäneljä', 'neljäkymmentäviisi',
            'neljäkymmentäkuusi', 'neljäkymmentäseitsemän', 'neljäkymmentäkahdeksan', 'neljäkymmentäyhdeksän',
            'viisikymmentäyksi', 'viisikymmentäkaksi', 'viisikymmentäkolme', 'viisikymmentäneljä', 'viisikymmentäviisi',
            'viisikymmentäkuusi', 'viisikymmentäseitsemän', 'viisikymmentäkahdeksan', 'viisikymmentäyhdeksän',
            'kuusikymmentäyksi', 'kuusikymmentäkaksi', 'kuusikymmentäkolme', 'kuusikymmentäneljä', 'kuusikymmentäviisi',
            'kuusikymmentäkuusi', 'kuusikymmentäseitsemän', 'kuusikymmentäkahdeksan', 'kuusikymmentäyhdeksän',
            'seitsemänkymmentäyksi', 'seitsemänkymmentäkaksi', 'seitsemänkymmentäkolme', 'seitsemänkymmentäneljä', 'seitsemänkymmentäviisi',
            'seitsemänkymmentäkuusi', 'seitsemänkymmentäseitsemän', 'seitsemänkymmentäkahdeksan', 'seitsemänkymmentäyhdeksän',
            'kahdeksankymmentäyksi', 'kahdeksankymmentäkaksi', 'kahdeksankymmentäkolme', 'kahdeksankymmentäneljä', 'kahdeksankymmentäviisi',
            'kahdeksankymmentäkuusi', 'kahdeksankymmentäseitsemän', 'kahdeksankymmentäkahdeksan', 'kahdeksankymmentäyhdeksän',
            'yhdeksänkymmentäyksi', 'yhdeksänkymmentäkaksi', 'yhdeksänkymmentäkolme', 'yhdeksänkymmentäneljä', 'yhdeksänkymmentäviisi',
            'yhdeksänkymmentäkuusi', 'yhdeksänkymmentäseitsemän', 'yhdeksänkymmentäkahdeksan', 'yhdeksänkymmentäyhdeksän',
        ]),
        'sija ja luku päivä': frozenset([
            'päivä', 'päivät', 'päivän', 'päivien', 'päivää', 'päiviä', 'päivänä', 'päivinä',
            'päiväksi', 'päiviksi', 'päivässä', 'päivissä', 'päivästä', 'päivistä', 'päivään', 'päiviin',
            'päivällä', 'päivillä', 'päivältä', 'päiviltä', 'päivälle', 'päiville', 'päivättä', 'päivittä',
            'päivin', 'päivineni'
        ]),
        'sija ja luku lapsi': frozenset([
            'lapsi', 'lapset', 'lapsen', 'lasten', 'lasta', 'lapsia', 'lapsena', 'lapsina',
            'lapseksi', 'lapsiksi', 'lapsessa', 'lapsissa', 'lapsesta', 'lapsista', 'lapseen', 'lapsiin',
            'lapsella', 'lapsilla', 'lapselta', 'lapsilta', 'lapselle', 'lapsille', 'lapsetta', 'lapsitta',
            'lapsin', 'lapsineni'
        ]),
        'sijamuodot päivä': frozenset([
            'päivä', 'päivän', 'päivää', 'päivänä',
            'päiväksi', 'päivässä', 'päivästä', 'päivään',
            'päivällä', 'päivältä', 'päivälle', 'päivättä'
        ]),
        'sijamuodot lapsi': frozenset([
            'lapsi', 'lapsen', 'lasta', 'lapsena', 
            'lapseksi', 'lapsessa', 'lapsesta', 'lapseen',
            'lapsella', 'lapselta', 'lapselle', 'lapsetta',
        ]),
        'sijamuodot kaupunki': frozenset([
            'kaupunki', 'kaupungin', 'kaupunkia', 'kaupunkina',
            'kaupungiksi', 'kaupungissa', 'kaupungista', 'kaupunkiin',
            'kaupungilla', 'kaupungilta', 'kaupungille', 'kaupungitta'
        ]),
        'sijamuodot ihminen': frozenset([
            'ihminen', 'ihmisen', 'ihmistä', 'ihmisenä',
            'ihmiseksi', 'ihmisessä', 'ihmisestä', 'ihmiseen',
            'ihmisellä', 'ihmiseltä', 'ihmiselle', 'ihmisettä'
        ]),
        'sijamuodot minä': frozenset([
            'minä', 'minun', 'minut', 'minua', 'minuna', 'minuksi', 'minussa', 'minusta', 'minuun',
            'minulla', 'minulta', 'minulle'
        ]),
        'persoonapronominit': frozenset([
            'minä', 'sinä', 'hän', 'me', 'te', 'he'
        ])
    }
    image_path = Path('results')
    image_path.mkdir(parents=True, exist_ok=True)

    all_words = load_frequencies_case_insensitive()

    for name, words in wordsets.items():
        selected = [(word, all_words.get(word.lower(), 0)) for word in words]
        ordered = sorted(selected, key=lambda x: -x[1])
        
        print(name)
        print(ordered)

        plot_frequencies(ordered, name, image_path)

def plot_frequencies(frequencies, title, image_path):
    values = []
    for i, (_, count) in enumerate(frequencies):
        values.append((i + 1, count))
    X = np.array(values)

    plt.style.use('seaborn-v0_8-deep')
    plt.scatter(X[:, 0], X[:, 1], c='C0', s=3)
    plt.gca().set(xscale='log',
                  yscale='log',
                  xlabel='Järjestysluku',
                  ylabel='Esiintymiskertojen lukumäärä',
                  title=title)
    plt.tight_layout()
    plt.savefig(image_path / f'{title}.png')
    #plt.show()
    plt.close()

def load_frequencies_case_insensitive():
    frequencies = {}
    with lzma.open(input_file, 'rt') as f:
        for line in f:
            [freq_str, token] = line.strip().split('\t', 1)

            if re.match(r'\w', token):
                token_lo = token.lower()
                n = int(freq_str)
                frequencies[token_lo] = frequencies.get(token_lo, 0) + n

    return frequencies

if __name__ == '__main__':
    main()
