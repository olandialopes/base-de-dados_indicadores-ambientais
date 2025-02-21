import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from base_adjustments_to_analyze import chaves
from filtros_grafico import plot_boxplot

year = {'efluentes': 2010, 'poluentes_atm': 2010, 'residuos_solidos1': 2012,
        'residuos_solidos2': 2012, 'emissoes': 2002}
year_t = dict()

ind_keys = {'eco_efic_quant_efluentes_liquidos': 'Efluentes líquidos',
            'eco_efic_co2_emissions': 'Emissãos de CO2',
            'eco_efic_quant_residuos_solidos': 'Resíduos sólidos',
            'eco_efic_quant_poluentes_emitidos': 'Poluentes emitidos',
            'eco_efic_quantidade_energia_padrao_calorias': 'Quantidade de energia (calorias)',
            'eco_efic_quant_consumida_energia_acordo_tipo': 'Quantidade de energia consumida'
            }

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


def calcular_num_firms_region(base):
    num_firms = dict()
    for key in base:
        num_firms[key] = base[key].groupby(by=['ano', 'region']).agg('size').reset_index()
    return num_firms


def indicators_boxplot(base, region=None):
    for key in base:
        for indicator in base[key]:
            if indicator.startswith('eco_efi'):
                # Format base
                base_t = base[key][(base[key][indicator].notnull()) &
                                   (base[key]['ano'] >= year[key])]

                lims = base_t['ano']
                year_t[key] = (lims.min(), lims.max())
                plot_boxplot(data=base_t, y=indicator, co2=indicator,
                             ylabel='Ecoeficiência',
                             title=f'Ecoeficiência / Setores Econômicos \n {ind_keys[indicator]}',
                             ylim_inferior=0, ylim_superior=10 ** 5, region=region)
                #plot_graphs(base_t, key=key, indicador=indicator)
            # else:
            #     plot_boxplot(data=base, x='ano', y=indicador)
            #     # fig, ax = plt.subplots()
            #     # sns.boxplot(data=base[key], x='ano', y=indicator, whis=(0, 100), ax=ax)
            # sns.despine(bottom=True, left=True)
            # plt.savefig(f'figures/boxplot_{key}_{indicator}.png')
            # plt.show()


def calcular_eco_efficiency_indicator(base, region=None):
    for key in base:
        # Filter the DataFrame based on the region (if provided)
        if region:
            filtered_df = base[key][(base[key]['massa_salarial'] > 0) & (base[key]['region'] == region)]
        else:
            filtered_df = base[key][(base[key]['massa_salarial'] > 0)]

        # Drop rows with NaN values in 'massa_salarial'
        filtered_df = filtered_df.dropna(subset=['massa_salarial'])

        # Iterate over the indicators
        for indicator in chaves:
            if indicator != 'perc_efficiency_treatment' and indicator in filtered_df:
                # Drop rows with NaN values in the current indicator
                filtered_df = filtered_df.dropna(subset=[indicator])

                # Ensure that the denominator is greater than zero
                filtered_df = filtered_df[filtered_df[indicator] > 0]

                # Calculate the eco-efficiency indicator
                filtered_df[f'eco_efic_{indicator}'] = filtered_df['massa_salarial'] / filtered_df[indicator]

        # Update the original DataFrame with the calculated indicators
        base[key] = filtered_df

    return base


def plot_graphs(base: pd.DataFrame, key, indicador, region=None):
    title_plot = f'Ecoeficiência / Ano \n {ind_keys[indicador]}'
    title = f'lineplot_{key}_{indicador}.png'

    plt.figure(figsize=(16, 7))
    palette = sns.color_palette("husl", 12)
    i = 0
    for sec in base['isic_12'].unique():
        if sec:
            bs = base[(base['isic_12'] == sec)]
            sns.lineplot(data=bs, x='ano', y=indicador, color=color_palette[sec],
                         marker='o', markersize=10, linewidth=2, errorbar=None, palette=[palette[i]])
            i += 1

    plt.xlabel('Ano', labelpad=5)
    plt.ylabel('Ecoeficiência', labelpad=10)
    plt.xlim((year_t[key][0] - .1, year_t[key][1] + .1))
    plt.ylim(0)
    for value in plt.yticks()[0]:
        plt.axhline(y=value, color='black', linestyle='-', alpha=0.3, linewidth=.75)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)
    plt.xticks(base['ano'].unique(), rotation=45)
    plt.subplots_adjust(left=0.05)
    plt.legend(list(base['isic_12'].unique()), loc='upper left', bbox_to_anchor=(.97, 1))
    plt.title(title_plot)
    plt.savefig(os.path.join('figures', title))


if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    # Plot with ecoefficiency

    base2 = calcular_eco_efficiency_indicator(b)
    emissions = base2['emissoes']
    emissions = emissions[['ano', 'mun', 'isic_12', 'massa_salarial', 'co2_emissions', 'eco_efic_co2_emissions']]

    out = emissions.groupby(by=['isic_12', 'mun', 'ano']).agg(np.median)

    # indicators_boxplot(base2)
    #
    # for region in ['Sudeste', 'Norte', 'Sul', 'Centro-oeste', 'Nordeste']:
    #     base3 = calcular_ecoficiencia_indicator(b, region=region)
    #     indicators_boxplot(base3, region=region)
    #
    # n_firms = calcular_num_firms_region(b)
