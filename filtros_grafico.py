""" Plots for the TD.
    Deixando explícitas os filtros de cada gráfico
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import os

# Colors to use on boxplots
color_palette = {
    'Manufacturing': 'red',
    'Trade': 'purple',
    'Utilities': 'green',
    'Transport': 'grey',
    'Mining': 'yellow',
    'Government': 'tomato',
    'Construction': 'orange',
    'Business': 'midnightblue',
    'Agriculture': 'navy',
    'OtherServices': 'lawngreen',
    'RealEstate': 'gold',
    'Financial': 'pink'
}

color_region = {
    'Sudeste': 'blue',
    'Nordeste': 'orange',
    'Norte': 'green',
    'Centro-oeste': 'brown',
    'Sul': 'purple'
}


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


def plot_boxplot(data, x='isic_12', y='quant_tonelada',
                number=1, region='', poluente='',
                title = 'Quantidade poluentes / Setores',
                ylim_superior = 200, ylim_inferior = 1,
                ylabel='Quantidade poluente (Mg)',
                xlabel='Setores', pallete=color_palette,
                description=False):
    
    if region or poluente:
        title += '\n'
    if region:
        title += f'{region}'
    if poluente:
        title += f' - {poluente}'

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=x, y=y, palette=pallete)

    # Putting the info about median, mean, min and max values (if description variable is set).
    if description:
        media = data[y].mean()
        mediana = data[y].median()
        minimo = data[y].min()
        maximo = data[y].max()
    
        plt.axhline(y=media, color='grey', linestyle='--', label=f'Média: {media:.2f}')
        plt.axhline(y=mediana, color='red', linestyle='--', label=f'Mediana: {mediana:.2f}')
        plt.axhline(y=minimo, color='blue', linestyle='--', label=f'Mínimo: {minimo:.2f}')
        plt.axhline(y=maximo, color='purple', linestyle='--', label=f'Máximo: {maximo:.2f}')
        plt.legend(loc='best', bbox_to_anchor=(1,1))
        
    plt.title(title)
    plt.ylim((ylim_inferior, ylim_superior))
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(rotation=45)
    plt.tight_layout(pad=2.0)

    title = f'boxplot_{number}'

    if region:
        title += f'_{region}'
    if poluente:
        title += f'_{poluente}'
    title += '.png'

    # Made file path more flexible on different operational systems.
    plt.savefig(os.path.join('plots_td', title))
    #plt.show()
    plt.close()


def gera_plots(data):
    number = 1

    # Gráfico 1 TD - Resíduos sólidos acima de 1 tonelada - setor realestate
    key = 'residuos_solidos2'
    indicador = 'quant_tonelada'
    minimum = 1
    year = 2011
    base1 = data[key][(data[key][indicador] > minimum) &
                      (data[key]['ano'] > year)]
    plot_boxplot(base1, y=indicador, number=number)
    number += 1
    #########################################################################

    # Gráfico 2 TD - resíduos sólidos acima de 26000 toneladas - setor transport/trade
    
    minimum = 26000
    base2 = data[key][(data[key][indicador] > minimum)]
    base2 = base2[(base2['isic_12'] == 'Transport') | (base2['isic_12'] == 'Trade')]
    plot_boxplot(base2, y=indicador, number=number, ylim_inferior=40000, ylim_superior=1000000)
    number += 1

    #########################################################################

    # Gráfico 4 TD - Poluentes atmosféricos por setores econômicos acima de zero. Mesmas keys para regiões
    key = 'poluentes_atm'
    indicador = 'quant_poluentes_emitidos'
    minimum = 0
    base4 = data[key][(data[key][indicador] > minimum)]
    print(base4[indicador])
    plot_boxplot(base4, y=indicador, number=number, 
                 title='Poluentes atmosféricos / Setores econômicos',
                 ylim_superior=5000, description=True)
    number += 1

    # Gráfico - Teste para separar o tipo de poluente atmosférico:
    regions = ['Sudeste', 'Norte', 'Sul', 'Centro-oeste', 'Nordeste']
    key = 'poluentes_atm'
    indicador = 'quant_poluentes_emitidos'
    poluente_emitido = ['Material Particulado (MP)',
                        'Monóxido de carbono (CO)',
                        'Óxidos de nitrogênio (NOx)',
                        'Óxidos de enxofre (SOx)']
    for region in regions:
        for poluente in poluente_emitido:
            base = data[key][(data[key]['tipo_poluente'] == poluente) &
                             (data[key]['region'] == region)]
            if len(base) > 0:
                plot_boxplot(base, y=indicador, number=number,
                             region=region, poluente=poluente,
                             ylim_superior=3500, description=True)
                number += 1

    # Gráfico 5 a 9 e 10 a 14 TD - poluentes atmosféricos por setores econômicos e por região (valores acima de zero)

    for key, indicador in zip(['poluentes_atm', 'emissoes',], ['quant_poluentes_emitidos', 'co2_emissions']):
        for region in regions:
            base = data[key][(data[key][indicador] > minimum) &
                             (data[key]['region'] == region)]
            plot_boxplot(base, y=indicador,
                        number=number, region=region,
                        ylim_superior=30000,
                        title='Poluentes atmosféricos / Setores econômicos',
                        description=True)
            number += 1

    # Gráfico 15 TD - Indicador eficiência de tratamento de efluentes por setor econômico (valores >0 e <= 100).
    key = 'efluentes'
    indicador = 'perc_efficiency_treatment'
    value = [0, 100]
    base = data[key][(data[key][indicador] > min(value)) &
                     (data[key][indicador] < max(value))]
    plot_boxplot(base, y=indicador, number=number,
                 ylim_inferior=1, ylim_superior=100,
                 title='Indicador eficiência efluentes / Setor',
                 ylabel='Indicador eficiência efluentes (0 < valor < 100)')
    number += 1
    ##########################################################################################################


    # Gráfico 16 TD - Efluentes líquidos  acima de 9000 m3/h - nacional
    key = 'efluentes'
    indicador = 'quant_efluentes_liquidos'
    minimum = 9000
    year = 2010
    base = data[key][(data[key][indicador] > minimum) &
                     (data[key]['ano'] > year)]
    if len(base) > 0:
        plot_boxplot(base, y=indicador, number=number,
                     ylim_inferior=minimum, ylim_superior=50000,
                     title = 'Efluentes líquidos / Setores',
                     ylabel='Efluentes líquidos (m3/h)')
        number += 1

    # análise da proporcionalidade da poluição por região
    # calculo da razão-somatória do indicador por estado ou DF de cada região pela quantidade de empresa em cada regiao
    quantidade_empresas = count_unique_firms(data)
    for key in data:
        for indicador in indicadores:
            if indicador in data[key]:
                sum_indicador = data[key].groupby(by=['ano', 'region'])[indicador].agg('sum').reset_index()
                quantidade_empresas[key]['razao'] = sum_indicador[indicador] / quantidade_empresas[key][0]
                quantidade_empresas[key].to_csv(f'output/quantidade_empresas_{key}.csv', index=False)
                
                plot_boxplot(quantidade_empresas[key],
                                y='razao', number=number, ylabel='Indicador por região',
                                x='region', pallete=color_region, ylim_inferior=200, ylim_superior=150000,
                                title='Indicador / Região', xlabel='Regiões')
                number += 1


if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    gera_plots(b)
