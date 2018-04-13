# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Cria PDFs do processamento TBC
Description          : Cria os PDFs a partir do relatório de processamento da linha de base do TBC e distribui na estrutura de pastas
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
import sys
import os
import pdfkit
from BeautifulSoup import BeautifulSoup

def criaPDFs(path_wkthmltopdf, tbc_html_report, output_folder):
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    log = []
    fix_html = tbc_html_report.replace("file:///", "").replace('/', '\\')
    with open(fix_html, "r") as f1:
        main = BeautifulSoup(f1)
        navigation =  main.findAll("frame", {"name": "NavigationFrame"})[0]["src"].replace("FILE://", "")
        with open(navigation, "r") as f2:
            nav = BeautifulSoup(f2)
            ptos_tbc = {}
            for pto in nav.findAll("a")[1:]:
                nome = pto.contents[0].contents[0].split("(")[0].split(" - ")[1].strip()
                ptos_tbc[nome] = {}
                ptos_tbc[nome]["link"] = pto["href"].replace("FILE://", "")
            
            for root, dirs, files in os.walk(output_folder):
                if root.split('\\')[-1] == "7_Processamento_TBC_RBMC":
                    nome_pto = root.split('\\')[-2]
                    if nome_pto in ptos_tbc:
                        ptos_tbc[nome_pto]["path"] = os.path.join(root, "{0}_ACURACIA_PRE.pdf".format(nome_pto))

            for pto in ptos_tbc:
                if "path" in ptos_tbc[pto]:
                    pdfkit.from_url(ptos_tbc[pto]["link"], ptos_tbc[pto]["path"], configuration=config)
                else:
                    log.append("O ponto {0} não está presente na estrutura de pasta definida.".format(pto))
    return log

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        print criaPDFs(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print(u'Parametros incorretos!')