# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Prepara estrutura de pastas para o processamento
Description          : Cria pastas e compacta arquivos para iniciar o processamento PPP e TBC
Version              : 0.1
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
import zipfile
import sys

def criaPastas(pasta):
    pto_regex = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
    for root, dirs, files in os.walk(pasta):
        if search(pto_regex, root.split('\\')[-1]):
            if not "6_Processamento_PPP" in dirs:
                os.mkdir(os.path.join(root, "6_Processamento_PPP"))
            if not "7_Processamento_TBC_RBMC" in dirs:
                os.mkdir(os.path.join(root, "7_Processamento_TBC_RBMC"))

def zipaPPP(pasta):
    for root, dirs, files in os.walk(pasta):
        if root.split('\\')[-1] == "2_RINEX":
            pto = root.split('\\')[-2]
            if (pto + ".18n") in files and (pto + ".18o") in files and not (pto + ".zip") in files:
                zf = zipfile.ZipFile(os.path.join(root, pto + ".zip"), "w", zipfile.ZIP_DEFLATED)
                zf.write(os.path.join(root, pto + ".18n"), pto + ".18n")
                zf.write(os.path.join(root, pto + ".18o"), pto + ".18o")

if __name__ == '__builtin__':
    criaPastas(pasta_dados)
    zipaPPP(pasta_dados)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        criaPastas(sys.argv[1])
        zipaPPP(sys.argv[1])
    else:
        print(u'Parametros incorretos!')