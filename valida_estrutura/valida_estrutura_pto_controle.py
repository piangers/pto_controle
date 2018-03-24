# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Verifica estrutura Ponto de Controle
Description          : Verifica estrutura de pasta padrão dos pontos de controle (somente PPP)
Version              : 1.2.0
Date                 : 2018-03-19
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
##data=string
##medidores=string
##pasta=folder
##log=output file

from os import listdir, sep
from os.path import isdir, isfile, join
from re import search
import csv
from datetime import datetime

class EvaluateStructure():
    def __init__(self, pasta, medidores, data):
        self.erros = []
        self.pasta = pasta
        self.medidores = medidores.split(";")
        self.data = data

        self.rinex_data = {}
        self.csv_data = {}

    def evaluate(self):
        self.erros += self.no_files(self.pasta)
        subpastas = [f for f in listdir(
            self.pasta) if isdir(join(self.pasta, f))]
        if len(subpastas) < 1:
            self.erros.append(
                u"A pasta {0} deveria ter subpastas.".format(self.pasta))
        else:
            for p in subpastas:
                if p not in [u"{0}_{1}".format(m, self.data) for m in self.medidores]:
                    self.erros.append(
                        u"A pasta {0}{1}{2} não segue o padrão de nomenclatura (medidor_YYYY-MM-DD).".format(self.pasta, sep, p))
                else:
                    erros_pasta = self.evaluate_first_level(
                        join(self.pasta, p))

                    erros_pasta += self.compare_csv_rinex(join(self.pasta, p))
                    self.rinex_data = {}
                    self.csv_data = {}

                    if len(erros_pasta) == 0:
                        self.erros.append(
                            u"A pasta {0}{1}{2} não contém erros.".format(self.pasta, sep, p))
                    else:
                        self.erros += erros_pasta
                self.erros.append(u"\n")

        return self.erros

    def evaluate_first_level(self, pasta):
        erros = []
        ptos_csv = []
        ptos_pasta = []

        medidor, data = pasta.split(sep)[-1].split("_")
        csv_name = "metadados_{0}_{1}.csv".format(medidor, data)
        files = [f for f in listdir(pasta) if isfile(join(pasta, f))]

        if csv_name in files:
            erros += self.evaluate_csv(pasta, csv_name)
            csv_data = self.get_data_csv(pasta, csv_name)
            ptos_csv = [x["cod_ponto"] for x in csv_data]
            for pto in csv_data:
                self.csv_data[pto["cod_ponto"]] = pto
        else:
            erros.append(u"A pasta {0} deveria conter o arquivo CSV de informações dos pontos do dia (metadados_{1}_{2}.csv).".format(
                pasta, medidor, data))

        if len(set(files).difference([csv_name])) > 0:
            for f in set(files).difference([csv_name]):
                erros.append(
                    u"A pasta {0} não deveria conter o arquivo {1}.".format(pasta, f))

        subpastas = [f for f in listdir(pasta) if isdir(join(pasta, f))]
        if len(subpastas) < 1:
            erros.append(u"A pasta {0} deveria ter subpastas.".format(pasta))
        else:
            for p in subpastas:
                if self.evaluate_nome_ponto(p):
                    ptos_pasta.append(p)
                    erros += self.evaluate_second_level(
                        join(pasta, p), p, data)
                else:
                    erros.append(
                        u"A pasta {0}{1}{2} não segue o padrão de nomenclatura para pontos de controle.".format(pasta, sep, p))
            for pto in set(ptos_pasta).difference(ptos_csv):
                erros.append(
                    u"{0} CSV - O ponto {1} possui pasta porém não está presente no CSV.".format(pasta, pto))
            for pto in set(ptos_csv).difference(ptos_pasta):
                erros.append(
                    u"{0} CSV - O ponto {1} está presente no CSV porém não possui pasta.".format(pasta, pto))
        return erros

    def evaluate_second_level(self, pasta, pto, data):
        erros = []
        erros += self.no_files(pasta)
        subpastas = [f for f in listdir(pasta) if isdir(join(pasta, f))]
        pastas_incorretas = set(subpastas).difference(
            ["1_Formato_Nativo", "2_RINEX", "3_Foto_Rastreio", "4_Croqui", "5_Foto_Auxiliar"])
        pastas_faltando = set(["1_Formato_Nativo", "2_RINEX",
                               "3_Foto_Rastreio", "4_Croqui"]).difference(subpastas)
        pastas_ok = set(["1_Formato_Nativo", "2_RINEX", "3_Foto_Rastreio",
                         "4_Croqui", "5_Foto_Auxiliar"]).intersection(subpastas)

        if len(pastas_incorretas) > 0:
            for p in pastas_incorretas:
                erros.append(
                    u"A pasta {0}{1}{2} não está prevista para estar na estrutura.".format(pasta, sep, p))

        if len(pastas_faltando) > 0:
            for p in pastas_faltando:
                erros.append(
                    u"A pasta {0} deveria ter a subpasta {1}.".format(pasta, p))

        if "1_Formato_Nativo" in pastas_ok:
            erros += self.evaluate_formato_nativo(
                join(pasta, "1_Formato_Nativo"), pto)
        if "2_RINEX" in pastas_ok:
            erros += self.evaluate_rinex(join(pasta, "2_RINEX"), pto, data)
        if "3_Foto_Rastreio" in pastas_ok:
            erros += self.evaluate_foto_rastreio(
                join(pasta, "3_Foto_Rastreio"), pto)
        if "4_Croqui" in pastas_ok:
            erros += self.evaluate_croqui(join(pasta, "4_Croqui"), pto)
        if "5_Foto_Auxiliar" in pastas_ok:
            erros += self.evaluate_foto_auxiliar(
                join(pasta, "5_Foto_Auxiliar"), pto)

        return erros

    @staticmethod
    def no_files(pasta):
        erros = []
        files = [f for f in listdir(pasta) if isfile(
            join(pasta, f)) and f != "Thumbs.db"]
        if len(files) > 0:
            for f in files:
                erros.append(
                    u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, f))
        return erros

    @staticmethod
    def no_folders(pasta):
        erros = []
        subpastas = [f for f in listdir(pasta) if isdir(join(pasta, f))]
        if len(subpastas) > 0:
            for s in subpastas:
                erros.append(
                    u"A pasta {0} não deve conter a subpasta {1}.".format(pasta, s))
        return erros

    @staticmethod
    def evaluate_nome_ponto(nome):
        # botar todos os estados
        pto_regex = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
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

        with open(join(pasta, nome), 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            headers = csv_reader.fieldnames
            if len(set(headers).difference(columns)) > 0:
                for col in set(headers).difference(columns):
                    erros.append(
                        u"{0} CSV - A coluna {1} está presente no CSV porém não é padrão.".format(pasta, col))
            if len(set(columns).difference(headers)) > 0:
                for col in set(columns).difference(headers):
                    erros.append(
                        u"{0} CSV - A coluna {1} não está presente no CSV.".format(pasta, col))

            for row in csv_reader:
                if "hora_inicio_rastreio" in row and "hora_fim_rastreio" in row:
                    FMT = '%H:%M'
                    tdelta = datetime.strptime(row["hora_fim_rastreio"], FMT) - datetime.strptime(row["hora_inicio_rastreio"], FMT)
                    minutes = tdelta.seconds/60
                    if minutes < 40:
                        erros.append(
                            u"{0} CSV - O ponto {1} está foi medido por menos de 40 min ({2} min).".format(pasta, row["cod_ponto"],minutes))
                if "altura_objeto" in row:
                    if row["altura_objeto"] > 8:
                        erros.append(
                            u"{0} CSV - O ponto {1} está possui altura maior que 8 metros ({2}).".format(pasta, row["cod_ponto"], row["altura_objeto"]))
                if "cod_ponto" in row:
                    if row["cod_ponto"] in ptos:
                        erros.append(
                            u"{0} CSV - O ponto {1} está duplicado no CSV.".format(pasta, row["cod_ponto"]))
                    else:
                        ptos.append(row["cod_ponto"])
                if "data" in row:
                    if row["data"] <> data:
                        erros.append(
                            u"{0} CSV - Data do ponto {1} está incompatível.".format(pasta, row["cod_ponto"]))
                if "materializado" in row:
                    if row["materializado"] <> "Não":
                        erros.append(
                            u"{0} CSV - Materializado para {1} deveria ser Não.".format(pasta, row["cod_ponto"]))
                if "metodo_implantacao" in row:
                    if row["metodo_implantacao"] <> "PPP":
                        erros.append(
                            u"{0} CSV - Método de implantação para {1} deveria ser PPP.".format(pasta, row["cod_ponto"]))
                if "referencia_implantacao" in row:
                    if row["referencia_implantacao"] <> "-":
                        erros.append(
                            u"{0} CSV - Referência de implantação para {1} deveria ser -.".format(pasta, row["cod_ponto"]))
        return erros

    @staticmethod
    def get_data_csv(pasta, nome):
        ptos = []
        with open(join(pasta, nome), 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                aux = {}
                if "cod_ponto" in row:
                    aux["cod_ponto"] = row["cod_ponto"]
                if "nr_serie_receptor" in row:
                    aux["nr_serie_receptor"] = row["nr_serie_receptor"]
                if "nr_serie_antena" in row:
                    aux["nr_serie_antena"] = row["nr_serie_antena"]
                if "hora_inicio_rastreio" in row:
                    aux["hora_inicio_rastreio"] = row["hora_inicio_rastreio"]
                if "hora_fim_rastreio" in row:
                    aux["hora_fim_rastreio"] = row["hora_fim_rastreio"]
                if "data" in row:
                    aux["data"] = row["data"]
                if "altura_antena" in row:
                    aux["altura_antena"] = row["altura_antena"]
                ptos.append(aux)
        return ptos

    @staticmethod
    def get_rinex_data(pasta, nome):
        rinex_info = {}
        with open(join(pasta, nome), 'rb') as rinex_file:
            lines = rinex_file.readlines()
            rinex_info["cod_ponto_1"] = lines[3].split(' ')[0]
            rinex_info["cod_ponto_2"] = lines[4].split(' ')[0]
            rinex_info["nr_serie_receptor"] = lines[6].split(' ')[0]
            rinex_info["nr_serie_antena"] = lines[7].split(' ')[0]
            rinex_info["altura_antena"] = lines[9].strip().split(' ')[0]
            aux_inicio = [x for x in lines[12].strip().split(' ') if x]
            rinex_info["data_rastreio_1"] = "{0}-{1}-{2}".format(aux_inicio[0],aux_inicio[1],aux_inicio[2])
            rinex_info["hora_inicio_rastreio"] = "{0}:{1}".format(aux_inicio[3],aux_inicio[4])
            aux_fim = [x for x in lines[13].strip().split(' ') if x]
            rinex_info["data_rastreio_2"] = "{0}-{1}-{2}".format(aux_inicio[0],aux_inicio[1],aux_inicio[2])
            rinex_info["hora_fim_rastreio"] = "{0}:{1}".format(aux_inicio[3],aux_inicio[4])

        return rinex_info

    def evaluate_formato_nativo(self, pasta, pto):
        erros = []
        erros += self.no_folders(pasta)
        files = [f.replace(".DAT", ".dat").replace(".T01", ".t01")
                 for f in listdir(pasta) if isfile(join(pasta, f))]
        arquivos_incorretos = set(files).difference(
            ["{0}.dat".format(pto), "{0}.t01".format(pto)])
        arquivos_faltando = set(["{0}.t01".format(pto)]).difference(files)
        if len(arquivos_incorretos) > 0:
            for a in arquivos_incorretos:
                erros.append(
                    u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, a))
        if len(arquivos_faltando) > 0:
            for a in arquivos_faltando:
                erros.append(
                    u"A pasta {0} deve conter o arquivo {1}.".format(pasta, a))
        return erros

    def evaluate_rinex(self, pasta, pto, data):
        erros = []
        erros += self.no_folders(pasta)
        ano = data[2:4]
        files = [f for f in listdir(pasta) if isfile(join(pasta, f))]
        arquivos_incorretos = set(files).difference(
            ["{0}.{1}n".format(pto, ano), "{0}.{1}o".format(pto, ano)])
        arquivos_faltando = set(
            ["{0}.{1}n".format(pto, ano), "{0}.{1}o".format(pto, ano)]).difference(files)
        if len(arquivos_incorretos) > 0:
            for a in arquivos_incorretos:
                erros.append(
                    u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, a))
        if len(arquivos_faltando) > 0:
            for a in arquivos_faltando:
                erros.append(
                    u"A pasta {0} deve conter o arquivo {1}.".format(pasta, a))
        else:
            rinex_name = "{0}.{1}o".format(pto, ano)
            self.rinex_data[pto] = self.get_rinex_data(pasta,rinex_name)

        return erros

    def evaluate_foto_rastreio(self, pasta, pto):
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
                erros.append(
                    u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, f))

        if len(fotos_ok) <> 4:
            erros.append(
                u"A pasta {0} deve conter exatamente 4 fotos.".format(pasta))

        return erros

    def evaluate_foto_auxiliar(self, pasta, pto):
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
                erros.append(
                    u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, f))

        return erros

    def evaluate_croqui(self, pasta, pto):
        erros = []
        erros += self.no_folders(pasta)
        files = [f.replace(".JPG", ".jpg")
                 for f in listdir(pasta) if isfile(join(pasta, f))]
        arquivos_incorretos = set(files).difference(
            ["Thumbs.db", "{0}_CROQUI.jpg".format(pto)])
        arquivos_faltando = set(
            ["{0}_CROQUI.jpg".format(pto)]).difference(files)
        if len(arquivos_incorretos) > 0:
            for a in arquivos_incorretos:
                erros.append(
                    u"A pasta {0} não deve conter o arquivo {1}.".format(pasta, a))
        if len(arquivos_faltando) > 0:
            for a in arquivos_faltando:
                erros.append(
                    u"A pasta {0} deve conter o arquivo {1}.".format(pasta, a))
        return erros

    def compare_csv_rinex(self, pasta):
        erros = []
        for key in self.csv_data:
            if key in self.rinex_data:
                if self.rinex_data[key]["cod_ponto_1"] != self.csv_data[key]["cod_ponto"] or self.rinex_data[key]["cod_ponto_2"] != self.csv_data[key]["cod_ponto"]:
                    erros.append(u"{0}: O arquivo RINEX do ponto {1} está com o nome de ponto incorreto.".format(pasta, self.csv_data[key]["cod_ponto"]))
                
                if self.rinex_data[key]["nr_serie_receptor"] != self.csv_data[key]["nr_serie_receptor"]:
                    erros.append(u"{0}: O arquivo RINEX do ponto {1} está com o nr serie receptor diferente do CSV.".format(pasta, self.csv_data[key]["cod_ponto"]))
                
                if self.rinex_data[key]["nr_serie_antena"] != self.csv_data[key]["nr_serie_antena"]:
                    erros.append(u"{0}: O arquivo RINEX do ponto {1} está com o nr serie antena diferente do CSV.".format(pasta, self.csv_data[key]["cod_ponto"]))
                
                if self.rinex_data[key]["hora_inicio_rastreio"] != self.csv_data[key]["hora_inicio_rastreio"]:
                    erros.append(u"{0}: O arquivo RINEX do ponto {1} está com a hora inicio rastreio diferente do CSV.".format(pasta, self.csv_data[key]["cod_ponto"]))
                
                if self.rinex_data[key]["hora_fim_rastreio"] != self.csv_data[key]["hora_fim_rastreio"]:
                    erros.append(u"{0}: O arquivo RINEX do ponto {1} está com a hora fim rastreio diferente do CSV.".format(pasta, self.csv_data[key]["cod_ponto"]))
                
                if self.rinex_data[key]["data_rastreio_1"] != self.csv_data[key]["data"] or self.rinex_data[key]["data_rastreio_2"] != self.csv_data[key]["data"]:
                    erros.append(u"{0}: O arquivo RINEX do ponto {1} está com a data de rastreio incorreta.".format(pasta, self.csv_data[key]["cod_ponto"]))
                
                if self.rinex_data[key]["altura_antena"] != self.csv_data[key]["altura_antena"]:
                    erros.append(u"{0}: O arquivo RINEX do ponto {1} está com a altura antena diferente do CSV.".format(pasta, self.csv_data[key]["cod_ponto"]))
            else:
                erros.append(u"{0}: Não foi encontrado informações do RINEX compatíveis com o ponto {1}.".format(pasta, self.csv_data[key]["cod_ponto"]))                
        return erros

