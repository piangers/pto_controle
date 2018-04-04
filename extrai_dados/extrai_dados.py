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
##pasta_dados=folder
##csv_file=output file

import PyPDF2
import os 
import os.path
import math
import sys
from re import search

def lerPPP(pasta):
    # caminho para os pdfs
    pdfs = []
    for root, dirs, files in os.walk(pasta):
        if root.split('\\')[-1] == "6_Processamento_PPP" and len(files) > 0:
            for f in files:
                if f.endswith('.pdf') and os.path.isfile(os.path.join(root, f)):
                    pdfs.append(os.path.join(root, f))

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
    pdfs = []
    for root, dirs, files in os.walk(pasta):
        if root.split('\\')[-1] == "7_Processamento_TBC_RBMC" and len(files) > 0:
            for f in files:
                if f.endswith('.pdf') and os.path.isfile(os.path.join(root, f)):
                    pdfs.append(os.path.join(root, f))

    conteudo_list = []
    for pdf in pdfs:
        with open(pdf, "rb") as f:
            conteudo = PyPDF2.PdfFileReader(f)    
            tbc = {}
            text = conteudo.getPage(0).extractText()
            pto_regex = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
            x = [ i for i, pto in enumerate(text.split('\n')) if search(pto_regex, pto)][0]
            tbc[u'nome_ponto'] = text.split('\n')[x]
            tbc[u'TBC_E'] = text.split('\n')[x+5].replace(' m', '').replace(',', '.')
            tbc[u'TBC_N'] = text.split('\n')[x+11].replace(' m', '').replace(',', '.')
            tbc[u'TBC_h'] = text.split('\n')[x+17].replace(' m', '').replace(',', '.')
            conteudo_list.append(tbc)
    return conteudo_list

def merge_lists(l1, l2, key):
    merged = {}
    for item in l1+l2:
        if item[key] in merged:
            merged[item[key]].update(item)
        else:
            merged[item[key]] = item
    return [val for (_, val) in merged.items()]

def criaCSV(nome_csv, ppp_list, tbc_list):
    merged = merge_lists(ppp_list, tbc_list, 'nome_ponto')
    erros = []
    with open(nome_csv, 'w') as f:
        f.write('nome_ponto,PPP_N,PPP_E,PPP_h,PPP_H,TBC_N,TBC_E,TBC_h,Delta_N,Delta_E,Delta_h,Delta_EN\n')
        for pto in merged:
            try:
                pto["Delta_E"] = round(float(pto[u'PPP_E']) - float(pto[u'TBC_E']),3)
                pto["Delta_N"] = round(float(pto[u'PPP_N']) - float(pto[u'TBC_N']),3)
                pto["Delta_h"] = round(float(pto[u'PPP_h']) - float(pto[u'TBC_h']),3)
                pto["Delta_EN"] = round(math.sqrt(pto["Delta_E"]**2 + pto["Delta_N"]**2),3)
                f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n'.format(pto["nome_ponto"], pto["PPP_N"], pto["PPP_E"], pto["PPP_h"], pto["PPP_H"], pto["TBC_N"], pto["TBC_E"], pto["TBC_h"], pto["Delta_N"], pto["Delta_E"], pto["Delta_h"], pto["Delta_EN"]))
            except:
                erros.append(pto["nome_ponto"])
    return erros


if __name__ == '__builtin__':
    tbc = lerTBC(pasta_tbc)
    ppp = lerPPP(pasta_ppp)
    criaCSV(csv_file, ppp,tbc)

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        tbc = lerTBC(sys.argv[1])
        ppp = lerPPP(sys.argv[1])
        print criaCSV(sys.argv[2], ppp,tbc)    
    else:
        print(u'Parametros incorretos!')


