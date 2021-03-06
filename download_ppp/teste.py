# -*- coding: utf-8 -*-
import sys
import os
from re import search
from zipfile import ZipFile

def cria_pastas_e_zipa(caminho):
    
    pasta1 = '6_Processamento_PPP'
    pasta2 = '7_processamento_TBC_RBMC'
    padrao = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
    nome_arq = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]\.+[0-9]+[0-9]+(o|n)*$"
    for root, dirs, files in os.walk(caminho):
                              
            # Cria zipfile
        if root.split('/')[-1] == "2_RINEX" and len(files)>0 :
            nome = root.split('/')[-2] + ".zip"
            with ZipFile(os.path.join(root,nome), 'w') as novo_zip:
                for fl in files:
                    if search(nome_arq,fl):
                        novo_zip.write(os.path.join(root,fl),fl)

cria_pastas_e_zipa(R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')            
                   