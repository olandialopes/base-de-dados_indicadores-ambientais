import os
import pandas as pd
import numpy as np
import pickle
from change_cnae_to_12_sectors import from_cnae_2digitos_to_12_mip_sectors

""" REAVALIAÇÃO DO ARQUIVO READ AND ORGANIZE DATABASES VISANDO JUNÇÇÃO DE CNPJS E EMISSOES POR SETORES E MUNICIPIOS 
    VIA CNPJS
    
    1. CALCULAR MEDIA EMISSOES POR SETORES E POR MUNICIPIO. CONJUNTO DE ANOS A DEFINIR PARA REPRESENTATIVIDADE
    2. DEPOIS JUNTAR COM MASSA SALARIAL MEDIA POR SETORES E MUNICIPIO 2010.
"""

# 1. A quantidade de efluentes líquidos da Base 1 está em m3/h
# Consultar GUIA RAPP para detalhes sobre variáveis

# Colunas a serem excluídas
variaveis_excluidas = {'efluentes': [
    'Código da Categoria', 'Razão Social', 'Código do Detalhe', 'Desc. Monitoramento Utilizado',
    'Compart. Ambiental da Emissão', 'Tipo de Emissão', 'Tipo Corpo Receptor',
    'Classe do Corpo Receptor', 'Nome do Corpo Hídrico', 'Corpo Receptor',
    'Qual?', 'Empresa Receptora do Efluente', 'Tipo de Emissão Para o Solo',
    '(Se outro) Qual?', 'Situação Cadastral',
    'Nível de Tratamento', 'Tipo de Tratamento', 'Detalhe'
],
    'poluentes_atm': [
        'Código da Categoria', 'Razão Social', 'Código do Detalhe', 'Detalhe',
        'Metodologia utilizada', 'Situação Cadastral'
    ],
    'residuos_solidos1': [
        'Código da Categoria', 'Código do Detalhe', 'Detalhe', 'Cod. Resíduo',
        'Tipo de Resíduo', 'Razão Social do gerador',
        'Tipo de monit. realizado', 'Tipo de Finalidade', 'Finalidade da Transferência',
        'CNPJ da emp. de Armazen/Destin',
        'Raz. soc. emp. Armazen/Destin', 'Situação Cadastral',
        'Identif. do Resíduo NBR 10.004', 'Efic. do sist. de tratamento'
    ],
    'residuos_solidos2': [
        'Código da Categoria', 'Razão Social do gerador', 'Código do Detalhe', 'Detalhe', 'Cód. Resíduo',
        'Tipo de Resíduo',
        'Situação Cadastral'
    ],
    'emissoes': [
        'Código da Categoria', 'Código do Detalhe', 'Detalhe', 'Observações',
        'Razão Social', 'Situação Cadastral', 'Densidade',
        'Unidade de Medida - densidade', 'Justificativa para alteração da densidade',
        'Poder Calorífico Inferior', 'Unidade de Medida - Poder Calorífico Inferior',
        'Justificativa para alteração do Poder Calorífico Inferior',
        'Justificativa para Alteração do Conteúdo de Carbono', 'Fator de Oxidação',
        'Unidade de Medida - Fator de Oxidação',
        'Justificativa para Alteração do Fator de Oxidação', 'Conteúdo de Carbono',
        'Unidade de Medida - Conteúdo de Carbono'
    ]
}

# Define a dictionary to map categories to sector codes
sector_mapping = {
    'Administradora de Projetos Florestais': 1,
    'Extração e Tratamento de Minerais': 2,
    'Indústria Química': 3,
    'Indústria Metalúrgica': 3,
    'Indústria de Produtos Minerais Não Metálicos': 3,
    'Indústria Mecânica': 3,
    'Indústria Têxtil': 3,
    'Indústria de Vestuário': 3,
    'Calçados e Artefatos de Tecidos': 3,
    'Indústria de Madeira': 3,
    'Indústria de Produtos de Matéria Plástica': 3,
    'Indústria de material Elétrico': 3,
    'Eletrônico e Comunicações': 3,
    'Indústrias Diversas': 3,
    'Indústria de Material de Transporte': 3,
    'Indústria de Papel e Celulose': 3,
    'Indústria de Borracha': 3,
    'Indústria de Couros e Peles': 3,
    'Indústria do Fumo': 3,
    'Indústria de Produtos Alimentares e Bebidas': 3,
    'Serviços de Utilidade': 4,
    'Obras civis - não relacionadas no Anexo VIII da Lei nº 6.938/1981,807': 5,
    'Veículos Automotores - Pneus - Pilhas e Baterias': 6,
    'Transporte, Terminais, Depósitos e Comércio': 7,
    'Serviços Administrativos': 8,
    'Turismo': 8
}

