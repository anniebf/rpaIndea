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
            AND NAF_FILFAZ <> '.' AND NAF_FILFAZ <> ' ' AND NAF_STATUS = '1'
            """)
    try:
        nf_cod, = cursor.fetchone()
    except:
        nf_cod = "000000"
    cursor.close()
    
    return nf_cod

def retorDescfa(nfcod):
    connectionBd = oracledb.connect(user=usernameBd, password=passwordBd, dsn=dsn)
    cursor = connectionBd.cursor()
    cursor.execute(fr"""
            SELECT B1_DESC FROM PROTHEUS11.sb1160 WHERE B1_COD =  '{nfcod}'
            """)
    try:
        b1_cod, = cursor.fetchone()
        b1_cod = re.sub(r'[*"\']', "", b1_cod).strip()
    except:
        b1_cod = "NAO ENCONTRADO"
    cursor.close()
    return b1_cod

def inserirDadosBovideos(cnpj: str, sexo: str, faixet: str, quant: int):
    try:

        connectionBd = oracledb.connect(user=usernameBd, password=passwordBd, dsn=dsn)
        cursor = connectionBd.cursor()
            
        nfcod = retornNFcod(cnpj)
        print(f"------ nfcod: {nfcod} ------")
        descfa = retorDescfa(faixet)
        print(f"------descfa: {descfa} ------")
            
        sql = fr"""INSERT INTO RPA.saldo_animais_indea (data, codfaz, faixet, descfa, sexo, quant) VALUES (SYSDATE,'{nfcod}', '{faixet}', '{descfa}', '{sexo}', {quant})"""
        print(nfcod, faixet, descfa, sexo, quant)
        cursor.execute(sql)
        connectionBd.commit()

        cursor.close()
    except Exception as e:
        
        print(f"Erro ao inserir dados no banco: {e}")
        print(nfcod, faixet, descfa, sexo, quant)
