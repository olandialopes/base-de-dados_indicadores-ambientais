import pandas as pd

data = pd.read_csv('4-relatorio-residuos solidos_ibama a partir 2012.csv', delimiter=';')

# Colunas a serem excluidas
variaveis_excluidas = [
    'Código da Categoria', 'Código do Detalhe', 'Detalhe', 'Cód. Resíduo', 'Tipo de Resíduo',
    'Situação Cadastral'
]
# Excluir as variáveis excluidas, cujos nomes estão acima
data = data.drop(columns=variaveis_excluidas, axis=1)

# Contar valores únicos de CNPJ em cada setor
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ do gerador'].nunique()

# Contar quantas vezes cada setor aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('4-contagem_empresas_por_setor.csv', index=False)

# Excluir linhas com pelo menos uma célula vazia em qualquer coluna
data = data.dropna(how='any')

# Contar valores únicos de CNPJ em cada setor
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ do gerador'].nunique()
# Contar quantas vezes cada setor aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('4-contagem_empresas_por_setor2.csv', index=False)

# Excluir linhas com valores zero em qualquer coluna
data = data[~(data == '0').any(axis=1)]

# Contar valores únicos de CNPJ em cada município
contagem_empresas_por_setor = data.groupby('Categoria de Atividade')['CNPJ do gerador'].nunique()
# Contar quantas vezes cada setor aparece
contagem_setor = data['Categoria de Atividade'].value_counts().reset_index()
contagem_setor.columns = ['Categoria de Atividade', 'Quantidade de Empresas']
# Salvar a contagem em um arquivo CSV
contagem_setor.to_csv('4-contagem_empresas_por_setor2.csv', index=False)

# Salvar as alterações de volta no arquivo CSV
data.to_csv('4-result_residuossolidos_a partir2012_setor.csv', index=False)
