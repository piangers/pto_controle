# -*- coding: utf-8 -*-
from zipfile import ZipFile
import zipfile
import os
import os.path
from re import search



def busca(local_destino):

    endereco = []
    for root, dirs, files in os.walk(local_destino):
        for d in dirs:
            if root.split(R'/')[-1] == "6_Processamento_PPP":
                c = root
                endereco.append(c)
    
            
                
               
                



busca(R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')
