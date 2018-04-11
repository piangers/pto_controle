# -*- coding: utf-8 -*-
from zipfile import ZipFile
import zipfile
import os
import os.path
from re import search

def zipa_arquivos(pasta):
    nome_arq = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]\.+[0-9]+[0-9]+(o|n)*$" 
    
    
    for root, dirs, files in os.walk(pasta):
        if root.split('/')[-1] == "2_RINEX" and len(files)>0 :
            nome = root.split('/')[-2]
            with ZipFile(root+'/'+nome+".zip", 'w') as novo_zip:
                for fl in files:
                    if search(nome_arq,fl):
                        #print search(nome_arq,fl)
                        os.path.join(root,fl)
                        novo_zip.write(os.path.join(root,fl),fl)
                        
                        
                
                
                


                
                
                
               
                
zipa_arquivos('/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')