renaming_variables = {'efluentes': {'CNPJ': 'cnpj', 'Estado': 'estado', 'Município': 'mun',
                                    'Categoria de Atividade': 'cat_activity', 'Ano': 'ano',
                                    'Quantidade': 'quant_efluentes_liquidos',
                                    'Eficiência do tratamento': 'perc_efficiency_treatment'},
                      'poluentes_atm': {'CNPJ': 'cnpj', 'Estado': 'estado', 'Município': 'mun',
                                        'Categoria de Atividade': 'cat_activity', 'Ano': 'ano',
                                        'Quantidade': 'quant_poluentes_emitidos', 'Poluente emitido': 'tipo_poluente'},
                      'residuos_solidos1': {'CNPJ': 'cnpj', 'Estado': 'estado', 'Município': 'mun',
                                            'Categoria de Atividade': 'cat_activity', 'Ano': 'ano',
                                            'Quantidade': 'quant_residuos_solidos',
                                            'Classif. do Resíduo NBR 10.004': 'tipo_residuo',
                                            'Unidade': 'unidade'},
                      # Com isso, os nomes das bases de resíduos vão estar harmonizados e podem ser unidos
                      'residuos_solidos2': {'CNPJ': 'cnpj', 'Estado': 'estado', 'Município': 'mun',
                                            'Categoria de Atividade': 'cat_activity', 'Ano': 'ano',
                                            'Quantidade Gerada': 'quant_residuos_solidos',
                                            'Classificação Resíduo': 'tipo_residuo',
                                            'Unidade': 'unidade'},
                      'emissoes': {'CNPJ': 'cnpj', 'Estado': 'estado', 'Município': 'mun',
                                   'Categoria de Atividade': 'cat_activity', 'Ano': 'ano',
                                   'Quantidade Consumida': 'quant_consumida_energia_acordo_tipo',
                                   'Energia': 'quantidade_energia_padrao_calorias',
                                   'Tipo de Fonte Energética': 'tipo_energia',
                                   'Unidade de Medida': 'unidade_medida',
                                   # Note um espaço no nome da coluna...
                                   'Emissões de CO2 ': 'co2_emissions'}
                      }


def getting_company_codes(data):
    if 'CNPJ' in data.columns and 'Ano' in data.columns:
        cnpjs = data[['CNPJ', 'Ano']].sort_values(by=['CNPJ', 'Ano']).drop_duplicates()
    else:
        # Lidar com o caso em que as colunas não existem no DataFrame
        # Isso pode incluir a criação das colunas ou outra ação apropriada.
        cnpjs = pd.DataFrame(columns=['CNPJ', 'Ano'])  # Exemplo: Criar um DataFrame vazio
    return cnpjs


# Define a function to categorize the sector based on the category
def categorize_setor_economico(data, col='Categoria de Atividade'):
    if col in data.columns:
        data['cod_setor'] = data[col].map(sector_mapping)
    return data


# Excluir as colunas indesejadas, cujos nomes estão acima
def cleaning_data(data, cols_to_exclude):
    for col in cols_to_exclude:
        if col in data.columns:
            data = data.drop(columns=col, axis=1)
    # Excluindo linhas onde a coluna "Ano" está vazia
    if 'Ano' in data.columns:
        data = data.dropna(subset=['Ano'])
    return data


def checking_geolocation(data, col):
    data[col] = data[col].str.replace('.', '', regex=True).str.replace(',', '.', regex=True)  # 44.934,23
    data[col] = data[col].replace('', '0.0').astype(float)  # ZERO NO LUGAR DE ESPACO VAZIO  13409.23
    data.loc[data[col] == 0, col] = np.nan
    # Excluding out of bounds for the case of Brazil
    if col == 'Latitude':
        data.loc[data[col] > 6, col] = np.nan
        data.loc[data[col] < -34, col] = np.nan
    if col == 'Longitude':
        data.loc[data[col] < -74, col] = np.nan
        data.loc[data[col] > - 35, col] = np.nan
    # Further checking needed. Confirm location coincides with given municipality.
    return data


def clean_cnpjs(data):
    data['cnpj'] = (data['cnpj'].str.replace('.', '', regex=True)
                    .str.replace('/', '', regex=True)
                    .str.replace('-', '', regex=True))
    return data


# Functions to handle each base quantities and necessary transformation
def process_efluentes(data):
    col = 'quant_efluentes_liquidos'
    data[col] = (data[col].str.replace('.', '', regex=True).str.replace('###########', '', regex=True)
                 .str.replace(',', '.', regex=True))
    data[col] = pd.to_numeric(data[col], errors='coerce')
    # Valores negativos?
    data.loc[data[col] < 0, col] = 0

    col = 'perc_efficiency_treatment'
    data[col] = data[col].str.replace('\%', '', regex=True)
    data[col] = pd.to_numeric(data[col], errors='coerce')
    return data


def process_poluentes(data):
    col = 'quant_poluentes_emitidos'
    data = process_generic_col(data, col)
    return data


def process_residuos(data):
    col = 'quant_residuos_solidos'
    data = process_generic_col(data, col)
    return data


def process_emissoes(data):
    cols = ['quant_consumida_energia_acordo_tipo', 'quantidade_energia_padrao_calorias', 'co2_emissions']
    for col in cols:
        data = process_generic_col(data, col)
    return data


