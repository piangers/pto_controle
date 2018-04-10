# -*- coding: utf-8 -*-

import zipfile
import os
import os.path
from re import search


def cria_pastas(caminho):
    pasta1 = '6_Processamento_PPP'
    pasta2 = '7_processamento_TBC_RBMC'
    padrao = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"

    for root, dirs, files in os.walk(caminho):
        for d in dirs:
            print d, search(padrao,d)
            if search(padrao,d):
                a = os.path.join(root,pasta1)
                os.mkdir(a)
                b = os.path.join(root,pasta2)
                os.mkdir(b)
                
                

cria_pastas(R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')