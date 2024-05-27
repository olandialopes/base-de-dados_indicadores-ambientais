import pickle
from scipy.stats import kstest, mannwhitneyu, kruskal
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

inds  = [      'quant_poluentes_emitidos',
               'co2_emissions',
               'massa_salarial',
               'eco_efic_quant_efluentes_liquidos',
               'eco_efic_co2_emissions',
               'eco_efic_quant_residuos_solidos',
               'eco_efic_quant_poluentes_emitidos',
               'eco_efic_quantidade_energia_padrao_calorias',
               'eco_efic_quant_consumida_energia_acordo_tipo' ]


def ktest(base, level=.05):
    
    stats = {'base': [], 'ks_statistic': [], 'p_value': [], 'norm?': [] }

    for i, key in enumerate(base):
        datab = base[key][(base[key][inds[i]].notnull()) &
                           base[key][inds[i]] > 0].reset_index(drop=True)[inds[i]]
        ks_value, p_value = kstest(datab, 'norm')
        stats['base'].append(key)
        stats['ks_statistic'].append(ks_value)
        stats['p_value'].append(p_value)
        stats['norm?'].append('Sim' if p_value >= level else 'Não')

    df = pd.DataFrame.from_dict(stats)
    df.to_csv('kolmogorov_smirnov_test.csv')

def difference_relevance(base):

    from ecoefficiency import calcular_ecoficiencia_indicator
    import numpy as np
    sig_level = .06
    eco_base = calcular_ecoficiencia_indicator(base)

    
    for region in ['Sudeste', 'Nordeste', 'Sul', 'Norte', 'Centro-oeste']:
        results = {'base': [], 'indicator': [], 'differences': []}
        for key in eco_base:
            for indicator in eco_base[key]:
                if indicator in inds:
                    k = [ eco_base[key][(eco_base[key]['isic_12'] == setor) &
                                        (eco_base[key][indicator].notnull()) &
                                        (eco_base[key][indicator] > 0) &
                                        (eco_base[key]['region'] == region)][indicator] \
                    for setor in eco_base[key]['isic_12'].unique() if setor]
                    
                    _, p_value = kruskal(*k)

                    results['base'].append(key)
                    results['indicator'].append(indicator)
                    medians = {}
                    for setor in eco_base[key]['isic_12'].unique():
                        if setor:
                            medians[setor] = eco_base[key][(eco_base[key]['isic_12'] == setor) &
                                                        (eco_base[key][indicator].notnull()) &
                                                        (eco_base[key][indicator] > 0) &
                                                        (eco_base[key]['region'] == region)][indicator].median()
                            
                            if f'{setor} median' not in results:
                                results[f'{setor} median'] = []

                            results[f'{setor} median'].append(medians[setor])
                            
                    if p_value < sig_level:

                        differs = [setor for setor in medians.keys() if abs(medians[setor] - np.mean(list(medians.values())) > 1.5 * np.std(list(medians.values())))]                
                        results['differences'].append('\n'.join(differs))
                    else:
                        results['differences'].append('null')
        df = pd.DataFrame.from_dict(results)
        df.to_csv(f'kruskal_test_{region}.csv')

