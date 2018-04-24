# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Deleta arquivos PPP na estrutura de pastas
Description          : Deleta arquivos PPP na estrutura de pastas
Version              : 1.0
copyright            : 1ºCGEO / DSG
reference:
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
##DSG=group
##pasta_dados=folder

import os 
from re import search
import sys
import shutil

def deletaArquivos(pasta):
    for f in os.listdir(pasta):
        file_path = os.path.join(pasta, f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def deletaPPP(estrutura_pasta):
    pto_regex = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
    for root, dirs, files in os.walk(estrutura_pasta):
        if search(pto_regex, root.split('\\')[-1]):
            if "6_Processamento_PPP" in dirs:
                deletaArquivos(os.path.join(root,"6_Processamento_PPP"))
            else:
                print "O padrao de pasta para o ponto {0} esta incorreto (nao possui 6_Processamento_PPP)".format(root.split('\\')[-1])

if __name__ == '__builtin__':
    deletaPPP(pasta_dados)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        deletaPPP(sys.argv[1])
    else:
        print(u'Parametros incorretos!')