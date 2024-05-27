import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from base_adjustments_to_analyze import chaves
from filtros_grafico import plot_boxplot
import pandas as pd
import os
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
import matplotlib.patches as mpatches
from matplotlib_scalebar.scalebar import ScaleBar
from PIL import Image

import re

def substituir_caracteres_latinos(string):
    mapeamento = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'à': 'a',
        'è': 'e',
        'ì': 'i',
        'ò': 'o',
        'ù': 'u',
        'ã': 'a',
        'õ': 'o',
        'â': 'a',
        'ê': 'e',
        'î': 'i',
        'ô': 'o',
        'û': 'u',
        'ç': 'c',
    }

    for latin_char, non_latin_char in mapeamento.items():
        string = string.replace(latin_char, non_latin_char)

    return string

import scipy.stats as stats

year = {'efluentes': 2010, 'poluentes_atm': 2010, 'residuos_solidos1': 2012,
            'residuos_solidos2': 2012, 'emissoes': 2002}
year_t = dict()

# ind_keys = {'eco_efic_quant_efluentes_liquidos': 'Efluentes líquidos',
#                 'eco_efic_co2_emissions': 'Emissão de CO2',
#                 'eco_efic_quant_residuos_solidos': 'Resíduos sólidos',
#                 'eco_efic_quant_poluentes_emitidos': 'Poluentes emitidos',
#                 'eco_efic_quantidade_energia_padrao_calorias': 'Quantidade de energia (calorias)',
#                 'eco_efic_quant_consumida_energia_acordo_tipo': 'Quantidade de energia consumida'
#             }

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

eco_base = {'efluentes': 'eco_efic_quant_efluentes_liquidos',
            'poluentes_atm': 'eco_efic_quant_poluentes_emitidos',
            'residuos_solidos1': 'eco_efic_quant_residuos_solidos',
            'residuos_solidos2': 'eco_efic_quant_residuos_solidos',
            'emissoes': ['eco_efic_quant_consumida_energia_acordo_tipo',
             'eco_efic_quantidade_energia_padrao_calorias',
             'eco_efic_co2_emissions']
            }


def calcular_num_firms_region(base):
    num_firms = dict()
    for key in base:
        eco_efi = eco_base[key]
        num_firms[key] = base[key].groupby(by=['estado', 'mun', 'isic_12']).agg(
            'size').reset_index()
        
    # for key in num_firms:
    #     data = pd.DataFrame(columns=['Municipio', 'Setor', 'Numero de empresas','Mediana_Ecoeficiencia'])
    #     eco_efi = eco_base[key]
    #     for mun in num_firms[key]['mun'].unique():
    #         if mun:
    #             for setor in num_firms[key]['isic_12'].unique():
    #                 if setor:
    #                     sub = base[key][(base[key]['mun'] == mun) & (base[key]['isic_12'] == setor) &
    #                                     (base[key][eco_efi].notnull())]
    
    #                     x = num_firms[key][(num_firms[key]['mun'] == mun) &
    #                      (num_firms[key]['isic_12'] == setor) & (num_firms[key][0] >= 3)]
                        
    #                     if not x.empty and not np.isnan(x[0].values[0]):
                            
    #                         data = pd.concat([data, pd.DataFrame({'Municipio': x['mun'].values[0],
    #                                                             'Setor': x['isic_12'].values[0],
    #                                                             'Numero de empresas': x[0].values[0],
    #                                                             'Mediana_Ecoeficiencia': sub[eco_efi].median()}, index=[0])])
    #     data.to_csv(os.path.join('output', f'POLICY_STATE_MEDIAN_{key}.csv'))                        
    return num_firms

