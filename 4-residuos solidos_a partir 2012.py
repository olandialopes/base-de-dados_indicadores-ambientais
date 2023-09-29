import pandas as pd

data = pd.read_csv('4-relatorio-residuos solidos_ibama a partir 2012.csv', delimiter=';')

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ do gerador'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ da base original: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios da base original: {contagem_valores_municipios}')

# Colunas a serem excluidas
variaveis_excluidas = [
    'Código da Categoria', 'Categoria de Atividade', 'Código do Detalhe', 'Detalhe', 'Cód. Resíduo', 'Tipo de Resíduo',
    'Situação Cadastral'
]
# Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ do gerador'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ depois de excluir qualquer celula em branco: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios depois de excluir qualquer celula em branco:: {contagem_valores_municipios}')

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos na coluna CNPJ (quantidade de CNPJ na base de dados)
contagem_valores_CNPJ = data['CNPJ do gerador'].nunique()
contagem_valores_municipios = data['Município'].nunique()
# Imprimir a contagem de valores únicos
print(f'Quantidade de CNPJ depois de excluir qualquer celula valor igual a zero: {contagem_valores_CNPJ}')
print(f'Quantidade de municipios depois de excluir qualquer celula valor igual a zero: {contagem_valores_municipios}')

# Contar valores únicos na coluna muncípio (quantidade de municípios na base de dados)
contagem_valores_unicos = data['Município'].nunique()

# Salvar as alterações de volta no arquivo CSV
data.to_csv('4-result_residuossolidos_a partir2012.csv', index=False)
