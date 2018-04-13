# -*- coding: utf-8 -*-

## DSG=group
## local=folder

from zipfile import ZipFile
import os
from re import search




def busca_zip(local_zip,local_destino):

    padrao = "^[\w\.-]+[\w\.-]+@([\w-]+\.)+[\w-]+[\w]+(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]+(.zip)+[\w]+(LIB)+[\w]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+(.zip)*$"
    
    endereco = []
    for root, dirs, files in os.walk(local_destino):

        if root.split(R'/')[-1] == "6_Processamento_PPP":
            caminho = root
            endereco.append(caminho)
        
             
               
               
   
    for root, dirs, files in os.walk(local_zip):
        lista_zip = []
        for f in files:
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                s1 = f.split('_')[1]
                s2 = s1.split('.')[0]
                
                #lista_compara = [x for x in pasta_correta if x not in s2]
                #print (u"A pasta correspondente"+s2+"não esta presente!")
                #if s2 == pasta_correta:
                    
                    #zip = ZipFile(os.path.join(root, f))  
                   # zip.extractall(os.path.join(destino))  

                        

busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

