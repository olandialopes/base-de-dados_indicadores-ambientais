""""
Lê as bases limpas.
Salvas localmente como bases (formato pickle), após rodar read_organize_databases.py

Analisar os indicadores (README.md)

"""
import pickle

paths = {'efluentes': 'relatorio efluentes liquidos_ibama.csv',
         'poluentes_atm': 'poluentes atmosfericos_dados_ibama.csv',
         'residuos_solidos1': 'residuos solidos_ibama_ate2012.csv',
         'residuos_solidos2': 'residuos solidos_ibama_apartir2012.csv',
         'emissoes': 'relatorio_emissoes atmosfericas ibama.csv'}


def emissions_by_municipality(data):
    pass


def quant_efluentes_cnae(data):
    data['clas_cnae20'] = data['clas_cnae20'].str[:2]
    print(data.groupby(by='clas_cnae20').agg('mean')['quant_efluentes_liquidos'].sort_values(ascending=False).head(20))


if __name__ == '__main__':
    nome = 'bases_massa_desidentificada'
    with open(nome, 'rb') as handler:
        b = pickle.load(handler)

    # Verificar quais colunas a base tem para análise
    for each in b:
        print(b[each].columns)
