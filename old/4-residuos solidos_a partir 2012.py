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

valores_unicos = data['Unidade'].unique()

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


# Mapear fatores de conversão para toneladas em notação científica
fatores_conversao = {'quilogramas': 1e-3, 'Litro': 0.001, 'Grama': 1e-6, 'Miligrama': 1e-9, 'Unidade': 1}

# Converter a coluna "Quantidade" para valores numéricos
data['Quantidade Gerada'] = pd.to_numeric(data['Quantidade Gerada'], errors='coerce')

# Criar uma nova coluna "Quantidade em Toneladas" com os valores convertidos
data['Quantidade em Toneladas'] = data.apply(lambda row: row['Quantidade Gerada] * fatores_conversao.get(row['Unidade'], 1), axis=1)


# Salvar o DataFrame modificado de volta para um arquivo CSV
data.to_csv('4-nova_base_convertida.csv', index=False)