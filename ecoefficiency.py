import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from base_adjustments_to_analyze import chaves


def indicators_boxplot(base):
    for key in base:
        for indicator in base[key]:
            if indicator.startswith('eco_efi'):
                fig, ax = plt.subplots()
                sns.boxplot(data=base[key], x='ano', y=indicator, whis=(0, 100), ax=ax)
                sns.despine(bottom=True, left=True)
                plt.savefig(f'figures/boxplot_{key}_{indicator}.png')
                plt.show()


def calcular_ecoficiencia_indicator(base):
    for key in base:
        for indicator in chaves:
            if indicator != 'perc_efficiency_treatment':
                if indicator in base[key]:
                    base[key][f'eco_efic_{indicator}'] = base[key]['massa_salarial'] / base[key][indicator]
    return base


if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    b2 = calcular_ecoficiencia_indicator(b)

