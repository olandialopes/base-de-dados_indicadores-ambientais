import os
import pandas as pd
import numpy as np

# TODO:
# 1. A quantidade de efluentes líquidos da Base 1 está em qual unidade? 0,4 o que?
# 2. Separar a base de poluentes por tipo de Poluente
# 3. Separar base emissões em emissões CO2 e energia consumida

# Colunas a serem excluidas
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
                                   'Quantidade Consumida': 'quant_consumida_energia',
                                   'Energia': 'tipo_energia_consumida', 'Emissões de CO2': 'co2_emissions'}

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
            # Aqui,  código para excluir as linhas onde a coluna "Ano" está vazia
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


def main(p0, paths, to_exclude):
    cnpjs = pd.DataFrame(columns=['CNPJ', 'Ano'])
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
        bases[each] = categorize_setor_economico(bases[each])
        cnpjs = pd.concat([cnpjs, getting_company_codes(bases[each])]).drop_duplicates()
        bases[each].rename(columns=renaming_variables[each])
    cnpjs.to_csv('cnpjs.csv', index=False)
    return bases, cnpjs


if __name__ == '__main__':
    p = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}

    f0 = '../PS3/ambiental/original_data'
    # f0 = '../base-de-dados_indicadores-ambientais'

    b, cn = main(p0=f0, paths=p, to_exclude=variaveis_excluidas)

    # TODO: renomear colunas, nome descritivo, mas sem acentos e espaços
    # Exemplo columns: Eficiência do tratamento => treatment_efficiency
    # TODO: transformar quantidades em numérico (float)
    # Exemplo, substituindo ',' por '.' depois astype(float)
