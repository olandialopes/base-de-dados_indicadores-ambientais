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
tradutor_concla_ibge = {'A': ['01', '02', '03'],
                        'B': ['05', '06', '07', '08', '09'],
                        'C': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
                              '24', '25', '26', '27', '28', '29', '30', '31', '32', '33'],
                        'D': ['35'],
                        'E': ['36', '37', '38', '39'],
                        'F': ['41', '42', '43'],
                        'G': ['45', '46', '47'],
                        'H': ['49', '50', '51', '52', '53'],
                        'I': ['55', '56'],
                        'J': ['58', '59', '60', '61', '62', '63'],
                        'K': ['64', '65', '66'],
                        'L': ['68'],
                        'M': ['69', '70', '71', '72', '73', '74', '75'],
                        'N': ['77', '78', '79', '80', '81', '82'],
                        'O': ['84'],
                        'P': ['85'],
                        'Q': ['86', '87', '88'],
                        'R': ['90', '91', '92', '93'],
                        'S': ['94', '95', '96'],
                        'T': ['97'],
                        'U': ['99']
                        }

tradutor_isis_12 = {'Agriculture': ['A'],
                    'Mining': ['B'],
                    'Manufacturing': ['C'],
                    'Utilities': ['D', 'E'],
                    'Construction': ['F'],
                    'Trade': ['G', 'I'],
                    'Transport': ['H'],
                    'Business': ['J', 'M', 'N'],
                    'Financial': ['K'],
                    'RealEstate': ['L'],
                    'Government': ['O', 'P', 'Q'],
                    'OtherServices': ['R', 'S', 'T', 'U']
                    }
# Função para obter a categoria com base no código CNAE
def obter_categoria_cnae(codigo_cnae):
    for categoria, codigos in tradutor_concla_ibge.items():
        if codigo_cnae[:2] in codigos:
            return categoria
    return None

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

    # pasta para output dos arquivos

    pasta_saida = 'analise_descritiva'

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Defina a variável 'chaves' aqui
    chaves = ['quant_efluentes_liquidos', 'quant_poluentes_emitidos', 'quant_residuos_solidos',
              'quant_consumida_energia_acordo_tipo', 'quantidade_energia_padrao_calorias', 'co2_emissions']

    # Loop para cada categoria do dicionário tradutor_concla_ibge
    for categoria, codigos in tradutor_concla_ibge.items():
        # Filtrar os dados para a categoria correspondente
        filtered_data = data[data['clas_cnae20'].str[:2].isin(codigos)]

        for chave in chaves:
            # Calcular o máximo para a categoria
            max_valor_categoria = filtered_data[chave].max()
            max_valor = filtered_data[chave].max()

             # Criar um nome de arquivo com base na chave e na categoria
            caminho_arquivo = os.path.join(pasta_saida, f'max_{chave}_categoria_{categoria}.txt')
            caminho_arquivo = os.path.join(pasta_saida, f'max_{chave}_geral.txt')

            with open(caminho_arquivo, 'w') as arquivo_saida:
                  # Escrever o valor máximo no arquivo
                  arquivo_saida.write(f'Máximo para {chave} na categoria {categoria}: {max_valor_categoria}')
                  # Escrever o valor máximo no arquivo
                  arquivo_saida.write(f'Máximo geral para {chave}: {max_valor}')

