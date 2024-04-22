import pandas as pd
import numpy as np
import os
from Levenshtein import distance

def most_aprox(string, lista):
    distan = [(chosen, distance(string, str(chosen))) for chosen in lista]
    distan.sort(key=lambda x: x[1])
    return distan[0][0]

mun_codes = pd.read_csv('municipios.csv', sep=';')
cod = 'CDIGO DO MUNICPIO - IBGE'
mun = 'MUNICPIO - TOM'

for csv in os.listdir('output'):
    if csv.startswith('POLICY'):
        data = pd.read_csv(f'output/{csv}')
        key = 'Municipio'
        lista = mun_codes[mun].astype(str).tolist()

        for municipio in data[key].astype(str).tolist():

            new_mun = most_aprox(municipio, lista)
            data.loc[data['Municipio'] == municipio, 'Cod Municipio'] = str(mun_codes.loc[mun_codes[mun] == new_mun, cod].values[0])
        
        #data = data.rename(columns={'Municipio': 'Cod Municipio'})
        data.to_csv(f'output/{csv}(name).csv')
        print(f'{csv} completed!')
        