def mun_median(base, mun_base):

    for key in mun_base:
        eco_efi = eco_base[key]
        
        data = pd.DataFrame(columns=['Setor', 'Mediana_Ecoeficiencia'])
        
        for setor in mun_base[key]['isic_12'].unique():
            
            setor_filter = mun_base[key][(mun_base[key]['isic_12'] == setor)][0].sum()
            
            if setor and setor_filter > 2:
                mediana = base[key][(base[key]['isic_12'] == setor) &
                                    (base[key][eco_efi] > 0) &
                                    (base[key][eco_efi].notnull())][eco_efi].median()
                if not np.isnan(mediana):
            
                    data = pd.concat([data, pd.DataFrame({'Setor': setor, 'Mediana_Ecoeficiencia': mediana},
                    index=[0])]).reset_index(drop=True)
            
                    data.to_csv(os.path.join('output', f'ecoeficiencia_mediana_isic_12_{key}.csv'))
            
        #########################################################################33

    for key in mun_base:
        eco_efi = eco_base[key]
        
        data = pd.DataFrame(columns=['Estado', 'Mediana_Ecoeficiencia'])
        
        for state in mun_base[key]['estado'].unique():
            
            state_filter = mun_base[key][(mun_base[key]['estado'] == state)][0].sum()
            
            if state and state_filter > 2:
                mediana = base[key][(base[key]['estado'] == state) &
                                    (base[key][eco_efi] > 0) &
                                    (base[key][eco_efi].notnull())][eco_efi].median()
                    
            if not np.isnan(mediana):
            
                data = pd.concat([data, pd.DataFrame({'Estado': state, 'Mediana_Ecoeficiencia': mediana},
                index=[0])]).reset_index(drop=True)
                
                data.to_csv(os.path.join('output', f'ecoeficiencia_mediana_uf_{key}.csv'))
    
    for key in mun_base:
        eco_efi = eco_base[key]
        
        data = pd.DataFrame(columns=['Municipio', 'Mediana_Ecoeficiencia'])
        
        for muni in mun_base[key]['mun'].unique():
            
            muni_filter = mun_base[key][(mun_base[key]['mun'] == state)][0].sum()
            
            if muni and muni_filter > 2:
                mediana = base[key][(base[key]['mun'] == muni) &
                                    (base[key][eco_efi] > 0) &
                                    (base[key][eco_efi].notnull())][eco_efi].median()
                if not np.isnan(mediana):
            
                    data = pd.concat([data, pd.DataFrame({'Municipio': muni, 'Mediana_Ecoeficiencia': mediana},
                    index=[0])]).reset_index(drop=True)
            
                    data.to_csv(os.path.join('output', f'ecoeficiencia_mediana_municipio_{key}.csv'))
        
def get_medians(base):

    indicadores = {'efluentes': 'quant_efluentes_liquidos',
                   'poluentes_atm':'quant_poluentes_emitidos',
                   'residuos_solidos1':'quant_residuos_solidos',
                   'residuos_solidos2':'quant_residuos_solidos',
                   'emissoes': 'co2_emissions'}

    for key in base:
        
        for indicator in base[key]:
            median_data = pd.DataFrame(columns=['ISIC_12'])
            if indicator.startswith('eco_efi'):
                for setor in base[key]['isic_12'].unique():
                    if setor:
                        mediana = base[key][(
                            base[key]['isic_12'] == setor)][indicator].dropna().reset_index(
                                drop=True).median()
                         
                        total = base[key][(base[key]['isic_12'] == setor)][indicadores[key]].sum()

                        median_data = pd.concat([median_data, pd.DataFrame(
                            {'ISIC_12': setor, indicadores[key]: total, 'Ecoeficiência': mediana}, index=[0])]).reset_index(drop=True)
                median_data = median_data.sort_values(by='Ecoeficiência').reset_index(drop=True)
                median_data.to_csv(os.path.join('output', f'mediana_por_setor_{key}.csv'))

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
                             ylim_inferior=0, ylim_superior=10**5, region=region)
                #plot_graphs(base_t, key=key, indicador=indicator)
            # else:
            #     plot_boxplot(data=base, x='ano', y=indicador)
            #     # fig, ax = plt.subplots()
            #     # sns.boxplot(data=base[key], x='ano', y=indicator, whis=(0, 100), ax=ax)
                # sns.despine(bottom=True, left=True)
                # plt.savefig(f'figures/boxplot_{key}_{indicator}.png')
                # plt.show()

