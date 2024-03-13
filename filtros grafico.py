""" Plots for the TD.
    Deixando explícitas os filtros de cada gráfico
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pickle


def plot_boxplot(data, x='ano', y='quant_tonelada', number=1):
    sns.boxplot(data=data, x=x, y=y, whis=(0, 100))
    plt.xticks(rotation=90)
    plt.tight_layout(pad=2.0)
    plt.savefig(f'plots_td/boxplot_{number}.png')
    plt.show()
    plt.close()


def gera_plots(data):
    number = 1
    # grafico 1 TD - residuos solidos acima de 1 tonelada - setor realestate
    key = 'residuos_solidos2'
    indicador = 'quant_tonelada'
    setor = 'RealEstate'
    minimum = 1
    year = 2011
    base1 = data[key][(data[key][indicador] > minimum) &
                      (data[key]['isic_12'] == setor) &
                      (data[key]['ano'] > year)]
    plot_boxplot(base1, y=indicador, number=number)
    number += 1

    # grafico 2 TD - residuos solidos acima de 26000 toneladas - setor transport/trade
    for setor in ['Transport', 'Trade']:
        minimum = 26000
        base2 = data[key][(data[key][indicador] > minimum) &
                          (data[key]['isic_12'] == setor)]
        plot_boxplot(base2, y=indicador, number=number)
        number += 1

    # Gráfico 4 TD - poluentes atmosféricos por setores econômicos acima de zero. Mesmas keys para regiões
    key = 'poluentes_atm'
    indicator = 'quant_poluentes_emitidos'
    minimum = 0
    base4 = data[key][(data[key][indicator] > minimum)]
    plot_boxplot(base4, y=indicator, number=number)
    number += 1

    # Gráfico 5 a 9 e 10 a 14 TD - poluentes atmosféricos por setores econômicos e por região (valores acima de zero)
    regions = ['Sudeste', 'Norte', 'Sul', 'Centro-oeste', 'Nordeste']
    for key, indicator in zip(['poluentes_atm', 'emissoes'],
                              ['quant_poluentes_emitidos', 'co2_emissions']):
        for region in regions:
            base = data[key][(data[key][indicator] > minimum) &
                             (data[key]['region'] == region)]
            plot_boxplot(base, y=indicator, number=number)
            number += 1

    # grafico 15 TD - indicador eficiência de tratamento de efluentes por setor econômico (valores >0 e <100)
    key = 'efluentes'
    indicator = 'perc_efficiency_treatment'
    value = [0, 100]
    base = data[key][(data[key][indicator] > min(value)) &
                     (data[key][indicator] < max(value))]
    plot_boxplot(base, y=indicator, number=number)


if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    gera_plots(b)
