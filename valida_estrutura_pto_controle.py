# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Verifica estrutura Ponto de Controle
Description          : Verifica estrutura de pasta padrão dos pontos de controle (somente PPP)
Version              : 1.3.0
Date                 : 2018-03-08
copyright            : 1ºCGEO / DSG
email                : diniz.felipe@eb.mil.br
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
##pasta=folder
##data=string
##medidores=string
##log=output file

from qgis.gui import QgsMessageBar
from qgis.core import QgsMessageLog
from qgis.utils import iface
from os import listdir, sep
from os.path import isdir, isfile, join
from re import search
import csv

class EvaluateStructure():
    def __init__(self, pasta, medidores, data):
        self.erros = []
        self.pasta = pasta
        self.medidores = medidores.split(";")
        self.data = data

    def evaluate(self):
        self.erros += self.no_files(self.pasta)
        subpastas = [f for f in listdir(self.pasta) if isdir(join(self.pasta, f))]
        if len(subpastas) < 1:
            self.erros.append(u"A pasta {0} deveria ter subpastas.".format(self.pasta))
        else:
            for p in subpastas:
                if p not in [u"{0}_{1}".format(m,self.data) for m in self.medidores]:
                    self.erros.append(u"A pasta {0}{1}{2} não segue o padrão de nomenclatura (medidor_YYYY-MM-DD).".format(self.pasta, sep, p))
                else:
                    erros_pasta = self.evaluate_first_level(join(self.pasta,p))
                    if len(erros_pasta) == 0:
                        self.erros.append(u"A pasta {0}{1}{2} não contém erros.".format(self.pasta, sep, p))
                    else:
                        self.erros += erros_pasta
                self.erros.append(u"\n")

        return self.erros

    def evaluate_first_level(self, pasta):
        erros = []
        ptos_csv = []
        ptos_pasta = []

        medidor, data = pasta.split(sep)[-1].split("_")
        csv_name = "metadados_{0}_{1}.csv".format(medidor,data)
        files = [f for f in listdir(pasta) if isfile(join(pasta, f))]

        if csv_name in files:
            erros += self.evaluate_csv(pasta, csv_name)
            ptos_csv = self.get_ptos_csv(pasta, csv_name)
        else:
            erros.append(u"A pasta {0} deveria conter o arquivo CSV de informações dos pontos do dia (metadados_{1}_{2}.csv).".format(pasta,medidor,data))
        
        if len(set(files).difference([csv_name])) > 0:
            for f in set(files).difference([csv_name]):
                erros.append(u"A pasta {0} não deveria conter o arquivo {1}.".format(pasta, f))

        subpastas = [f for f in listdir(pasta) if isdir(join(pasta, f))]
        if len(subpastas) < 1:
            erros.append(u"A pasta {0} deveria ter subpastas.".format(pasta))
        else:
            for p in subpastas:
                if self.evaluate_nome_ponto(p):
                    ptos_pasta.append(p)
                    erros += self.evaluate_second_level(join(pasta,p), p, data)
                else:
                    erros.append(u"A pasta {0}{1}{2} não segue o padrão de nomenclatura para pontos de controle.".format(pasta, sep, p))
            for pto in set(ptos_pasta).difference(ptos_csv):
                erros.append(u"{0} CSV - O ponto {1} possui pasta porém não está presente no CSV.".format(pasta, pto))
            for pto in set(ptos_csv).difference(ptos_pasta):
                erros.append(u"{0} CSV - O ponto {1} está presente no CSV porém não possui pasta.".format(pasta, pto))
        return erros

    def evaluate_second_level(self, pasta, pto, data):
        erros = []
        erros += self.no_files(pasta)
        subpastas = [f for f in listdir(pasta) if isdir(join(pasta, f))]
        pastas_incorretas = set(subpastas).difference(["1_Formato_Nativo", "2_RINEX", "3_Foto_Rastreio", "4_Croqui", "5_Foto_Auxiliar"])
        pastas_faltando = set(["1_Formato_Nativo", "2_RINEX", "3_Foto_Rastreio", "4_Croqui"]).difference(subpastas)
        pastas_ok = set(["1_Formato_Nativo", "2_RINEX", "3_Foto_Rastreio", "4_Croqui", "5_Foto_Auxiliar"]).intersection(subpastas)

        if len(pastas_incorretas) > 0:
            for p in pastas_incorretas:
                erros.append(u"A pasta {0}{1}{2} não está prevista para estar na estrutura.".format(pasta, sep, p))

        if len(pastas_faltando) > 0:
            for p in pastas_faltando:
                erros.append(u"A pasta {0} deveria ter a subpasta {1}.".format(pasta, p))
                
        if "1_Formato_Nativo" in pastas_ok:
            erros += self.evaluate_formato_nativo(join(pasta,"1_Formato_Nativo"), pto)
        if "2_RINEX" in pastas_ok:
            erros += self.evaluate_rinex(join(pasta,"2_RINEX"), pto, data)
        if "3_Foto_Rastreio" in pastas_ok:
            erros += self.evaluate_foto_rastreio(join(pasta,"3_Foto_Rastreio"), pto)
        if "4_Croqui" in pastas_ok:
            erros += self.evaluate_croqui(join(pasta,"4_Croqui"), pto)
        if "5_Foto_Auxiliar" in pastas_ok:
            erros += self.evaluate_foto_auxiliar(join(pasta,"5_Foto_Auxiliar"), pto)

        return erros

    @staticmethod
    def no_files(pasta):
        erros = []
        files = [f for f in listdir(pasta) if isfile(join(pasta, f) and f != "Thumbs.db")]
        if len(files) > 0:
            for f in files:
                erros.append(u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, f))
        return erros

    @staticmethod
    def no_folders(pasta):
        erros = []
        subpastas = [f for f in listdir(pasta) if isdir(join(pasta, f))]
        if len(subpastas) > 0:
            for s in subpastas:
                erros.append(u"A pasta {0} não deve conter a subpasta {1}.".format(pasta, s))
        return erros

    @staticmethod
    def evaluate_nome_ponto(nome):
        #botar todos os estados
        pto_regex ="^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
        if search(pto_regex, nome):
            return True
        else:
            return False

    @staticmethod
    def evaluate_csv(pasta, nome):
        erros = []

        data = nome[:-4].split("_")[-1]

        columns = ["cod_ponto", "operador_levantamento", "data", "hora_inicio_rastreio", "hora_fim_rastreio",
                    "taxa_gravacao", "altura_antena", "altura_objeto", "nr_serie_antena", "nr_serie_receptor", "tipo_medicao",
                    "materializado", "med_altura", "metodo_implantacao", "referencia_implantacao"]
        ptos = []

        with open(join(pasta,nome), 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            headers = csv_reader.fieldnames
            if len(set(headers).difference(columns)) > 0:
                for col in set(headers).difference(columns):
                    erros.append(u"{0} CSV - A coluna {1} está presente no CSV porém não é padrão.".format(pasta, col))
            if len(set(columns).difference(headers)) > 0:
                for col in set(columns).difference(headers):
                    erros.append(u"{0} CSV - A coluna {1} não está presente no CSV.".format(pasta, col))

            for row in csv_reader:
                if "cod_ponto" in row:
                    if row["cod_ponto"] in ptos:
                        erros.append(u"{0} CSV - O ponto {1} está duplicado no CSV.".format(pasta, row["cod_ponto"]))
                    else:
                        ptos.append(row["cod_ponto"])
                if "data" in row:
                    if row["data"] <> data:
                        erros.append(u"{0} CSV - Data do ponto {1} está incompatível.".format(pasta, row["cod_ponto"]))
                if "materializado" in row:
                    if row["materializado"] <> "Não":
                        erros.append(u"{0} CSV - Materializado para {1} deveria ser Não.".format(pasta, row["cod_ponto"]))
                if "metodo_implantacao" in row:
                    if row["metodo_implantacao"] <> "PPP":
                        erros.append(u"{0} CSV - Método de implantação para {1} deveria ser PPP.".format(pasta, row["cod_ponto"]))
                if "referencia_implantacao" in row:
                    if row["referencia_implantacao"] <> "-":
                        erros.append(u"{0} CSV - Referência de implantação para {1} deveria ser -.".format(pasta, row["cod_ponto"]))
        return erros

    @staticmethod
    def get_ptos_csv(pasta, nome):
        ptos = []
        with open(join(pasta,nome), 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if "cod_ponto" in row:
                    ptos.append(row["cod_ponto"])
        return ptos

    @staticmethod
    def evaluate_formato_nativo(pasta, pto):
        erros = []
        erros += self.no_folders(pasta)
        files = [f.replace(".DAT", ".dat").replace(".T01", ".t01") for f in listdir(pasta) if isfile(join(pasta, f))]
        arquivos_incorretos = set(files).difference(["{0}.dat".format(pto), "{0}.t01".format(pto)])
        arquivos_faltando = set(["{0}.t01".format(pto)]).difference(files)
        if len(arquivos_incorretos) > 0:
            for a in arquivos_incorretos:
                erros.append(u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, a))
        if len(arquivos_faltando) > 0:
            for a in arquivos_faltando:
                erros.append(u"A pasta {0} deve conter o arquivo {1}.".format(pasta, a))
        return erros

    @staticmethod
    def evaluate_rinex(pasta, pto, data):
        erros = []
        erros += self.no_folders(pasta)
        ano = data[2:4]
        files = [f for f in listdir(pasta) if isfile(join(pasta, f))]
        arquivos_incorretos = set(files).difference(["{0}.{1}n".format(pto,ano), "{0}.{1}o".format(pto, ano)])
        arquivos_faltando = set(["{0}.{1}n".format(pto, ano), "{0}.{1}o".format(pto, ano)]).difference(files)
        if len(arquivos_incorretos) > 0:
            for a in arquivos_incorretos:
                erros.append(u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, a))
        if len(arquivos_faltando) > 0:
            for a in arquivos_faltando:
                erros.append(u"A pasta {0} deve conter o arquivo {1}.".format(pasta, a))
        return erros

    @staticmethod
    def evaluate_foto_rastreio(pasta, pto):
        erros = []
        erros += self.no_folders(pasta)
        files = [f for f in listdir(pasta) if isfile(join(pasta, f))]
        fotos_ok = []
        foto_regex = "^{0}_(360|3[0-5][0-9]|[0-2][0-9][0-9])_FOTO.(jpg|JPG)$".format(pto)

        for f in files:
            if search(foto_regex, f):
                fotos_ok.append(f)
            elif f == "Thumbs.db":
                pass
            else:
                erros.append(u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, f))

        if len(fotos_ok) <> 4:
            erros.append(u"A pasta {0} deve conter exatamente 4 fotos.".format(pasta))
            
        return erros


    @staticmethod
    def evaluate_foto_auxiliar(pasta, pto):
        erros = []
        erros += self.no_folders(pasta)
        files = [f for f in listdir(pasta) if isfile(join(pasta, f))]
        fotos_ok = []
        foto_regex = "^{0}_\d+_FOTO_AUX.(jpg|JPG)$".format(pto)

        for f in files:
            if search(foto_regex, f):
                fotos_ok.append(f)
            elif f == "Thumbs.db":
                pass
            else:
                erros.append(u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, f))
            
        return erros

    @staticmethod
    def evaluate_croqui(pasta, pto):
        erros = []
        erros += self.no_folders(pasta)
        files = [f.replace(".JPG", ".jpg") for f in listdir(pasta) if isfile(join(pasta, f))]
        arquivos_incorretos = set(files).difference(["Thumbs.db","{0}_CROQUI.jpg".format(pto)])
        arquivos_faltando = set(["{0}_CROQUI.jpg".format(pto)]).difference(files)
        if len(arquivos_incorretos) > 0:
            for a in arquivos_incorretos:
                erros.append(u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, a))
        if len(arquivos_faltando) > 0:
            for a in arquivos_faltando:
                erros.append(u"A pasta {0} deve conter o arquivo {1}.".format(pasta, a))
        return erros

if __name__ == '__builtin__':
    erros =  EvaluateStructure(pasta,medidores,data).evaluate()

    #log erros
    QgsMessageLog.logMessage(u"Nova execução:", tag="Verifica estrutura", level=QgsMessageLog.INFO)
    for erro in erros:
        QgsMessageLog.logMessage(u"{0}".format(erro), tag="Verifica estrutura", level=QgsMessageLog.INFO)
    
    #save in file
    try:
        with open(log, 'w') as f:
            erros_text = "\n".join(erros).encode('utf-8')
            f.write(erros_text)
            iface.messageBar().pushMessage(u'Situacao', "Arquivo de log gerado em {0}".format(log), level=QgsMessageBar.INFO, duration=20)
    except Exception as e:
        QgsMessageLog.logMessage(u"Erro: {0}".format(e), tag="Verifica estrutura", level=QgsMessageLog.CRITICAL)
        iface.messageBar().pushMessage(u'Situacao', "Erro na execução do script.", level=QgsMessageBar.CRITICAL, duration=20)