# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Extrai dados processamento PPP e TBC
Description          : Extrai dados do relatório de processamento em PDF do PPP e TBC e realiza o controle de qualidade
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
##pasta_ppp=folder
##pasta_tbc=folder
##csv_file=output file

import PyPDF2
import os 
import os.path
import math
import sys

def lerPPP(pasta):
    # caminho para os pdfs
    pdfs = [os.path.join(pasta, nome) for nome in os.listdir(pasta) if nome.endswith('.pdf') and os.path.isfile(os.path.join(pasta, nome))]
    conteudo_list = []
    for pdf in pdfs:
        # abre o arquivo pdf e cria um objeto reader
        with open(pdf, "rb") as f:
            conteudo = PyPDF2.PdfFileReader(f)       # objeto que representa o documento
            # Itera pelas páginas do documento
            ppp = {}
            text = conteudo.getPage(0).extractText() 
            ppp["PPP_N"] = text.split('\n')[74].replace(',', '.')
            ppp["PPP_E"] = text.split('\n')[75].replace(',', '.')
            ppp["PPP_h"] = text.split('\n')[73].replace(',', '.')
            ppp["PPP_H"] = text.split('\n')[108].replace(',', '.')
            ppp["nome_ponto"] = text.split('\n')[2].split(':')[1]
            # fecha o arquivo
            conteudo_list.append(ppp)
    return conteudo_list

def lerTBC(pasta):
    # caminho para os pdfs
    pdfs = [os.path.join(pasta, nome) for nome in os.listdir(pasta) if nome.endswith('.pdf') and os.path.isfile(os.path.join(pasta, nome))]
    conteudo_list = []
    for pdf in pdfs:
        # abre o arquivo pdf e cria um objeto reader
        with open(pdf, "rb") as f:
            conteudo = PyPDF2.PdfFileReader(f)       # objeto que representa o documento
            # Itera pelas páginas do documento
            tbc = {}
            text = conteudo.getPage(0).extractText()
            tbc[u'nome_ponto'] = text.split('\n')[79]
            tbc[u'TBC_E'] = text.split('\n')[84].replace(' m', '').replace(',', '.')
            tbc[u'TBC_N'] = text.split('\n')[90].replace(' m', '').replace(',', '.')
            tbc[u'TBC_h'] = text.split('\n')[96].replace(' m', '').replace(',', '.')
            # fecha o arquivo
            conteudo_list.append(tbc)
    return conteudo_list
    
def criaCSV(nome_csv, ppp_list, tbc_list):
    for ppp in ppp_list:
        for tbc in tbc_list:
            if tbc["nome_ponto"] == ppp["nome_ponto"]:
                ppp[u'TBC_E'] = tbc[u'TBC_E']
                ppp[u'TBC_N'] = tbc[u'TBC_N']
                ppp[u'TBC_h'] = tbc[u'TBC_h']
        
        ppp["Delta_E"] = round(float(ppp[u'PPP_E']) - float(ppp[u'TBC_E']),3)
        ppp["Delta_N"] = round(float(ppp[u'PPP_N']) - float(ppp[u'TBC_N']),3)
        ppp["Delta_h"] = round(float(ppp[u'PPP_h']) - float(ppp[u'TBC_h']),3)
        ppp["Delta_EN"] = round(math.sqrt(ppp["Delta_E"]**2 + ppp["Delta_N"]**2),3)
      
    with open(nome_csv, 'w') as f:
        f.write('nome_ponto,PPP_N,PPP_E,PPP_h,PPP_H,TBC_N,TBC_E,TBC_h,Delta_N,Delta_E,Delta_h,Delta_EN\n')
        for ppp in ppp_list:
            f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n'.format(ppp["nome_ponto"], ppp["PPP_N"], ppp["PPP_E"], ppp["PPP_h"], ppp["PPP_H"], ppp["TBC_N"], ppp["TBC_E"], ppp["TBC_h"], ppp["Delta_N"], ppp["Delta_E"], ppp["Delta_h"], ppp["Delta_EN"]))


if __name__ == '__builtin__':
    tbc = lerTBC(pasta_tbc)
    ppp = lerPPP(pasta_ppp)
    criaCSV(csv_file, ppp,tbc)

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        tbc = lerTBC(sys.argv[1])
        ppp = lerPPP(sys.argv[2])
        criaCSV(sys.argv[3], ppp,tbc)
    else:
        print(u'Parametros incorretos!')


