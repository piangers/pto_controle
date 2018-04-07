# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Organiza arquivos processados do PPP
Description          : Descompacta e distribui na estrutura de pastas os arquivos processados do PPP
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
##pasta_ppp=folder

import os 
from re import search
import zipfile
import sys
import shutil

def organizePPP(estrutura_pasta, pasta_ppp):
    pto_regex = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
    zipfiles = {f.split("_")[1][:-4]: os.path.join(pasta_ppp, f) for f in os.listdir(pasta_ppp) if os.path.isfile(os.path.join(pasta_ppp, f)) and f.endswith('.zip') and len(f.split("_")) == 4 and search(pto_regex,f.split("_")[1][:-4])}
    ptos_estrutura = {}
    for root, dirs, files in os.walk(estrutura_pasta):
        if search(pto_regex, root.split('\\')[-1]):
            if "6_Processamento_PPP" in dirs:
                ptos_estrutura[root.split('\\')[-1]] = os.path.join(root,"6_Processamento_PPP")
            else:
                print u"O padrao de pasta para o ponto {0} esta incorreto (nao possui 6_Processamento_PPP)".format(root.split('\\')[-1])
    
    for zip_pto in zipfiles:
        if zip_pto in ptos_estrutura:
            if len(os.listdir(ptos_estrutura[zip_pto])) == 0:
                zip_ref = zipfile.ZipFile(zipfiles[zip_pto], 'r')
                zip_ref.extractall(ptos_estrutura[zip_pto])
                zip_ref.close()
                if len(os.listdir(ptos_estrutura[zip_pto])) == 1:
                    source = os.path.join(ptos_estrutura[zip_pto], os.listdir(ptos_estrutura[zip_pto])[0])
                    if os.path.isdir(source):
                        for f in os.listdir(source):
                            shutil.move(os.path.join(source,f), ptos_estrutura[zip_pto])
                        shutil.rmtree(source)


    print u"Pontos nao encontrados na estrutura:"
    print repr(list(set(zipfiles.keys()) - set(ptos_estrutura.keys())))
    print "------------------------------------"
    print u"Pontos que nao possuem zip:"
    print repr(list(set(ptos_estrutura.keys()) - set(zipfiles.keys())))

if __name__ == '__builtin__':
    organizePPP(pasta_dados, pasta_ppp)

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        organizePPP(sys.argv[1], sys.argv[2])
    else:
        print(u'Parametros incorretos!')