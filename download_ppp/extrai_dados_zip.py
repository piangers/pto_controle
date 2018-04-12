# -*- coding: utf-8 -*-

## DSG=group
## local=folder

from zipfile import ZipFile
import os
from re import search




def busca_zip(local_zip,local_destino):

    padrao = "^[\w\.-]+[\w\.-]+@([\w-]+\.)+[\w-]+[\w]+(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]+(.zip)+[\w]+(LIB)+[\w]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+(.zip)*$"
    
    for root2, dirs, files in os.walk(local_destino):
        for d in dirs:
            if root2.split('/')[-1] == '6_Processamento_PPP':
                pasta_correta = root2.split('/')[-2]
                #print compara
                destino = root2

    for root, dirs, files in os.walk(local_zip):
        for f in files:
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                s1 = f.split('_')[1]
                s1.split('.')[0]
                
                if s1.split('.')[0] == pasta_correta:
                    
                    zip = ZipFile(os.path.join(root, f))  
                    zip.extractall(os.path.join(destino))  

                        

busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

