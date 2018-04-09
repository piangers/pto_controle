# -*- coding: utf-8 -*-

import zipfile
import os
import os.path
from re import search

def zipa_arquivos(pasta):
    nome_pasta = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
    nome_zip = nome_pasta
    fls = []
    for root, dirs, files in os.walk(pasta):
        for f in files:
            print f
            
             


zipa_arquivos(R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')