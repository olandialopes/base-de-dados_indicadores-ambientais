import csv

from sqlalchemy import create_engine
import getpass
import pandas as pd
import pandas.io.sql as psql

cols = ['ano', 'cnpj_cei', 'razao_social', 'natureza_juridica', 'cnpj_raiz',
        'codemun', 'uf_ipea', 'bairro', 'cei_vinc', 'cep', 'clas_cnae10',
        'clas_cnae20', 'clas_cnae95', 'cnpj_contr_assist', 'cnpj_contr_assoc',
        'cnpj_contr_central', 'cnpj_contr_conf', 'cnpj_contr_sind',
        'data_abertura', 'data_baixa', 'data_encerramento', 'email',
        'ind_atividade', 'ind_contr_central', 'ind_estab_sind', 'ind_pat',
        'ind_rais_neg', 'ind_simples', 'endereco', 'qtde_proprietarios',
        'perc_pat_ali', 'perc_pat_ces', 'perc_pat_coz', 'perc_pat_ref',
        'perc_pat_tra', 'qtde_port_defic', 'qtde_vinc_ativos', 'qtde_vinc_clt',
        'qtde_vinc_estat', 'qtde_vinc_pat_ate_5sm', 'qtde_vinc_pat_sup_5sm',
        'regiao_metro', 'sbcl_cnae2x', 'subativ_ibge', 'subs_ibge', 'tam_estab',
        'telefone_contato', 'telefone_estab', 'tipo_estab', 'uf',
        'vl_contr_assist', 'vl_contr_assoc', 'vl_contr_conf', 'vl_contr_sind',
        'vl_rem_estab_01', 'vl_rem_estab_02', 'vl_rem_estab_03',
        'vl_rem_estab_04', 'vl_rem_estab_05', 'vl_rem_estab_06',
        'vl_rem_estab_07', 'vl_rem_estab_08', 'vl_rem_estab_09',
        'vl_rem_estab_10', 'vl_rem_estab_11', 'vl_rem_estab_12', 'port_estab',
        'numero']


def get_connection():
    user = input("User: ")
    password = getpass.getpass(prompt='Password: ', stream=None)
    host = 'psql10-df'
    port = '5432'
    base = 'rais_2019'

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{base}")

    print("Iniciando o processo. Aguarde!")

    return engine


def execute_query(conn, query):
    conn.cursor.execute(query)
    return conn.cursor.fetcahall()


if __name__ == '__main__':
    c = pd.read_csv('cod_cnae_csv')
    cnae_t = list(set([str(cnae)[:5] for cnae in c['cod_cnae']]))
    x = "','".join(cnae_t)
    with get_connection().connect() as connection:
        # q = """
        # CREATE TABLE cnae (
        # cod_cnae VARCHAR(30)
        # );
        #     """
        q1 = """ SELECT DISTINCT clas_cnae20 FROM estabelecimentos.tb_estabelecimentos;"""

        q2 = """        SELECT
                        cnpj_cei,  
                        clas_cnae20,
                        qtde_vinc_ativos,
                        codemun,
                        ano,
                        port_estab,
                        tam_estab,
                        SUM(                      
                        COALESCE(vl_rem_estab_01, 0) + 
                        COALESCE(vl_rem_estab_02, 0) + 
                        COALESCE(vl_rem_estab_03, 0) + 
                        COALESCE(vl_rem_estab_04, 0) + 
                        COALESCE(vl_rem_estab_05, 0) + 
                        COALESCE(vl_rem_estab_06, 0) + 
                        COALESCE(vl_rem_estab_07, 0) + 
                        COALESCE(vl_rem_estab_08, 0) + 
                        COALESCE(vl_rem_estab_09, 0) + 
                        COALESCE(vl_rem_estab_10, 0) + 
                        COALESCE(vl_rem_estab_11, 0) + 
                        COALESCE(vl_rem_estab_12, 0)
                        ) as massa_salarial 
                        FROM estabelecimentos.tb_estabelecimentos
                        WHERE clas_cnae20 IN ('25926','10996','12107','29506','28151','20215','24491','10538','51200','28224','49302','20118','26221','23923','25918','28658','25322','27902','24415','20525','26329','10511','13146','21238','23125','22090','25411','23206','16226','28666','23419','23192','26515','26400','29441','30121','28534','26604','28631','28291','28518','25438','28241','15211','20614','10520','27406','24121','27511','17214','30415','20291','49400','27317','91060','24431','29417','28321','27325','28135','10414','11224','10317','10724','13405','20991','21211','11216','20924','28313','28526','10660','33171','31240','20517','10112','26311','29204','21220','17427','20223','23427','15297','25390','10716','20193','25225','31039','20711','35115','11135','26523','24211','27210','28232','17109','19101','19314','13308','21106','10139','50912','28127','24229','28640','24237','28623','25217','22234','23915','27104','26701','29107','27333','22129','20738','23494','29492','12204','20631','29433','15106','25420','29450','10422','29425','24245','10937','50211','91031','60000','20720','22218','38394','20932','24423','20142','10651','20916','10431','52401','20941','27228','28330','26213','25501','22293','30326','27597','24393','11127','25993','49116','25110','28691','25136','26108','10325','35204','20126','17311','23991','28119','25128','28216','20622','10333','30113','31012','28542','32990','35140','10121','19225','30423','19217','23303','30911','11119','25314','23117','35123','24512','24318','28143','16218','30318','25934','29301','21010','31160','22226')
                        GROUP BY 
                        cnpj_cei, 
                        clas_cnae20,
                        qtde_vinc_ativos,
                        codemun,
                        ano,
                        port_estab,
                        tam_estab;
                """

        #
        # connection.execute(q)
        # connection.commit()

        # with open('./cod_cnae_csv', 'r') as f:
        #     reader = csv.reader(f)
        #     next(reader)
        #     for row in reader:
        #         connection.execute(
        #             "INSERT INTO cnae (cod_cnae) VALUES ('{}')".format(row[0])
        #         )
        # connection.commit()
        # t2 = psql.read_sql(q1, connection)
        d = psql.read_sql(q2, connection)

        filtered_df = d.groupby(['clas_cnae20','ano','codemun', 'port_estab','tam_estab']).filter(lambda x: len(x) >= 3)
        filtered_df = filtered_df.drop(columns=['cnpj_cei'])

        # Timed out tentative
        # d = pd.DataFrame(execute_query(conn=connection, query=q), columns=['cnpj_cei',
        #                                                                    'clas_cnae10',
        #                                                                    'clas_cnae20',
        #                                                                    'qtde_vinc_ativos',
        #                                                                    'codemun',
        #                                                                    'cep',
        #                                                                    'ano',
        #                                                                    'bairro'])
        filtered_df.to_parquet('firms_ambiental')