def lines_news(base):

    ecog = ['eco_efic_quant_poluentes_emitidos',
            'eco_efic_co2_emissions']
    

    # indicators = {  'quant_efluentes_liquidos': {'marker': 'o', 'div': 1, 'c': '#d53838'},
    #                 'quant_poluentes_emitidos': {'marker': '>', 'div': 10, 'c': '#4e8a34'},
    #                 'quant_residuos_solidos': {'marker': 's', 'div': 100, 'c': '#e7b51e'},
    #                 'co2_emissions': {'marker': '^', 'div': 100, 'c': '#442f87'}}
                    
    year = 2013
    plt.figure(figsize=(12, 7))
    
    # ind_keys = {'quant_efluentes_liquidos': 'Efluentes líquidos',
    #             'co2_emissions': 'CO2 Emissions',
    #             'quant_residuos_s olidos': 'Resíduos sólidos',
    #             'quant_poluentes_emitidos': 'Poluentes emitidos',
    #             'quantidade_energia_padrao_calorias': 'Quantidade de energia (calorias)',
    #             'quant_consumida_energia_acordo_tipo': 'Quantidade de energia consumida',
    #         }

    # print([key for key in base])
    # input()
    div = 10**1

    key = 'poluentes_atm'
    indicador = 'eco_efic_quant_poluentes_emitidos'

    massa = (base['poluentes_atm'].loc[:, 'massa_salarial'] + base['emissoes'].loc[:, 'massa_salarial']) / 2

    dataset = base[key][(base[key][indicador].notnull()) & 
                               (base[key]['ano'] >= year)]
 

    sns.lineplot(data=dataset, x='ano', y=indicador,
    marker='o', markersize=8, linewidth=2, errorbar=None)

    key = 'emissoes'
    indicador = 'eco_efic_co2_emissions'

    dataset = base[key][(base[key][indicador].notnull()) & 
                                    (base[key]['ano'] >= year)]

    sns.lineplot(data=dataset, x='ano', y=indicador,
    marker='^', markersize=8, linewidth=2, errorbar=None)

    dataset['massa_salarial'] = dataset['massa_salarial'] / div
    
    sns.lineplot(data=dataset, x='ano', y='massa_salarial',
    marker='s', markersize=8, linewidth=2, errorbar=None)
        
    plt.grid(True, which='major', axis='y', color='black', alpha=.5)
    plt.ylabel('')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.yticks(list(map(lambda x: x*10**6, [0, .5, 1, 1.5, 2, 2.5])))
    plt.gca().spines['bottom'].set_visible(True)
    plt.gca().spines['left'].set_visible(True)
    plt.xlabel('Ano')   
    plt.legend(['Ecoeficiência poluentes emitidos',
    'Ecoeficiência emissão CO2', 'Massa salarial'],
     loc='upper right', frameon=False,  bbox_to_anchor=(1.13, 1.16),
    fontsize=14, labelspacing=.7)
    plt.xticks([y for y in range(year, 2021)] ,rotation=45)
    plt.savefig('eco_poluentes.png')
    plt.clf()

def lines_newss(base):

    import numpy as np
    plt.figure(figsize=(16, 7))
    salary = 'massa_salarial'
    ind_keys = {'eco_efic_quant_efluentes_liquidos': 'Efluentes líquidos',
                'eco_efic_co2_emissions': 'CO2 Emissions',
                'eco_efic_quant_residuos_solidos': 'Resíduos sólidos',
                'eco_efic_quant_poluentes_emitidos': 'Poluentes emitidos',
                'eco_efic_quantidade_energia_padrao_calorias': 'Quantidade de energia (calorias)',
                'eco_efic_quant_consumida_energia_acordo_tipo': 'Quantidade de energia consumida',
            }
    for key in base:
        for indicador in base[key]:
            if indicador.startswith('eco_efi') and indicador != 'eco_efic_co2_emissions':
                # Filtrar e ordenar o DataFrame
                dataset = base[key][(base[key][indicador].notnull()) & 
                                     (base[key][indicador] > 0) &
                                     (base[key][salary].notnull()) &
                                     (base[key][salary] > 0)]
                dataset = dataset.sort_values(by=salary)
                
                # Definir os intervalos de x
                num_intervalos = 70
                intervalos_x = np.linspace(dataset[salary].min(), dataset[salary].max(), num_intervalos + 1)

                # Calcular a média de y em cada intervalo de x
                media_y_por_intervalo = []
                for i in range(num_intervalos):
                    intervalo_x_atual = dataset[(dataset[salary] >= intervalos_x[i]) & 
                                                (dataset[salary] <= intervalos_x[i+1])]
                    media_y = intervalo_x_atual[indicador].mean()
                    media_y_por_intervalo.append(media_y)

                # Plotar o lineplot das médias de y em relação aos intervalos de x
                plt.plot(intervalos_x[:-1], media_y_por_intervalo, marker='o')
                plt.xlabel('Massa salarial')
                plt.ylabel('Média de Ecoeficiência')
                plt.title(f'Média de Ecoeficiência em Intervalos de Massa Salarial\n{ind_keys[indicador]}')
                plt.grid(True)
                plt.savefig(os.path.join('plots_td', f'eco_per_salary_{indicador}.png'))
                plt.clf()


