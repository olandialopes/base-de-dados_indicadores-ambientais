""""
Lê as bases limpas.
Salvas localmente como bases (formato pickle), após rodar read_organize_databases.py

Analisar os indicadores (README.md)

"""
from typing import Any

import pandas as pd
import os
import pickle
import csv
from collections import defaultdict


print("Diretório atual:", os.getcwd())

paths = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}
# Wider technical note 2/2021.
# tradutor_concla_ibge = {'A': ['01', '02', '03'],
#                         'B': ['05', '06', '07', '08', '09'],
#                         'C': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
#                               '24', '25', '26', '27', '28', '29', '30', '31', '32', '33'],
#                         'D': ['35'],
#                         'E': ['36', '37', '38', '39'],
#                         'F': ['41', '42', '43'],
#                         'G': ['45', '46', '47'],
#                         'H': ['49', '50', '51', '52', '53'],
#                         'I': ['55', '56'],
#                         'J': ['58', '59', '60', '61', '62', '63'],
#                         'K': ['64', '65', '66'],
#                         'L': ['68'],
#                         'M': ['69', '70', '71', '72', '73', '74', '75'],
#                         'N': ['77', '78', '79', '80', '81', '82'],
#                         'O': ['84'],
#                         'P': ['85'],
#                         'Q': ['86', '87', '88'],
#                         'R': ['90', '91', '92', '93'],
#                         'S': ['94', '95', '96'],
#                         'T': ['97'],
#                         'U': ['99']
#                         }
#
# tradutor_isis_12 = {'Agriculture': ['A'],
#                     'Mining': ['B'],
#                     'Manufacturing': ['C'],
#                     'Utilities': ['D', 'E'],
#                     'Construction': ['F'],
#                     'Trade': ['G', 'I'],
#                     'Transport': ['H'],
#                     'Business': ['J', 'M', 'N'],
#                     'Financial': ['K'],
#                     'RealEstate': ['L'],
#                     'Government': ['O', 'P', 'Q'],
#                     'OtherServices': ['R', 'S', 'T', 'U']
#                     }


def emissions_by_municipality(data):
    pass


def quant_efluentes_cnae(data):
    data['clas_cnae20'] = data['clas_cnae20'].str[:2]
    print(data.groupby(by='clas_cnae20').agg('mean')['quant_efluentes_liquidos'].sort_values(ascending=False).head(20))


if __name__ == '__main__':
    nome = 'bases_massa_desindentificada'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

# Concatenar todos os DataFrames em um único DataFrame
data = pd.concat(b.values(), ignore_index=True)

# -------------------------------------------------------------------------------------------
# Inserção de dicionário dentro de dicionário
results: defaultdict[Any, dict] = defaultdict(dict)
#  Agrupar os dados por 'ano' e 'class_cnae20' e somar a quantidade de efluentes líquidos

chaves = ['quant_efluentes_liquidos', 'quant_poluentes_emitidos', 'quant_residuos_solidos',
          'quant_consumida_energia_acordo_tipo', 'quantidade_energia_padrao_calorias', 'co2_emissions']


# pasta para outuput dos arquivos
pasta_saida = 'analise descritiva'

# Loop para cada chave
for chave in chaves:
    # Criar um nome de arquivo com base na chave (por exemplo, 'media_desvio_quant_efluentes_liquidos.txt')
    caminho_arquivo = os.path.join(pasta_saida, f'media_desvio_{chave}.txt')

    # Filtrar os dados onde 'perc_efficiency_treatment' é menor ou igual a 80% e diferente de zero
    filtered_data = data[(data['perc_efficiency_treatment'] <= 80) & (data['perc_efficiency_treatment'] != '0')]

    # Criar um novo DataFrame com as colunas desejadas
    filtered_data = filtered_data[['clas_cnae20', 'perc_efficiency_treatment']]

    # Imprimir o percentual abaixo de 80% - conteúdo de filtered_data na tela
    # print(filtered_data)

    # Contar a quantidade de ocorrências de cada valor na coluna 'clas_cnae20'
    count_by_cnae20 = filtered_data['clas_cnae20'].value_counts().reset_index()

    # Renomear as colunas - cnae e número de ocorrências de não conformidade (abaixo de 80#)
    count_by_cnae20.columns = ['class_cnae20', 'qtde']

    # calculando a média e desvio padrão para estado mun e cnae de todos os dados filtrados
    resultado = data.groupby(['ano', 'clas_cnae20', 'estado', 'mun'])[chave].agg(['mean', 'std']).reset_index()
    resultado = data.groupby(['ano', 'clas_cnae20', 'estado'])[chave].agg(['mean', 'std']).reset_index()
    resultado = data.groupby(['ano', 'clas_cnae20'])[chave].agg(['mean', 'std']).reset_index()
    # Abrir o arquivo para escrita

    # Encontre o CNAE com a maior geração de resíduos sólidos
    max_residuos_solidos_cnae = data.groupby('clas_cnae20')['quant_residuos_solidos'].sum().idxmax()
    max_residuos_solidos_valor = data.groupby('clas_cnae20')['quant_residuos_solidos'].sum().max()
    print(f'O CNAE com a maior geração de resíduos sólidos é {max_residuos_solidos_cnae} com um total de {max_residuos_solidos_valor} resíduos sólidos gerados.')

    with open(caminho_arquivo, 'w') as arquivo_saida:
        # Escrever os resultados no arquivo
        arquivo_saida.write(f'Resultados para {chave}:\n')
        arquivo_saida.write(resultado.to_string(index=False))

        # Salvar a contagem por CNAE em um arquivo
        output_cont_cnae = os.path.join(pasta_saida, 'contagem_cnae20.txt')

        with open(output_cont_cnae, 'w') as arquivo_saida:
            arquivo_saida.write('Contagem por CNAE:\n')
            arquivo_saida.write(count_by_cnae20.to_string(index=False))