def calcular_ecoficiencia_indicator(base, region=None):
    year = 2010

    for key in base:
        # -> valores acima de zero (retirando null's).
        
        if region:
            num = base[key][(base[key]['massa_salarial'] > 0) &
             (base[key]['region'] == region) &
             (base[key]['ano'] >= year) &
             (base[key]['massa_salarial'].notnull())]['massa_salarial']
        else:
            num = base[key][(base[key]['massa_salarial'].notnull()) &
                            (base[ key]['massa_salarial'] > 0) &
                            (base[key]['ano'] >= year)]['massa_salarial']
    
        
        # base[key]['massa_salarial'] = base[key]['massa_salarial'].dropna().reset_index(drop=True)
        for indicator in chaves:
            if indicator != 'perc_efficiency_treatment':
                if indicator in base[key]:
                    # -> valores acima de zero (retirando null's)
                    den = base[key][(base[key][indicator].notnull()) &
                                    (base[key][indicator] > 2) &
                                    (base[key]['ano'] >= year)][indicator]

                    # eco eficiência label
                    base[key][f'eco_efic_{indicator}'] = num / den
    return base

def calcular_ecoficiencia_co2(base):

    key = 'emissoes'
    v = {}

    co2 = {2013: 898501000, 2014: 785954000, 2015: 881353000,
           2016: 881859000, 2017: 796443000, 2018: 801146000,
           2019: 1021979000, 2020: 1081876000}
    
    for year in co2.keys():
        num = base[key][(base[key]['massa_salarial'].notnull()) &
                        (base[key]['massa_salarial'] > 0) &
                        (base[key]['ano'] == year)]['massa_salarial'].sum()
        
        if year not in v.keys():
            v[year] = []
        v[year].append(num / co2[year])

    df = pd.DataFrame.from_dict(v)
    df.to_csv('eco_efficiency_co2.csv')
    
def plot_graphs(base: pd.DataFrame, key, indicador, region=None):
    
    title_plot = f'Ecoeficiência / Ano \n {ind_keys[indicador]}'
    title = f'lineplot_{key}_{indicador}.pdf'

    plt.figure(figsize=(16, 7))
    palette = sns.color_palette("husl", 12)
    
    i = 0
    for sec in base['isic_12'].unique():
        if sec:
            bs = base[(base['isic_12'] == sec)]
            sns.lineplot(data=bs, x='ano', y=indicador, color=color_palette[sec],
            marker='o', markersize=10, linewidth=2, errorbar=None)
            i += 1
    
    plt.xlabel('Ano', labelpad=5)
    plt.ylabel('Ecoeficiência', labelpad=10)
    plt.xlim((year_t[key][0]-.1, year_t[key][1]+.1))
    plt.ylim(0)
    for value in plt.yticks()[0]:
        plt.axhline(y=value, color='black', linestyle='-', alpha=0.3, linewidth=.75)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False) 
    plt.subplots_adjust(left=0.05)
    plt.xticks(base['ano'].unique(), rotation=45)
    plt.legend(list(base['isic_12'].unique()), loc='upper left', bbox_to_anchor=(.97, 1))
    plt.title(title_plot)
    plt.savefig(os.path.join('figures', title))

def create_custom_legend(cmap, values, labels, ax, legend_title):
    patches = []
    for value, label in zip(values, labels):
        color = cmap(value)
        patch = mpatches.Patch(color=color, label=label)
        patches.append(patch)
    ax.legend(handles=patches, loc='lower left', title=legend_title,
        fontsize='medium', frameon=False, prop={'size': 10}, title_fontsize='xx-large',
        edgecolor='black')
        
