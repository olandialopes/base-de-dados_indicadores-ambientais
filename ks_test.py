import pickle
from scipy.stats import kstest
import pandas as pd

def ktest(base, level=.05):
    inds  = [  'quant_efluentes_liquidos',
               'quant_poluentes_emitidos',
               'quant_residuos_solidos',
               'quant_residuos_solidos',
               'co2_emissions']

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

if __name__ == '__main__':
    nome = 'base_final_isic'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    ktest(b)
    