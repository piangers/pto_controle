# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Atualiza banco de dados de ponto de controle
Description          : Atualiza a situação dos pontos medidos no banco de dados de ponto de controle
Version              : 0.1
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
# DSG=group
# pasta=folder
# servidor=string
# porta=string
# nome_bd=string

import os
import csv


class AutalizaBD():
    def __init__(self, pasta, servidor, porta, nome_bd):
        self.pasta = pasta
        self.servidor = servidor
        self.porta = porta
        self.nome_bd = nome_bd

    def getPontosFromCSV(self):
        pontos = []
        for root, dirs, files in os.walk(self.pasta):
            for f in files:
                if f.endswith(".csv"):
                    with open(join(pasta, files), 'rb') as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        for row in csv_reader:
                            aux = {}
                            if "cod_ponto" in row:
                                aux["cod_ponto"] == row["cod_ponto"]
                            if "operador_levantamento" in row:
                                aux["operador_levantamento"] == row["operador_levantamento"]
                            if "data" in row:
                                aux["data"] == row["data"]
                            pontos.append(aux)
        return pontos

    def atualiza(pontos):
        pass


if __name__ == '__builtin__':

    from qgis.gui import QgsMessageBar
    from qgis.core import QgsMessageLog
    from qgis.utils import iface

    try:
        atualiza_db = AutalizaBD(pasta, servidor, porta, nome_bd)
        pontos = atualiza_db.getPontosFromCSV()
        atualiza_db.atualiza(pontos)
        iface.messageBar().pushMessage(u'Situacao', "Banco de dados atualizado com sucesso",
                                       level=QgsMessageBar.INFO, duration=20)
    except Exception as e:
        QgsMessageLog.logMessage(u"Erro: {0}".format(
            e), tag="Atualiza banco de dados", level=QgsMessageLog.CRITICAL)
        iface.messageBar().pushMessage(u'Situacao', "Erro na execução do script.",
                                       level=QgsMessageBar.CRITICAL, duration=20)


if __name__ == '__main__':
    atualiza_db = AtualizaBD(sys.argv[0], sys.argv[1],
                             sys.argv[2], sys.argv[3])

    pontos = atualiza_db.getPontosFromCSV()
    atualiza_db.atualiza(pontos)
