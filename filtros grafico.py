""" Plots for the TD.
    Deixando explícitas os filtros de cada gráfico
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pickle


indicadores = ['quant_efluentes_liquidos',
               'quant_poluentes_emitidos',
               'quant_residuos_solidos',
               'co2_emissions']


def count_unique_firms(base):
    num_firms = dict()
    for key in base:
        num_firms[key] = base[key].groupby(by=['ano', 'region', 'massa_salarial']).agg('size').reset_index()
        num_firms[key][0] = 1
        num_firms[key] = num_firms[key].groupby(by=['ano', 'region']).agg('size').reset_index()
    return num_firms


def plot_boxplot(data, x='ano', y='quant_tonelada', number=1, region=''):
    sns.boxplot(data=data, x=x, y=y, whis=(0, 100))
    plt.title(f'{x}_{y}_{region}'.capitalize())
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

    # gráfico - teste para separar o tipo de poluente atmosférico:
    # key = 'poluentes_atm'
    # indicator = 'quant_poluentes_emitidos'
    # poluente_emitido = ['Material Particulado (MP)',
    #                     'Monóxido de carbono (CO)',
    #                     'Óxidos de nitrogênio (NOx)',
    #                     'Óxidos de enxofre (SOx)']
    # for poluente in poluente_emitido:
    #     base = data[key][(data[key]['Poluente emitido'] == poluente) &
    #                      (data[key]['isic_12'] == setor)]
    #     plot_boxplot(base, y=poluente, number=number)

    # Gráfico 5 a 9 e 10 a 14 TD - poluentes atmosféricos por setores econômicos e por região (valores acima de zero)
    regions = ['Sudeste', 'Norte', 'Sul', 'Centro-oeste', 'Nordeste']
    for key, indicator in zip(['poluentes_atm', 'emissoes',], ['quant_poluentes_emitidos', 'co2_emissions']):
        for region in regions:
            base = data[key][(data[key][indicator] > minimum) &
                             (data[key]['region'] == region)]
            plot_boxplot(base, y=indicator, number=number, region=region)
            number += 1

    # grafico 15 TD - indicador eficiência de tratamento de efluentes por setor econômico (valores >0 e <100)
    key = 'efluentes'
    indicator = 'perc_efficiency_treatment'
    value = [0, 100]
    base = data[key][(data[key][indicator] > min(value)) &
                     (data[key][indicator] < max(value))]
    plot_boxplot(base, y=indicator, number=number)
    number += 1

    # grafico 16 TD - efluentes liquidos  acima de 9000 m3/h - nacional
    key = 'efluentes'
    indicator = 'quant_efluentes_liquidos'
    minimum = 9000
    year = 2010
    # TODO FIX GRAPHS
    base = data[key][(data[key][indicator] > minimum) &
                     (data[key]['isic_12'] == setor) &
                     (data[key]['ano'] > year) &
                     (data[key]['region'] == region)]
    plot_boxplot(base, y=indicator, number=number)
    number += 1

    # análise da proporcionalidade da poluição por região
    # calculo da razão-somatória do indicador por estado ou DF de cada região pela quantidade de empresa em cada regiao
    quantidade_empresas = count_unique_firms(data)
    for key in data:
        for indicador in indicadores:
            if indicador in data[key]:
                sum_indicador = data[key].groupby(by=['ano', 'region'])[indicador].agg('sum').reset_index()
                quantidade_empresas[key]['razao'] = sum_indicador[indicador] / quantidade_empresas[key][0]
                for region in regions:
                    plot_boxplot(quantidade_empresas[key][quantidade_empresas[key]['region'] == region],
                                 y='razao', number=number, region=region)
                    number += 1


if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    gera_plots(b)
