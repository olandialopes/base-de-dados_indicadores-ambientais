""" Ajustes finais para base antes de analisar.

# Quais ajustes na base ainda faltam antes de começar a análise
# 1. Contar as empresas, por setor, por regiao, por estado, por ano, por município
# 2. Padronizar as unidades de tipo de resíduo e retirar indicadores com unidade desconhecida
# 3. Padronizar as unidades de tipo de energia
"""

import pickle
import seaborn as sns
from matplotlib import pyplot as plt
from ridge_density_plot import draw_density_plot
import change_cnae_to_12_sectors

chaves = ['quant_efluentes_liquidos', 'quant_poluentes_emitidos', 'quant_residuos_solidos',
          'quant_consumida_energia_acordo_tipo', 'quantidade_energia_padrao_calorias', 'co2_emissions',
          'perc_efficiency_treatment']

paths = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}

regions = {'Sudeste': ['SAO PAULO', 'RIO DE JANEIRO', 'MINAS GERAIS', 'ESPIRITO SANTO', ],
           'Centro-oeste': ['DISTRITO FEDERAL', 'GOIAS', 'MATO GROSSO', 'MATO GROSSO DO SUL'],
           'Nordeste': ['PERNAMBUCO', 'CEARA', 'PARAIBA', 'BAHIA',
                        'RIO GRANDE DO NORTE', 'PIAUI',
                        'MARANHAO', 'SERGIPE', 'ALAGOAS'],
           'Sul': ['PARANA', 'RIO GRANDE DO SUL', 'SANTA CATARINA'],
           'Norte': ['PARA', 'TOCANTINS', 'AMAZONAS', 'AMAPA', 'RONDONIA', 'ACRE', 'RORAIMA']}


def convert_to_isic(base):
    for each in paths:
        base[each]['cnae2d'] = base[each]['clas_cnae20'].str[:2]
        base[each] = change_cnae_to_12_sectors.from_cnae_2digitos_to_12_mip_sectors(base[each], 'cnae2d')
        for col in ['clas_cnae20', 'cnae2d', 'letter_code', 'cod_setor', 'cat_activity']:
            try:
                base[each] = base[each].drop(col, axis=1)
            except KeyError:
                pass
    return base


def no_conformity_indicators(base):
    """ Adds an indicator of conformity to the base of efluentes"""
    key = 'efluentes'
    indicator = 'perc_efficiency_treatment'
    base[key].loc[:, 'nao_conformidade'] = 0
    base[key].loc[:, 'conformidade'] = 0
    base[key].loc[(base[key][indicator] < 80) & (base[key][indicator] >= 0), 'nao_conformidade'] = 1
    base[key].loc[(base[key][indicator] >= 80) & (base[key][indicator] <= 100), 'conformidade'] = 1
    return base


def add_regions(base):
    for key in base:
        base[key]['region'] = base[key]['estado'].map({state: region
                                                       for region, states in regions.items()
                                                       for state in states})
    return base


def adjust_units_residuos(base, key='residuos_solidos1'):
    if key == 'residuos_solidos1':
        conversao_ton = {'kilogramas': 1e-3,
                         'Tonelada': 1,
                         'Grama': 1e-6,
                         'Miligrama': 1e-9,
                         'Ton. por ano': 1,
                         }
    else:
        conversao_ton = {'kilogramas': 1e-3, 'Litro': 0.001, 'Unidade': 1}

    def adjust(row):
        try:
            return row['quant_residuos_solidos'] * conversao_ton[row['unidade']]
        except KeyError:
            return None

    base[key].loc[:, 'quant_tonelada'] = base[key].apply(lambda row: adjust(row), axis=1)
    return base


def adjust_units_energia(base):
    base = adjust_units_residuos(base, 'residuos_solidos1')
    base = adjust_units_residuos(base, 'residuos_solidos2')
    return base


def plot_quantities(pivot_table, key, col1, col2):
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table, annot=True, fmt='d', cmap='viridis', cbar_kws={'label': 'Count'})
    plt.title(f'Counts by {col1} and {col2}')
    plt.tight_layout()
    plt.savefig(f'figures/{key}_{col1}_{col2}_count.png')
    plt.show()


def indicators_ridge_plot(base):
    for key in base:
        for indicator in chaves:
            if indicator in base[key]:
                draw_density_plot(base, key, 'ano', indicator)


def indicators_boxplot(base):
    for key in base:
        for indicator in chaves:
            if indicator in base[key]:
                fig, ax = plt.subplots()
                sns.boxplot(data=base[key], x='ano', y=indicator, whis=(0, 100), ax=ax)
                sns.despine(bottom=True, left=True)
                plt.savefig(f'figures/boxplot_{key}_{indicator}.png')
                plt.show()


def plot_count_firms(base, col1='region', col2='isic_12'):
    # Contar as empresas, por regiao, por estado, por ano, # por município
    for key in base:
        pivot_table = base[key].pivot_table(index=col1, columns=col2, aggfunc='size', fill_value=0)
        plot_quantities(pivot_table, key, col1, col2)


def main(base):
    base = convert_to_isic(base)
    base = no_conformity_indicators(base)
    base = add_regions(base)
    base = adjust_units_energia(base)
    plot_count_firms(base)
    # base = calcular_ecoficiencia_indicator(base)
    indicators_boxplot(base)
    return base


density_table = {
        'óleo Diesel': 853,
        'Gás Natural (Seco)': 0.63,
        'Gás Natural Úmido': 0.63,
        'Gasolina': 0.715,
        'Lubrificantes': 902,
        'Biomassa - Álcool Etílico Anidro': 791.5,
        'Biomassa - Biodiesel B100': 880,
        'Querosene Iluminante': 803,
        'Querosene de Aviação': 760,
        'Gás Liquefeito de Petróleo (GLP)': 522,
        'Eletricidade - Rede Pública': None,  # Representing 'NA' as None
        'Petróleo Bruto': 980,
        'Óleo Combustível': 967,
        'Coque de Petróleo': 830,
        'Gasolina de Aviação': 710,
        'Nafta': 750,
        'Óleo de Xisto': 970,
        'Biomassa - Carvão Vegetal': 490,
        'Biomassa - Outro Combustível Renovável-Lenha de Eucalipto': 800,
        'Outro Combustível Não-Renovável-THINNER': 845
    }


# ___________________________________________________________________
def get_density(material):
    return density_table.get(material, None)


def adjust_units_emissoes(base, key='emissoes'):
    if key == 'emissoes':
        base[key]['conversao_ener'] = (base[key]["quant_consumida_energia_acordo_tipo"] *
                                       density_table[base][key]['unidade_medida'])
    return base


if __name__ == '__main__':
    nome = 'bases_massa_desidentificada'
    nome2 = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    b = main(b)

    with open(nome2, 'wb') as handler:
        pickle.dump(b, handler)

    with open(nome2, 'rb') as handler:
        b = pickle.load(handler)
