# -*- coding: utf-8 -*-

## DSG=group
## local=folder

from zipfile import ZipFile
import os
from re import search



def busca_zip(local_zip,local_destino):

    padrao = "^[\w\.-]+[\w\.-]+@([\w-]+\.)+[\w-]+[\w]+(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]+(.zip)+[\w]+(LIB)+[\w]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+(.zip)*$"
    
    for root, dirs, files in os.walk(local_zip):
        lista_zip = {}
        
        lista_pedaco_zip = []
        for f in files:    
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                
                s1 = f.split('_')[1]
                pedaco_nome_zip = s1.split('.')[0] # s2 recebe o trecho do nome do ZIP selecionado, que será comparado com o do endereço

                caminho = os.path.join(root,f)

                #lista_zip[pedaco_nome_zip] = caminho
                lista_zip[f] = caminho

                #lista_pedaco_zip.append(pedaco_nome_zip) # procurar em todos os elementos nessa lista
                #lista_pedaco_zip.sort()




            endereco = []
            for root2, dirs, files in os.walk(local_destino):

                todos_os_zips = lista_zip.keys()
                
                if root2.split(R'/')[-1] == "6_Processamento_PPP":
                    pai = root2.split(R'/')[-2]

                    for z in todos_os_zips:
                        nome = z.split('_')[1].split('.')[0]
                        
                        if pai == nome:
                            caminho_zip = lista_zip[z]
                            
                            #EXTRAIR AQUI
                   
                            with ZipFile(caminho_zip,"r") as zip_ref:
                                zip_ref.extract(root2)
                        
                    

            
            

                        
busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

