""""
Le as bases limpas.
Analisar os indicadores (README.md)

"""

import read_organize_databases

paths = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}


def emissions_by_municipality(data):
    pass


if __name__ == '__main__':
    # f0 = 'data'
    f0 = '../PS3/ambiental/original_data'
    bases, _ = read_organize_databases.main(paths, read_organize_databases.variaveis_excluidas)
    for each in bases:
        emissions_by_municipality(bases[each])