def maps_generator(base):
    
    import geobr
    import matplotlib.pyplot as plt

    res = {'Sudeste': 'Sudeste',
           'Nordeste': 'Nordeste',
           'Sul': 'Sul',
           'Centro-oeste': 'Centro Oeste',
           'Norte': 'Norte'}

    plt.rcParams.update({"font.size": 5})
    regions = geobr.read_region(year=2020)

    # 'efluentes': 'eco_efic_quant_efluentes_liquidos'
    ufs = list(regions['name_region'])

    for key in base:
        for indicator in base[key]:
            if indicator.startswith('eco_efi'):

                ecoindice = {'region': [], 'ecoefficiency': []}
                fig, ax = plt.subplots(figsize=(7, 7))

                plt.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.05)

                for region in base[key]['region'].unique():

                    temp = base[key][(base[key]['region'] == region)][indicator]

                    ecoindice['region'].append(res[region])
                    ecoindice['ecoefficiency'].append(temp.median())

                tomerge = pd.DataFrame.from_dict(ecoindice)
            
                #cmap = plt.cm.Greens  # Use the same colormap as in your data plot
                tomerge['ecoefficiency'] = (tomerge['ecoefficiency'] - tomerge['ecoefficiency'].min()) \
                                            / (tomerge['ecoefficiency'].max() - tomerge['ecoefficiency'].min()) * 1.2

                intervals = [.0, .2, .4, .6, .8, 1.2]
                colors = ['#beffd2', '#74c58c', '#025f1e']

                # Criar a norma de limite dos intervalos
                # norm = BoundaryNorm(intervals, len(colors))
                # # Criar o mapa de cores personalizado
                # cmap = ListedColormap(colors)
                labels = ['0.00 - 0.20', '0.21 - 0.40', '0.41 - 0.60',
                        '0.61 - 0.80', '0.81 - 0.99', '1.01 - 1.20']

                import matplotlib.cm as cm
                create_custom_legend(cm.viridis, intervals, labels, ax, 'Eco-efficiency')
                
                df = regions.merge(tomerge, how='left', left_on='name_region', right_on='region')

                df.boundary.plot(ax=ax, linewidth=.65, edgecolor='black')
                ax.grid(True, linestyle='-', alpha=.5)
                df.plot(ax=ax, column='ecoefficiency', cmap='viridis')
                

                for idx, row in regions.iterrows():
                    plt.annotate(text=row['name_region'], xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                    color='black', fontsize=10, ha='center', va='center')

                ax.set_title(f'Eco-eficciency - {ind_keys[indicator]}', fontsize=16)
                plt.savefig(f'maps/map_{indicator}.png')
                

ind_keys = {'eco_efic_quant_efluentes_liquidos': 'Liquid Effluents',
                'eco_efic_co2_emissions': 'CO2 Emissions',
                'eco_efic_quant_residuos_solidos': 'Solid Waste',
                'eco_efic_quant_poluentes_emitidos': 'Pollutants Emitted',
                'eco_efic_quantidade_energia_padrao_calorias': 'Amount of energy (calories)',
                'eco_efic_quant_consumida_energia_acordo_tipo': 'Amount of energy consumed',
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

eco_base = {'efluentes': 'eco_efic_quant_efluentes_liquidos',
            'poluentes_atm': 'eco_efic_quant_poluentes_emitidos',
            'residuos_solidos1': 'eco_efic_quant_residuos_solidos',
            'residuos_solidos2': 'eco_efic_quant_residuos_solidos',
            'emissoes': 'eco_efic_quantidade_energia_padrao_calorias'
            
            }


if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)


    # Plot with ecoefficiency
    base2 = calcular_ecoficiencia_indicator(b)

    for key in base2:
        base2[key] = base2[key][(base2[key][eco_base[key]].notnull()) &
                               (base2[key][eco_base[key]] > 0)].reset_index()
            

    calcular_ecoficiencia_co2(base2)
    # maps_generator(base2)



    #get_medians(base2)
    # indicators_boxplot(base2)

    # for region in ['Sudeste', 'Norte', 'Sul', 'Centro-oeste', 'Nordeste']:
    #     base3 = calcular_ecoficiencia_indicator(b, region=region)
    #     indicators_boxplot(base3, region=region)
    
    # n_firms = calcular_num_firms_region(base2)
    # #mun_median(base=base2, mun_base=n_firms)
    
