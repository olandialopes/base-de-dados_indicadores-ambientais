import pyarrow.parquet as pq
import pandas as pd

def get_unique_cnae():
    # Get uniques CNAE's codes
    ppgu = pd.read_csv('empresas_indicadores.csv')
    ppgu = ppgu[['Codigo_CNAE', 'PP/GU']]
    ppgu = ppgu.drop_duplicates(subset=['Codigo_CNAE'], keep='first').reset_index(drop=True)
    x = [ str(cod)[:5] for cod in ppgu['Codigo_CNAE']]
    ppgu['Codigo_CNAE'] = x
    ppgu = ppgu.drop_duplicates(subset=['Codigo_CNAE'], keep='first').reset_index(drop=True)
    ###############################
    return ppgu


# print(df[df['ano'] > 2002])
# print(len(df['clas_cnae20'].unique()))

def tcfa_value():
    tcfa_arrecadacao = pd.read_csv('arrecadacaoTCFA.csv', sep=';')
    filter1 = [value.replace('.', '') for value in tcfa_arrecadacao['Valor Pago (R$)']]
    filter2 = [float(value.replace(',', '.')) for value in filter1]
    return sum(filter2)

def calcular_total():

    porte = {
             2: {'Pequeno': 0, 'Médio': 0, 'Alto': 50},
             4: {'Pequeno': 112.5, 'Médio': 180, 'Alto': 225},
             6: {'Pequeno': 225, 'Médio': 360, 'Alto': 450},
             9: {'Pequeno': 450, 'Médio': 900, 'Alto': 2250}
            }
    
    dataset = pd.read_csv('clas_cnae20.csv')
    dataset = dataset[dataset['ano'] > 2001]
    dataset = dataset[['tam_estab', 'PP/GU']]
    total = 0

    

    for firm in dataset.values:
        if firm[1] != '-':
            for key in porte.keys():
                if firm[0] and firm[0] <= key:
                    total += porte[key][firm[1]]
                    break
    return total

if __name__ == '__main__':
    print('IBAMA:', tcfa_value())
    print('Calculado:', calcular_total() * 4)
    