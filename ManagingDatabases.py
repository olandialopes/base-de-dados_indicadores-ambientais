import os
import pandas as pd
import numpy as np


# Colunas a serem excluidas
colunas_indesejadas = [
    'Código da Categoria', 'Razão Social', 'Código do Detalhe', 'Desc. Monitoramento Utilizado',
    'Compart. Ambiental da Emissão', 'Tipo de Emissão', 'Tipo Corpo Receptor',
    'Classe do Corpo Receptor', 'Nome do Corpo Hídrico', 'Corpo Receptor',
    'Qual?', 'Empresa Receptora do Efluente', 'Tipo de Emissão Para o Solo',
    '(Se outro) Qual?', 'Situação Cadastral',
    'Nível de Tratamento', 'Tipo de Tratamento', 'Detalhe'
]


# Excluir as colunas indesejadas, cujos nomes estão acima
def cleaning_data(data, cols_to_exclude):
    data = data.drop(columns=cols_to_exclude, axis=1)
    return data


def checking_geolocation(data, col):
    data[col] = data[col].str.replace(',', '.').astype(float)
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


if __name__ == '__main__':
    f1 = 'relatorio efluentes liquidos_ibama.csv'
    f0 = '../PS3/ambiental'

    efluentes = pd.read_csv(os.path.join(f0, f1), sep=';')
    efluentes = cleaning_data(efluentes, colunas_indesejadas)
    efluentes = checking_geolocation(efluentes, 'Latitude')
    efluentes = checking_geolocation(efluentes, 'Longitude')