def analisys(base):
    datasets = {'emissoes': ['co2_emissions', 'eco_efic_co2_emissions', 'massa_salarial'],
                'poluentes_atm': ['quant_poluentes_emitidos', 'eco_efic_quant_poluentes_emitidos']
               } 

    folder = { 'Indicator': [], 'Comparison of eco-efficiency (2013 - 2020)': []}
    for key in datasets.keys():
        for indicator in datasets[key]:
            folder['Indicator'].append(indicator)
            for year in range(2013, 2021):
                dataset = base[key][(base[key][indicator].notnull()) &
                                    (base[key][indicator] > 0) &
                                    (base[key]['ano'] == year)][indicator]

                if year not in folder.keys():
                    folder[year] = []

                folder[year].append(dataset.median())

            if indicator.startswith('eco_efi'):
                per = ((folder[2020][-1] - folder[2013][-1]) / folder[2013][-1]) * 100
                per_t = f'{-per:.2f} % (↓)' if per < 0 else f'{per:.2f} % (↑)'
                
                folder['Comparison of eco-efficiency (2013 - 2020)'].append(per_t)   
            else:
                folder['Comparison of eco-efficiency (2013 - 2020)'].append('Não se aplica')
    df = pd.DataFrame.from_dict(folder)
    df.to_csv('per_results.csv')