if __name__ == '__builtin__':

    from qgis.gui import QgsMessageBar
    from qgis.core import QgsMessageLog
    from qgis.utils import iface
    erros = EvaluateStructure(pasta, medidores, data).evaluate()

    # log erros
    QgsMessageLog.logMessage(
        u"Nova execução:", tag="Verifica estrutura", level=QgsMessageLog.INFO)
    for erro in erros:
        QgsMessageLog.logMessage(u"{0}".format(
            erro), tag="Verifica estrutura", level=QgsMessageLog.INFO)

    #save in file
    try:
        with open(log, 'w') as f:
            erros_text = "\n".join(erros).encode('utf-8')
            f.write(erros_text)
            iface.messageBar().pushMessage(u'Situacao', "Arquivo de log gerado em {0}".format(
                log), level=QgsMessageBar.INFO, duration=20)
    except Exception as e:
        QgsMessageLog.logMessage(u"Erro: {0}".format(
            e), tag="Verifica estrutura", level=QgsMessageLog.CRITICAL)
        iface.messageBar().pushMessage(u'Situacao', "Erro na execução do script.",
                                       level=QgsMessageBar.CRITICAL, duration=20)


if __name__ == '__main__':
    erros = EvaluateStructure(sys.argv[0], sys.argv[1], sys.argv[2]).evaluate()
    print(erros)
