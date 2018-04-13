# -*- coding: utf-8 -*-

##DSG=group
##pasta_dados=folder



import sys
import os
from re import search
from zipfile import ZipFile

def cria_pastas_e_zip(caminho):
    
    pasta1 = '6_Processamento_PPP'
    pasta2 = '7_processamento_TBC_RBMC'
    padrao = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
    nome_arq = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]\.+[0-9]+[0-9]+(o|n)*$"
    conteudo=[]
    for root, dirs, files in os.walk(caminho):
        #Cria as pastas
        if search(padrao,root.split("\\")[-1]):
            if dirs.indexOf(pasta1) == -1:
                os.mkdir (os.path.join(root, pasta1))
            if dirs.indexOf(pasta2) == -1:
                os.mkdir (os.path.join(root, pasta2))                             
            # Cria zipfile
            if root.split('/')[-1] == "2_RINEX" and len(files)>0 :
                nome = root.split('/')[-2] + ".zip"
                with ZipFile(os.path.join(root,nome), 'w') as novo_zip:
                    for fl in files:
                        if search(nome_arq,fl):
                            novo_zip.write(os.path.join(root,fl),fl)
    return conteudo                 
                   
if __name__ == '__main__':
    if len(sys.argv)>=1:
        cria_zipa = cria_pastas_e_zip(sys.argv[1])
    else:
        print(u'Parametros incorretos!')