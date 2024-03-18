
# How to run

0. Base utilizada: `bases_massa_desidentificada`
1. Base gerada: `base_final_isic`

1. Com as bases no diretório original_data e a path indicada na variável **f0**, simplesmente run 

`python read_organize_databases.py`

3. O resultado são as cinco bases limpas, organizadas em um dicionário e uma lista de CNPJs e Anos
3. Isso significa: mantendo as variáveis de interesse, com nomes harmonizados e no formato correto.
4. Na sequência as bases são unidas com os dados de massa salarial por meio do CNPJ em comum. Run

`python merge_massa_indicadaores.py`

5. As tarefas estão presentes, mas a execução é restrita por motivos de sigilo. Com isso, a base da RAIS com a massa 
salarial não consta desse repositório. Será disponibilizada apenas após sua desidentificação.
6. Então a base é ajustada conforme os procedimentos listados na função main

`python base_adjustments_to_analyze.py`

7. Finalmente, após filtros de interesse, os plots e figuras são gerados com 

`python filtros_grafico.py`

8. Alternativamente, é possível também o script `python ecofficiency.py`

7. A versão do python é 3.11 e a do ambiente pandas é 1.5.3. Veja todas as bibliotecas necessárias em `environment.yml`

## Tarefas de forma mais geral

0. Todo: conferir Vitor 2906 com 4 dígitos
1. TODO 1. Separar base emissões em emissões CO2 e energia consumida (análise descritiva)
1. Fazer a análise descritiva (até para gente conhecer a base);
2. Análise geral pela CNAE/indicadores: soma, média e desvio padrão
3. Verificar se houve aumento ou diminuição da quantidade de efluentes líquidos, resíduos, emissões por ano e setor;
4. Qual o CNAE que apresenta maior não conformidade em relação à eficiência do tratamento de efluentes:
5. Eficiência mínima para o tratamento dos efluentes líquidos é de 80%  exigidos pela legislação" (DE VASCONCELOS, 2020)
6. Qual o CNAE que apresenta a melhor eficiência e a pior eficiência do tratamento de efluentes liquidos?
7. Qual a CNAE que apresenta a maior quantidade de resíduos total (classes perigosa e não perigosa);
8. Qual a CNAE que apresenta a maior quantidade de resíduos sólidos da classe perigosa?
9. Qual a CNAE que apresenta a menor quantidade de resíduos sólidos da classe perigosa?
10. Houve um aumento de geração de resíduos da classe perigosa ao longo do tempo ou diminuiu 
(análise por CNA/ano)?

## Avaliar os setores econômicos 

0. Avaliar se o os setores econômicos estão reduzindo a geração de GEE, conforme estabelecido ns compromissos do Brasil com os protocolos e COP referentes ao clima, bem como com a PNMC;
1. Avaliar se os setores estão reduzindo a geração de resíduos conforme estabelecido pela PNRS;
2. Avaliar se os municípios estão atendendo aos padrões estabelecidos pelas Resoluções do Conama em relação aos poluentes atmosféricos;
3. Avaliar se o uso de fonte energética pelos setores está coerente com os compromissos brasileiros
4. Qual o setor econômico apresenta maior poluição para os indicadores selecionados?
5. Qual o setor econômico apresenta a maior geração de renda (massa salarial) e correlação com os indicadores ambientais?
6. Criar gráficos com os dados anteriores e rankings

## Análise por estado, CNAE e indicadores: média e desvio padrão

## Análise por estado, município, CNAE e indicadores: média e desvio padrão
1. Aplicar os indicadores de ECOEFICIÊNCIA (conforme a literatura)
3. Redução dos dados para entrada no modelo principal que é o PolicySpace2 (setores/indicadores)

## Dados base análise indicadores poluição por setores CNAE

Este repositório lê e organiza bases disponíveis no IBAMA:
1. Resíduos sólidos e efluentes líquidos
2. Poluentes e emissões atmosféricas

Organizado por Olandia Lopes, Valdex Santos e Bernardo Alves Furtado

# RESULTADOS DAS BASES

Base 1: 
## Efluentes líquidos

Indicadores: Quantidade gerada de efluentes líquidos por ano e por empresa/setor e eficiência do tratamento;

Base de dados 2: 
## Emissões atmosféricas (toneladas/ano)

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


