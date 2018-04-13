# -*- coding: utf-8 -*-

## DSG=group
## local=folder

from zipfile import ZipFile
import os
from re import search




def busca_zip(local_zip,local_destino):

    padrao = "^[\w\.-]+[\w\.-]+@([\w-]+\.)+[\w-]+[\w]+(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]+(.zip)+[\w]+(LIB)+[\w]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+(.zip)*$"
    
    endereco = []
    for root2, dirs, files in os.walk(local_destino):

        if root2.split(R'/')[-1] == "6_Processamento_PPP":
            caminho = root2
            p = caminho.split(R'/')[-2]  # comparação
            endereco.append(p)
            endereco.sort()
    #print endereco    # mostar a lista de endereços a ser armazenado os ZIPs   
        
    for root, dirs, files in os.walk(local_zip):
        lista_zip = []
        for f in files:
            
        
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                
                s1 = f.split('_')[1]
                s2 = s1.split('.')[0] # s2 recebe o trecho do nome do ZIP selecionado, que será comparado com o do endereço
                lista_zip.append(s2)
                lista_zip.sort()
                            
                # Preciso realizar comparações de listas para definir onde serão realizadas as extrações ZIP.
                # Para cada comparação ele deve buscar o trecho do nome correspondente, no código endereço e comparar
                # com o trecho do nome do zip para extrair na pasta correspondente, caso contrario não. 
                
                
            
                    #zip = ZipFile(os.path.join(root, f))  
                    #zip.extract(endereco) 

                        

busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

