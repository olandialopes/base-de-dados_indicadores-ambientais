""" Plots for the TD.
    Deixando explícitas os filtros de cada gráfico
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import os

def description_per_sector(data: pd.DataFrame, csv_obj: pd.DataFrame):
    regions = ['Sudeste', 'Norte', 'Sul', 'Centro-oeste', 'Nordeste']
    key = 'poluentes_atm'
    indicador = 'quant_poluentes_emitidos'
    poluente_emitido = ['Material Particulado (MP)',
                        'Monóxido de carbono (CO)',
                        'Óxidos de nitrogênio (NOx)',
                        'Óxidos de enxofre (SOx)']
    for region in regions:
        for poluente in poluente_emitido:
            for section in data[key]['isic_12'].unique():
                if section:
                    base = data[key][(data[key]['tipo_poluente'] == poluente) &
                                    (data[key]['region'] == region) &
                                    (data[key]['isic_12'] == section) &
                                    (data[key][indicador] > 0)]
                    plot_title = f'{region} {poluente} {section}'
                    media = base[indicador].mean()
                    mediana = base[indicador].median()
                    min = base[indicador].min()
                    max = base[indicador].max()
                    if media and mediana and min and max:
                        csv_obj = csv_obj.append({'box_plot': plot_title,
                                'Média': base[indicador].mean(),
                                'Mediana': base[indicador].median(),
                                'Mínimo': base[indicador].min(),
                                'Máximo': base[indicador].max()
                                }, ignore_index=True)
    return csv_obj
                

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

indicadores_t = dict(zip(
    indicadores, ['Quantidade efluentes líquidos',
                  'Quantidade poluentes emitidos',
                  'Quantidade resíduos sólidos',
                  'Emissão de CO2']
))


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
                ylabel='Quantidade poluente (t)',
                xlabel='Setores', pallete=color_palette,
                description=False, des_data: pd.DataFrame = None,
                co2=''):
    
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

        plot_title = f'{region} {poluente} {co2}'.strip() if poluente or region or co2 else \
                                                    'Nacional'
        des_data = des_data.append({'box_plot': plot_title,
                         'Média': media,
                         'Mediana': mediana,
                         'Mínimo': minimo,
                         'Máximo': maximo
                         }, ignore_index=True)
        
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
    if co2:
        title += f'_{co2}'
    title += '.png'

    # Made file path more flexible on different operational systems.
    plt.savefig(os.path.join('plots_td', title))
    #plt.show()
    plt.close()
    return des_data


def gera_plots(data, csv_description=None):
    number = 1    

    # Massa Salarial
    indicador = 'massa_salarial'
    new_data = pd.concat([ data[key][['massa_salarial', 'isic_12']] for key in data ],axis=0 )
    new_data = new_data[(new_data[indicador] > 0)]
    new_data = new_data.reset_index(drop=True)

    plot_boxplot(new_data, y=indicador, number=number,
                 ylabel='Massa salarial', title='Massa salarial / Setores econômicos',
                 ylim_inferior=0, ylim_superior=2*10**8)
    number += 1
    
    # Gráfico 1 TD - Resíduos sólidos acima de 1 tonelada - setor realestate
    key = 'residuos_solidos2'
    indicador = 'quant_tonelada'
    minimum = 1
    year = 2011
    base1 = data[key][(data[key][indicador] > minimum) &
                      (data[key]['ano'] > year)]
    plot_boxplot(base1, y=indicador, number=number, co2='Residuos Solidos (Nacional)',
                 region=' ',
                 ylabel='Resíduos sólidos (t)',
                 title='Resíduos sólidos / Setores econômicos')
    number += 1
    #########################################################################

    # Gráfico 2 TD - resíduos sólidos acima de 26000 toneladas - setor transport/trade
 
    minimum = 26000
    base2 = data[key][(data[key][indicador] > minimum)]
    base2 = base2[(base2['isic_12'] == 'Transport') | (base2['isic_12'] == 'Trade')]
    plot_boxplot(base2, y=indicador, number=number,
                 ylim_inferior=minimum, ylim_superior=1000000,
                 co2='Residuos Solidos acima de 26000 t',
                 region=' ',
                 ylabel='Resíduos sólidos (t)',
                 title='Resíduos sólidos / Setores econômicos')
    number += 1

    # 250000 toneladas por região
    minimum = 25 * 10**4
    year_t = 2012
    base2_t = data[key][(data[key][indicador] > minimum) &
                        (data[key]['ano'] >= year_t)]
    base2_t = base2_t.dropna().reset_index(drop=True)
    csv_description = plot_boxplot(base2_t, y=indicador, number=number,
                 ylim_inferior=minimum, ylim_superior=base2_t[indicador].mean(),
                 co2='Residuos solidos (Grandes Geradores)',
                 ylabel='Resíduos sólidos (t)',
                 title='Resíduos sólidos (Grandes Geradores) / Setores econômicos',
                 description=True, des_data=csv_description)   
    number += 1
    #########################################################################

    # Gráfico 4 TD - Poluentes atmosféricos por setores econômicos acima de zero. Mesmas keys para regiões
    key = 'poluentes_atm'
    indicador = 'quant_poluentes_emitidos'
    minimum = 1
    base4 = data[key][(data[key][indicador] > minimum)]
    csv_description = plot_boxplot(base4, y=indicador, number=number, 
                 title='Poluentes atmosféricos / Setores econômicos',
                 ylim_superior=base4[indicador].mean(), description=True, des_data=csv_description,
                 co2='Nacional', ylabel='Quantidade poluente emitido')
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
                             (data[key]['region'] == region) &
                             (data[key][indicador] > minimum)]
            if len(base) > 0:
                csv_description = plot_boxplot(base, y=indicador, number=number,
                             region=region, poluente=poluente,
                             ylim_superior=base[indicador].mean(), description=True,
                             des_data=csv_description, ylabel='Quantidade poluente emitido')
                number += 1

    # Gráfico 5 a 9 e 10 a 14 TD - poluentes atmosféricos por setores econômicos e por região (valores acima de zero)

    for key, indicador in zip(['poluentes_atm', 'emissoes',], ['quant_poluentes_emitidos', 'co2_emissions']):
        for region in regions:
            base = data[key][(data[key][indicador] > minimum) &
                             (data[key]['region'] == region)]
            if indicador == 'quant_poluentes_emitidos':
                title_base = 'Quantidade de poluentes emitidos'
            else:
                title_base = 'Emissão de CO2' 
            csv_description = plot_boxplot(base, y=indicador,
                        number=number, region=region,
                        ylim_superior=base[indicador].mean(),
                        title=f'{title_base} / Setores econômicos',
                        description=True, des_data=csv_description,
                        ylabel='Quantidade poluente emitido',
                        co2=indicador)
            number += 1

    for key, indicador in zip(['poluentes_atm', 'emissoes',], ['quant_poluentes_emitidos', 'co2_emissions']):
        
        base = data[key][(data[key][indicador] > minimum)]
        if indicador == 'quant_poluentes_emitidos':
            title_base = 'Quantidade de poluentes emitidos'
        else:
            title_base = 'Emissão de CO2' 
        csv_description = plot_boxplot(base, y=indicador,
                    number=number, region=' ',
                    ylim_superior=7*10**5,
                    title=f'{title_base} / Setores econômicos',
                    description=True, des_data=csv_description,
                    ylabel='Quantidade poluente emitido',
                    co2='Emissão de CO2 (Nacional)')
    number += 1

    # Gráfico 15 TD - Indicador eficiência de tratamento de efluentes por setor econômico (valores >0 e <= 100).
    key = 'efluentes'
    indicador = 'perc_efficiency_treatment'
    value = [0, 100]
    base = data[key][(data[key][indicador] > min(value)) &
                     (data[key][indicador] <= max(value))]
    plot_boxplot(base, y=indicador, number=number,
                 ylim_inferior=1, ylim_superior=100,
                 title='Indicador eficiência efluentes / Setor',
                 ylabel='Indicador eficiência efluentes (0 < valor <= 100)',
                 region=' ',
                 co2=indicador)
    number += 1
    ##########################################################################################################


    # Gráfico 16 TD - Efluentes líquidos  acima de 9000 m3/h - nacional
    key = 'efluentes'
    indicador = 'quant_efluentes_liquidos'
    minimum = 9000
    year = 2010
    base = data[key][(data[key][indicador] > minimum)]
    if len(base) > 0:
        csv_description = plot_boxplot(base, y=indicador, number=number,
                     ylim_inferior=minimum, ylim_superior=10**5,
                     title = 'Efluentes líquidos / Setores',
                     ylabel='Efluentes líquidos (m3/h)',
                     co2=f'{indicador} | Nacional',
                     description=True, des_data=csv_description)
        number += 1

    # Per region
    for region in regions:
        base2 = data[key][(data[key][indicador] > minimum) &
                         (data[key]['ano'] > year) &
                         (data[key]['region'] == region)]
        if len(base2) > 0:
            csv_description = plot_boxplot(base2, y=indicador, number=number,
                        ylim_inferior=minimum, ylim_superior=10**5,
                        title = f'Efluentes líquidos / Setores \n {region}',
                        ylabel='Efluentes líquidos (m3/h)',
                        co2=f'{indicador} | {region}',
                        description=True, des_data=csv_description)
            number += 1

    
    if len(base) > 0:
        plot_boxplot(base, y=indicador, number=number, x='region',
                     ylim_inferior=minimum, ylim_superior=10**5,
                     title = 'Efluentes líquidos / Regiões',
                     ylabel='Efluentes líquidos (m3/h)',
                     xlabel='Regiões', pallete=color_region,
                     co2=indicador)
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
                                y='razao', number=number, ylabel='Razão-somatória',
                                x='region', pallete=color_region, ylim_inferior=200, ylim_superior=quantidade_empresas[key]['razao'].mean(),
                                title=f'Proporcionalidade poluição / Região \n {indicadores_t[indicador]}', xlabel='Regiões', co2=indicador)
                number += 1

    return csv_description

if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)
    
     # Init dataframe to csv
    csv_description = pd.DataFrame(columns=['box_plot',
                                            'Média',
                                            'Mediana',
                                            'Máximo',
                                            'Mínimo' ])

    csv_description = gera_plots(b, csv_description=csv_description)
    csv_description = description_per_sector(b, csv_description)
    csv_description = csv_description.dropna().reset_index(drop=True)
    csv_description.to_csv('descritivos.csv')