def spearman():
    from scipy.stats import spearmanr
    data = pd.read_csv('per_results.csv')

    ndata = data.drop(columns=['Indicator', 'Comparison of eco-efficiency (2013 - 2020)'])
    matrix, pvalue = spearmanr(ndata, axis=1)

    ticks = ['Emissão CO2',
             'Ecoeficiência emissão CO2',
             'Massa salarial',
             'Poluentes emitidos',
             'Ecoeficiência poluentes emitidos',
             'Ecoeficiência emissão CO2 (2)',
             'PIB nacional',
             'Emissão CO2 (2)']

    sns.set(style="white")
    plt.figure(figsize=(12, 9))
    hmap = sns.heatmap(matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    hmap.set_xticklabels(ticks, rotation=45, ha='right')
    hmap.set_yticklabels(ticks, rotation=0)
    plt.tight_layout(pad=.1)
    plt.subplots_adjust(top=0.85)

    plt.title('Matriz de correlação \n (2013 - 2020)', fontsize=16)
    plt.savefig('correlacao.png')
    #plt.show()

def pca_generator(base: dict):
    data = {'ISIC': [], 'PIB': []}        
    years = list(range(2013, 2021))
    co2 = {2013: 898501000, 2014: 785954000, 2015: 881353000,
           2016: 881859000, 2017: 796443000, 2018: 801146000,
           2019: 1021979000, 2020: 1081876000}
    sectors = {'Manufacturing': 'MA', 'Utilities': 'UT', 'Mining': 'MI', 'Business': 'BU', 'Transport': 'TR', 'Trade': 'TD',
               'Agriculture': 'AG', 'Government': 'GO', 'OtherServices': 'OT', 'Construction': 'CO' , 'RealEstate': 'RE',
               'Financial': 'FI'}
    del base['residuos_solidos1']
    for key in base:
        for setor in base[key]['isic_12'].unique():
            if setor:
                for year in years:
                    data['ISIC'].append(sectors[setor] + str(year)[2:])
                    data['PIB'].append(co2[year])
                            
                    for indicator in inds:
                        if indicator not in data:
                                data[indicator] = []

                        if indicator in base[key]:    
                            value = base[key][(base[key]['ano'] == year) &
                                            (base[key][indicator].notnull()) &
                                            (base[key][indicator] > 0) & 
                                            (base[key]['isic_12'] == setor)][indicator].median()
                            data[indicator].append(value)
                        else:
                            data[indicator].append(0)

        print(f'{key} done!')
    
    # data['quant_residuos_solidos'] = data['quant_residuos_solidos'][384:]
                        
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna().reset_index(drop=True)
    dataset = dataset.groupby('ISIC').sum()
    dataset = dataset.loc[:, ~dataset.columns.str.contains('^Unnamed')] 
    
    
    dataset.to_csv('pca_data.csv')

def pca_graph(file):
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    import seaborn as sns; sns.set_style("whitegrid", {'axes.grid' : False})
    import numpy as np

    dataset = pd.read_csv(file)
    target_dataset = dataset['co2_emissions']
    num_dataset = dataset.drop(columns=['ISIC', 'co2_emissions'])
    X = num_dataset.values
    Y = target_dataset.values

    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    pca = PCA()
    X_new = pca.fit_transform(X)

    def myplot(score,coeff,labels=None):
        xs = score[:,0]
        ys = score[:,1]
        n = coeff.shape[0]
        scalex = 1.0/(xs.max() - xs.min())
        scaley = 1.0/(ys.max() - ys.min())
        plt.scatter(xs * scalex,ys * scaley, c = Y, s=100, cmap='viridis', alpha=.6)
        for i in range(n):
            plt.arrow(0, 0, coeff[i,0], coeff[i,1], color ='b', alpha = 1, linewidth=.75)
            if labels is None:
                plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
            else:
                plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color='black', ha = 'center', va = 'center')
        plt.xlim(-1,1)
        plt.ylim(-1,1)
        plt.title('Análise de componentes principais (PCA)')
        plt.xlabel("PC{}".format(1))
        plt.ylabel("PC{}".format(2))
        plt.grid()

    labels = list(num_dataset.columns)
    myplot(X_new[:,0:2],np.transpose(pca.components_[0:2, :]),labels=labels)
    plt.show()
    

if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    from ecoefficiency import calcular_ecoficiencia_indicator
    base = calcular_ecoficiencia_indicator(b)
    #pca_generator(base)

    pca_graph('pca_data.csv')

    # dataset = pd.read_csv('pca_data.csv')
    
    # dataset = dataset.groupby('ISIC').sum()
    # dataset.to_csv('pca_data.csv')

    # dataset = dataset[:20]

    # X_var = dataset[['Mediana']]

    # norm = StandardScaler()
    # norm = norm.fit_transform(X_var)

    # pca_op = PCA(n_components=2)
    # X_pca = pca_op.fit_transform(norm)

    # pca1 = pca_op.components_[0]
    # components = dataset['ISIC'].unique() 

    # dataset['PCA'] = X_pca

    # plt.figure(figsize=(10, 6))

    # for isic in components:
    #     plt.scatter(X_pca[dataset['ISIC'] == isic], dataset[dataset['ISIC'] == isic]['ISIC'], label=isic)

    # for i, (isic, coef) in enumerate(zip(components, pca1)):
    #     plt.arrow(0, 0, coef * 3, i, head_width=.1, head_length=.1, fc='r', ec='r')
    #     plt.text(coef * 3, i, isic, ha='center', va='center', color='r')

    # plt.xlabel('Componente Principal 1 (PC1)')
    # plt.ylabel('ISIC')
    # plt.title('Biplot - Análise de Componentes Principais (PCA)')
    # plt.grid(True)
    # plt.legend()
    # plt.show()
    

    

    

    