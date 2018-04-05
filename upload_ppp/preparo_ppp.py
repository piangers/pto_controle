# -*- coding: utf-8 -*-
''' ___________________________________________________________________
         
         se_nao_existe_pasta_com_este_nome = not os.path.isdir(pasta1)
         entao_cria = os.mkdir(pasta1)
        if se_nao_existe_pasta_com_este_nome:
        
        else:
             entao_cria 
    ___________________________________________________________________'''


##DSG=group
##pasta=folder
##zip_file=input file

import zipfile
import os
import os.path
from re import search


def cria_pastas(pasta):
    # caminho para os .TXT apenas para referencia
    caminho = '/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04'
    padrao  = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
    x = [ i for i, pto in enumerate(text.split('\n')) if search(padrao, pto)][0]
    
    for root, dirs in os.walk(pasta):
        if root.split('\\')[-1] == nome_pasta:
            
            for arquivo in files:
                if os.path.isdir('6_Processamento_PPP'):
                    pass
                else:
                    os.mkdir('6_Processamento_PPP') # cria pasta caso nao exista
                    print ('Pasta criada com sucesso!')
                
                if os.path.isdir('7_Processamento_TBC_RBMC'):
                    pass
                else:
                    os.mkdir('7_Processamento_TBC_RBMC') # cria pasta caso nao exista
                    print ('Pasta criada com sucesso!')

        '''     if not os.path.exists(caminho):
                os.makedirs(caminho)
                elif not os.path.isdir(caminho):
                raise IOError(caminho + " nao eh um diretorio!")'''
        
    




if __name__ == '__builtin__':
    cria= cria_pastas()
    zipa= zipa_arquivos()
   