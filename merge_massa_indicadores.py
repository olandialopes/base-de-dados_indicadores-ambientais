import pandas as pd

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
    return data
    

if __name__ == '__main__':
    d = return_massa_cnae_base()
