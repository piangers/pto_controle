# -*- coding: utf-8 -*-
from zipfile import ZipFile
import zipfile
import os
import os.path
from re import search




def busca_zip(local_destino):
    
    for root2, dirs, files in os.walk(local_destino):
        if root2.split('/')[-1] == '6_Processamento_PPP':
            destino = root2.split('/')[-2]
            print destino 


busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')
