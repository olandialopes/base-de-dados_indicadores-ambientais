import pandas as pd

# Old code. Check if necessary
# Mapear fatores de conversão para toneladas em notação científica
fatores_conversao = {'kilogramas': 1e-3, 'Tonelada': 1, 'Grama': 1e-6, 'Miligrama': 1e-9}


def convert(data):
    # Converter a coluna "Quantidade" para valores numéricos
    data['Quantidade'] = pd.to_numeric(data['Quantidade'], errors='coerce')

    # Criar uma nova coluna "Quantidade em Toneladas" com os valores convertidos
    data['Quantidade em Toneladas'] = data.apply(lambda row: row['Quantidade'] * fatores_conversao[row['Unidade']], axis=1)

    # Salvar o DataFrame modificado de volta para um arquivo CSV
    data.to_csv('3-nova_base_convertida.csv', index=False)

