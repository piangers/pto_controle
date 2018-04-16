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
            pedaco_nome_endereco = caminho.split(R'/')[-2]  # comparação
            endereco.append(pedaco_nome_endereco)
            endereco.sort()
    #print endereco    # mostar a lista de endereços a ser armazenado os ZIPs   
        
    for root, dirs, files in os.walk(local_zip):
        lista_zip = []
        for f in files:    
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                
                s1 = f.split('_')[1]
                pedaco_nome_zip = s1.split('.')[0] # s2 recebe o trecho do nome do ZIP selecionado, que será comparado com o do endereço
                lista_zip.append(pedaco_nome_zip)
                lista_zip.sort()
        #print lista_zip                        
                # Preciso realizar comparações de listas para definir onde serão realizadas as extrações ZIP.
                # Para cada comparação ele deve buscar o trecho do nome correspondente, no código endereço e comparar
                # com o trecho do nome do zip para extrair na pasta correspondente, caso contrario não. 
                
        listas = [lista_zip, endereco]
        #print listas
        lista_pos = []
        for i in range (len(listas)): # procurar em todas as listas internas
            for j in range (i): # procurar em todos os elementos nessa lista
                if pedaco_nome_endereco in listas[i][j]: # se pedaco_nome_endereco estiver em listas I e em J:
                    lista_pos.append((i, j)) # aqui adicionamos cada índice na lista
        return lista_pos            
        print lista_pos
        
                            
                        

busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

