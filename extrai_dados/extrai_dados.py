# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Extrai dados processamento PPP e TBC
Description          : Extrai dados do relatório de processamento em PDF do PPP e TBC e realiza o controle de qualidade
Version              : 2.1
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

import os 
import math
import sys
from re import search

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

def convertPDF(file, password =''):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(file, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    text = text.decode("utf-8")
    device.close()
    retstr.close()
    return text

def lerPPP(pasta):
    pdfs = []
    for root, dirs, files in os.walk(pasta):
        if root.split('\\')[-1] == "6_Processamento_PPP" and len(files) > 0:
            for f in files:
                if f.endswith('.pdf') and os.path.isfile(os.path.join(root, f)):
                    pdfs.append(os.path.join(root, f))

    conteudo_list = []
    for pdf in pdfs:
        with open(pdf, "rb") as f:
            ppp = {}
            text = convertPDF(f)
            ppp["orbita"] = text.split('\n')[24].strip().replace(u'RÁPIDA', 'RAPIDA')
            ppp["PPP_N"] = text.split('\n')[64].replace(',', '.').strip()
            ppp["PPP_E"] = text.split('\n')[67].replace(',', '.').strip()
            ppp["PPP_h"] = text.split('\n')[59].replace(',', '.').strip()
            ppp["PPP_H"] = text.split('\n')[50].replace(',', '.').strip()
            ppp["nome_ponto"] = text.split('\n')[3].split(':')[1].strip()
            conteudo_list.append(ppp)
    return conteudo_list

def lerTBC(pasta):
    pdfs = []
    for root, dirs, files in os.walk(pasta):
        if root.split('\\')[-1] == "7_Processamento_TBC_RBMC" and len(files) > 0:
            for f in files:
                if f.endswith('.pdf') and os.path.isfile(os.path.join(root, f)):
                    pdfs.append(os.path.join(root, f))

    conteudo_list = []
    for pdf in pdfs:
        with open(pdf, "rb") as f:
            tbc = {}
            text = convertPDF(f)

            pto_regex = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
            x = [ i for i, pto in enumerate(text.split('\n')) if search(pto_regex, pto)]
            if len(x) > 0:
                x = x[0]
                tbc[u'nome_ponto'] = text.split('\n')[x].strip()
                tbc[u'TBC_E'] = text.split('\n')[x+32].replace(' m', '').replace(',', '.').strip()
                tbc[u'TBC_N'] = text.split('\n')[x+42].replace(' m', '').replace(',', '.').strip()
                tbc[u'TBC_h'] = text.split('\n')[x+52].replace(' m', '').replace(',', '.').strip()
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
        f.write('nome_ponto;ORBITA;PPP_N;PPP_E;PPP_h;PPP_H;TBC_N;TBC_E;TBC_h;Delta_N;Delta_E;Delta_h;Delta_EN\n')
        for pto in merged:
            try:
                pto["Delta_E"] = round(float(pto[u'PPP_E']) - float(pto[u'TBC_E']),3)
                pto["Delta_N"] = round(float(pto[u'PPP_N']) - float(pto[u'TBC_N']),3)
                pto["Delta_h"] = math.fabs(round(float(pto[u'PPP_h']) - float(pto[u'TBC_h']),3))
                pto["Delta_EN"] = round(math.sqrt(pto["Delta_E"]**2 + pto["Delta_N"]**2),3)
                for key in pto:
                    pto[key] = "{0}".format(pto[key]).replace('.', ',')
                f.write('{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12}\n'.format(pto["nome_ponto"], pto["orbita"], pto["PPP_N"], pto["PPP_E"], pto["PPP_h"], pto["PPP_H"], pto["TBC_N"], pto["TBC_E"], pto["TBC_h"], pto["Delta_N"], pto["Delta_E"], pto["Delta_h"], pto["Delta_EN"]))
            except Exception as e:
                print e
                print pto
                erros.append(pto["nome_ponto"])
    return erros


if __name__ == '__builtin__':
    tbc = lerTBC(pasta_dados)
    ppp = lerPPP(pasta_dados)
    criaCSV(csv_file, ppp,tbc)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        tbc = lerTBC(sys.argv[1])
        ppp = lerPPP(sys.argv[1])
        print criaCSV(sys.argv[2], ppp,tbc)
    else:
        print(u'Parametros incorretos!')


