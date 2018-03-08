# -*- coding: utf-8 -*-

import unittest
from mock import call, mock
import sys
sys.path.append('../')
from os import sep

from valida_estrutura_pto_controle import EvaluateStructure

class TestEvaluateStructure(unittest.TestCase):
    """
    Test the EvaluateStructure class from the valida_estrutura_pto_controle library
    """
 
    def test_empty_root_folder(self):
        result = EvaluateStructure('test_1','op','2018-01-01').evaluate()
        self.assertEqual(result, [u"A pasta test_1 deveria ter subpastas."])

    def test_no_files_root_folder(self):
            result = EvaluateStructure('test_2','op','2018-01-01').evaluate()
            self.assertItemsEqual(result, [
                u"A pasta test_2 não deve conter arquivos.",
                u"A pasta test_2{0}op_2018-01-01 deveria ter subpastas.".format(sep),
            ])

    @mock.patch.object(EvaluateStructure, 'evaluate_first_level')
    def test_name_root_folder(self, mock_first_level):
        mock_first_level.return_value = []
        result = EvaluateStructure('test_3','op','2018-01-01').evaluate()
        mock_first_level.assert_called_once_with('test_3{0}op_2018-01-01'.format(sep))
        self.assertItemsEqual(result, [
          u"A pasta test_3{0}op_2018-01-02 não segue o padrão de nomenclatura (medidor_YYYY-MM-DD).".format(sep),
          u"A pasta test_3{0}x_2018-01-01 não segue o padrão de nomenclatura (medidor_YYYY-MM-DD).".format(sep),
          ])

    def test_names_first_level(self):
        result = EvaluateStructure('test_4','op','2018-01-01').evaluate()
        self.assertItemsEqual(result, [
          u"A pasta test_4{0}op_2018-01-01{0}RS-HV-01 não segue o padrão de nomenclatura para pontos de controle.".format(sep),
          u"A pasta test_4{0}op_2018-01-01{0}S-HV-15 não segue o padrão de nomenclatura para pontos de controle.".format(sep),
          u"A pasta test_4{0}op_2018-01-01 não deveria conter o arquivo op_2018-01-01.csv.".format(sep),
          u"A pasta test_4{0}op_2018-01-01 deveria conter o arquivo CSV de informações dos pontos do dia (metadados_op_2018-01-01.csv).".format(sep)
        ])
 
    @mock.patch.object(EvaluateStructure, 'evaluate_second_level')
    def test_csv_ptos_first_level(self, mock_second_level):
        mock_second_level.return_value = []
        result = EvaluateStructure('test_5','op','2018-01-01').evaluate()
        mock_second_level.assert_has_calls([
            call('test_5{0}op_2018-01-01{0}RS-HV-1'.format(sep), 'RS-HV-1'), 
            call('test_5{0}op_2018-01-01{0}SC-HV-2'.format(sep), 'SC-HV-2')
            ])
        self.assertItemsEqual(result, [
          u"O ponto SC-HV-2 possui pasta porém não está presente no CSV.",
          u"O ponto RS-HV-2 está presente no CSV porém não possui pasta.",
          u"A coluna teste está presente no CSV porém não é padrão.",
          u"A coluna taxa_gravacao não está presente no CSV.",
          U"Data do ponto RS-HV-2 está incompatível.",
          u"Método de implantação para RS-HV-1 deveria ser PPP.",
          u"Referência de implantação para RS-HV-2 deveria ser -.",
          u"O ponto RS-HV-1 está duplicado no CSV.",
          u"Materializado para RS-HV-1 deveria ser Não."
        ])

    def test_no_files_third_level(self):
        result = EvaluateStructure('test_6','op','2018-01-01').evaluate()
        self.assertItemsEqual(result, [
            u'A pasta test_6{0}op_2018-01-01{0}RS-HV-1{0}x não está prevista para estar na estrutura.'.format(sep),
            u'A pasta test_6{0}op_2018-01-01{0}RS-HV-1 não deve conter arquivos.'.format(sep),
            u'A pasta test_6{0}op_2018-01-01{0}RS-HV-1 deveria ter a subpasta 1_Formato_Nativo.'.format(sep),
            u'A pasta test_6{0}op_2018-01-01{0}RS-HV-1 deveria ter a subpasta 2_RINEX.'.format(sep),
            u'A pasta test_6{0}op_2018-01-01{0}RS-HV-1 deveria ter a subpasta 3_Foto_Rastreio.'.format(sep),
            u'A pasta test_6{0}op_2018-01-01{0}RS-HV-1 deveria ter a subpasta 4_Croqui.'.format(sep)
        ])

    def test_third_level(self):

        result = EvaluateStructure('test_7','op','2018-01-01').evaluate()

        self.assertItemsEqual(result, [
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}4_Croqui deve conter o arquivo RS-HV-1_CROQUI.jpg.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}3_Foto_Rastreio deve conter exatamente 4 fotos.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}2_RINEX deve conter o arquivo RS-HV-1.16o.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}2_RINEX deve conter o arquivo RS-HV-1.16n.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}1_Formato_Nativo deve conter o arquivo RS-HV-1.DAT.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}1_Formato_Nativo deve conter o arquivo RS-HV-1.T01.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}1_Formato_Nativo não deve conter o arquivo x.txt.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}2_RINEX não deve conter o arquivo x.txt.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}3_Foto_Rastreio não deve conter o arquivo x.txt.".format(sep),
            u"A pasta test_7{0}op_2018-01-01{0}RS-HV-1{0}4_Croqui não deve conter o arquivo x.txt.".format(sep)
        ])

    def test_evaluate_all(self):

        result = EvaluateStructure('test_8','op','2018-01-01').evaluate()

        self.assertItemsEqual(result, [])

if __name__ == '__main__':
    unittest.main()