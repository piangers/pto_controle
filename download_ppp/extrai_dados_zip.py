# -*- coding: utf-8 -*-

## DSG=group
## local=folder

from zipfile import ZipFile
import os
from re import search
from collections import defaultdict


def busca_zip(local_zip,local_destino):

    padrao = "^[\w\.-]+[\w\.-]+@([\w-]+\.)+[\w-]+[\w]+(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]+(.zip)+[\w]+(LIB)+[\w]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+(.zip)*$"
    
    for root, dirs, files in os.walk(local_zip):
        lista_zip = []
        for f in files:    
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                
                s1 = f.split('_')[1]
                pedaco_nome_zip = s1.split('.')[0] # s2 recebe o trecho do nome do ZIP selecionado, que será comparado com o do endereço
                lista_zip.append(pedaco_nome_zip) # procurar em todos os elementos nessa lista
                lista_zip.sort()

            endereco = []
            for root2, dirs, files in os.walk(local_destino):

                if root2.split(R'/')[-1] == "6_Processamento_PPP":
                    caminho = root2
                    pedaco_nome_endereco = caminho.split(R'/')[-2] 
                    endereco.append(pedaco_nome_endereco)
                    endereco.sort()
            listas = [lista_zip,endereco]
            print listas
            keys = defaultdict(list)
            for key, value in enumerate(listas):

            # Adiciona o índice do valor na lista de índices:
                keys[value].append(key)
            # Exibe o resultado:
            for value in keys:
                if len(keys[value]) > 1:
                    print(value, keys[value])
                        
            

                        
busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

