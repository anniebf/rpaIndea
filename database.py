import oracledb

from dotenv import load_dotenv
import os
import re

load_dotenv()

usernameBd = os.getenv('usernameBd')
passwordBd = os.getenv('passwordBd')
dsn = os.getenv('dsnhomol')


def retornNFcod(cnpj):
    connectionBd = oracledb.connect(user=usernameBd, password=passwordBd, dsn=dsn)
    cursor = connectionBd.cursor()
    cursor.execute(fr"""
            SELECT NAF_CODIGO FROM PROTHEUS11.NAF160 WHERE NAF_CNPJ = '{cnpj}'
            """)
    nf_cod, = cursor.fetchone()
    cursor.close()
    
    return nf_cod

def retorDescfa(nfcod):
    connectionBd = oracledb.connect(user=usernameBd, password=passwordBd, dsn=dsn)
    cursor = connectionBd.cursor()
    cursor.execute(fr"""
            SELECT B1_DESC FROM PROTHEUS11.sb1160 WHERE B1_COD =  '{nfcod}'
            """)
    b1_cod, = cursor.fetchone()
    b1_cod = re.sub(r'[*"\']', "", b1_cod).strip()
    cursor.close()
    return b1_cod

def inserirDadosBovideos(cnpj: str, sexo: str, faixet: str, quant: int):
    try:
        connectionBd = oracledb.connect(user=usernameBd, password=passwordBd, dsn=dsn)
        cursor = connectionBd.cursor()
            
        nfcod = retornNFcod(cnpj)
        #print(f"------ nfcod: {nfcod} ------")
        descfa = retorDescfa(nfcod)
        #print(f"------descfa: {descfa} ------")
        if nfcod is None or descfa is None:
            print(f"Erro: Não foi possível encontrar nfcod ou descfa para o CNPJ {cnpj}.")
            

        sql = fr"""INSERT INTO RPA.saldo_animais_indea (data, codfaz, faixet, descfa, sexo, quant) VALUES (SYSDATE,'{nfcod}', '{faixet}', '{descfa}', '{sexo}', {quant})"""
        print(nfcod, faixet, descfa, sexo, quant)
        cursor.execute(sql)
        connectionBd.commit()

        cursor.close()
    except Exception as e:
        
        print(f"Erro ao inserir dados no banco: {e}")
        print(nfcod, faixet, descfa, sexo, quant)