def process_generic_col(data, col):
    # Generic transformation function applied repeatedly, given the column
    data[col] = (data[col].str.replace('.', '', regex=True)
                 .str.replace(',', '.', regex=True))
    data[col] = pd.to_numeric(data[col], errors='coerce')
    return data


process_quantities = {'efluentes': process_efluentes,
                      'poluentes_atm': process_poluentes,
                      'residuos_solidos1': process_residuos,
                      'residuos_solidos2': process_residuos,
                      'emissoes': process_emissoes
                      }


def main(p0, paths, to_exclude):
    bases = dict()
    each: str
    for each in ['efluentes', 'poluentes_atm', 'residuos_solidos1', 'residuos_solidos2', 'emissoes']:
        bases[each] = pd.read_csv(os.path.join(p0, paths[each]), sep=';')
        bases[each] = cleaning_data(bases[each], to_exclude[each])
        if 'Latitude' in bases[each]:
            bases[each] = checking_geolocation(bases[each], 'Latitude')
            bases[each] = checking_geolocation(bases[each], 'Longitude')
        if 'residuos' in each:
            bases[each] = bases[each].rename(columns={'CNPJ do gerador': 'CNPJ',
                                                      'Ano da geração': 'Ano',
                                                      'Ano da geração do resíduo': 'Ano'})
        # bases[each] = categorize_setor_economico(bases[each])
        bases[each].rename(columns=renaming_variables[each], inplace=True)
        # # Sending each base to process their quantities accordingly
        bases[each] = process_quantities[each](bases[each])
        bases[each] = clean_cnpjs(bases[each])
    return bases


f1 = 'data/cnpjs_massa_salarial.csv'
input_format = {'cnpj': str,
                'ano': int,
                'clas_cnae10': str,
                'clas_cnae20': str,
                'clas_cnae95': str,
                'massa_salarial': float
                }
f2 = 'data/tradutor_cnae10_cnae20.sas7bdat'


def return_massa_cnae_base():
    data = pd.read_csv(f1, dtype=input_format)

    # Reading tradutor 10 para 20.
    tradutor = pd.read_sas(f2, format='sas7bdat', encoding='utf-8')
    # Sorting by cnae20_professional, so that we can keep only Xs when duplicates on cnae10
    tradutor = tradutor.sort_values(by=['cnae10', 'cnae_20_preferencial'])
    tradutor = tradutor.drop_duplicates(subset='cnae10', keep='first')

    # Merging tradutor with existing data so that I can later use the tranlation to input into clas_cnae20
    data = pd.merge(data, tradutor, left_on='clas_cnae10', right_on='cnae10', how='left')
    data['clas_cnae20'].fillna(data['cnae20'], inplace=True)

    # Just keeping essential columns
    cols_to_keep = ['cnpj', 'ano', 'massa_salarial', 'clas_cnae20']
    data = data[cols_to_keep]

    # Dropping if no information on massa salarial
    data = data[~data['massa_salarial'].isna()]
    data['clas_cnae20'] = data['clas_cnae20'].astype(str).str[:2]
    return data


if __name__ == '__main__':
    p = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',''
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}

    f0 = '../base-de-dados_indicadores-ambientais/original_data'

    b = main(p0=f0, paths=p, to_exclude=variaveis_excluidas)
    e = b['emissoes']
    e = e[['cnpj', 'ano', 'co2_emissions']]
    e = e[e.co2_emissions > 0]

    m = return_massa_cnae_base()
    m = from_cnae_2digitos_to_12_mip_sectors(m, col='clas_cnae20')
    m.drop(['clas_cnae20', 'letter_code'], axis=1, inplace=True)

    em = pd.merge(m, e, on=['cnpj', 'ano'], how='right')
    em['ano'] = em.ano.astype(int)

    t = em.groupby('isic_12').agg('sum')
    t['eco'] = t['co2_emissions'] / t['massa_salarial']
    t.sort_values(by='eco')

    # mun = pd.read_csv('cnpj_mun_code.csv')
    # mun = mun.loc[mun.groupby('cnpj_cei')['ano'].idxmax()]
    # mun['cnpj'] = mun['cnpj_cei'].astype(str).str.zfill(14)
    # mun.drop(['cnpj_cei', 'ano'], axis=1, inplace=True)
    #
    # emun = pd.merge(em, mun, on='cnpj', how='left')
    # emun = emun[~emun.massa_salarial.isna()]
    # emun['codemun'] = emun['codemun'].astype(int)
    #
    # # Getting the median of massa salarial by sector and municipality over all available years
    # # Then calculating eco-efficiency
    # emun.drop(['ano', 'cnpj'], axis=1, inplace=True)
    # eco = emun.groupby(['isic_12', 'codemun']).median().reset_index()
    # eco = eco[eco.massa_salarial > 0]
    # eco['eco'] = eco['co2_emissions'] / eco['massa_salarial']
