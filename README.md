
# TODO

# 1. Separar a base de poluentes por tipo de Poluente (análise descritiva/texto para discussão)
# 2. Separar base emissões em emissões CO2 e energia consumida (análise descritiva)

# TODO forma mais geral

# 0. Todo: conferir Vitor 2906 com 4 dígitos
# 1. Fazer a análise descritiva (até para gente conhecer a base);
- verificar se houve aumento ou diminuição da quantidade de efluentes liquidos, resíduos, emissões por ano e setor)
- Qual o cnae que apresenta maior não conformidade em relação a eficiência do tratamento de efluentes:
- Devem ser seguidos de tratamento complementar, pois sua eficiência em média não ultrapassa 60% na 
- remoção de carga orgânica, bem abaixo dos 80% mínimos exigidos pela legislação" (DE VASCONCELOS, 2020)
- Qual o cnae que apresenta a melhor eficiencia e a pior eficiência do tratamento de efluentes liquidos;
- Qual a cnae que apresenta a maior quantidade de resíduos solidos da classe perigosa?
- Qual a cnae que apresenta a maior quantidade de resíduos solidos da classe perigosa?
- Houve um aumento de geração de residuos da classe perigosa ao longo do tempo ou diminuiu?
- poluidoras (por poluente, por município, por ano, etc.). 
-  CNAE por poluente, municipio, etc.
- 
# 2. Aplicar os indicadores de ECOEFICIÊNCIA (conforme a literatura)
# 3. Redução dos dados para entrada no modelo principal que é o PolicySpace2 (setores/indicadores)



# Dados base análise indicadores poluição por setores CNAE

Este repositório lê e organiza bases disponíveis no IBAMA:
1. Resíduos sólidos e efluentes líquidos
2. Poluentes e emissões atmosféricas

Organizado por Olandia Lopes, Valdex Santos e Bernardo Alves Furtado

## How to run

1. Com as bases no diretório original_data e a path indicada na variável **f0**, simplesmente run `python read_organize_databases.py`
2. Os resultados são as cinco bases limpas, organizadas em um dicionário e uma lista de CNPJs e Anos
3. Isso significa: mantendo as variáveis de interesse, com nomes harmonizaods e no formato correto.
4. Na sequência as bases são unidas com os dados de massa salarial por meio do CNPJ em comum
5. Por motivos de sigilo, a base da RAIS com a massa salarial não consta desse repositório
6. Será disponibilizada apenas após as análises feitos e sua desindetificação
7. A versão do python é 3.9 e a do ambiente pandas é 1.5.3;


# RESULTADOS DAS BASES

Base 1: 
## Efluentes líquidos

Indicadores: Quantidade gerada de efluentes líquidos por ano e por empresa/setor e eficiência do tratamento;

Base de dados 2: 
## Emissões atmosféricas

- Indicadores:

·         Quantidade gerada de poluentes atmosféricos (Material particulado - MP) por ano e por empresa/setor;

·         Quantidade gerada de poluentes atmosféricos (Monóxido de carbono – CO)) por ano e por empresa/setor

·         Quantidade gerada de poluentes atmosféricos (Óxidos de nitrogênio – NOx) por ano e por empresa/setor

·         Quantidade gerada de poluentes atmosféricos (Óxidos de enxofre – SOx) por ano e por empresa/setor


Base de dados 3 e 4
## Resíduos sólidos 

- Indicador:

·         Quantidade gerada de resíduos sólidos por classe (perigoso e não perigoso) por ano e por empresa/setor;


Base de dados 5: 
## Emissões atmosféricas 

- Indicadores

·         Quantidade consumida de energia por tipo de fonte energética (eletricidade – rede pública; biomassa-lenha; turfa; óleo diesel, entre outros ) por ano e por empresa/setor;

·         Quantidade de emissões de CO2 por ano, por empresa/setor.

## Sources:
Os dados utilizados foram coletados da base de dados do IBAMA disponíveis no Relatório Anual de Atividades Potencialmente Poluidoras e Utilizadoras de Recursos Ambientais – RAPP, conforme abaixo:

1. Efluentes liquidos: https://dadosabertos.ibama.gov.br/pt_PT/dataset/efluentes-liquidos
2. Emissões de Poluentes atmosféricos: https://dadosabertos.ibama.gov.br/pt_PT/dataset/emissoes-de-poluentes-atmosfericos
3. Resíduos sólidos anterior a 2012: https://dadosabertos.ibama.gov.br/pt_PT/dataset/residuos-solidos-gerador-anterior-a-2012
4. Resíduos sólidos a partir de 2012: https://dadosabertos.ibama.gov.br/pt_PT/dataset/residuos-solidos-gerador-a-partir-de-2012
5. Emissões atmosféricas: https://dadosabertos.ibama.gov.br/pt_PT/dataset/fontes-energeticas


