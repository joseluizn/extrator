#!/usr/bin/env python
# coding=latin-1

import re
import unittest

from extraction import PatternsFactory
import helpers
import core


class CoreTests(unittest.TestCase):
    """
    Tests function from core module.
    """

    def setUp(self):
        self.singula_input = PatternsFactory('STF-STJ')
        self.pluralized = PatternsFactory('STF-STJ', pluralized=True)


    # Reshape function processes list of citations each in a list
    # Each citation refers to a textual citation within the decision
    # each citation is: [ classe, num_list, court, posfixo, position_posfixo]
    # Expected result is a list of citations as they are stored

    def test_reshape_single(self):
        
        _input = [
            ['re', ['123'], 'STF', None, 1]
        ]

        expected = [
            're 123 123 STF N/A',
        ]

        self.assertEqual(core.reshape(_input), expected)


    def test_reshape_multiple(self):
        _input = [
            ['hc', ['5', '7'], 'STJ', 'agr', 2]

        ]

        expected = [
            'hc 5 5 STJ agr',
            'hc 7 7 STJ agr'
        ]

        self.assertEqual(core.reshape(_input), expected)


    # Normalize matches process the textual string of each citation

    def test_normalize_matches_classe_full_multiple(self):

        _input = [
                ['recursos especiais', '5, 6 e 7', 'STJ', 'agr', 2]
        ]

        expect = [
            ('resp', ['5', '6', '7'], 'STJ', 'AgR', 2),
        ]
        
        self.assertEqual(
                core.normalize_matches(_input),
                expect
            )

    def test_normalize_matches_classe_abbrev_single(self):

        _input = [
                ['hc', '123', 'STF', 'agr', 2]
        ]

        expect = [
            ('hc', ['123'], 'STF', 'AgR', 2),
        ]
        
        self.assertEqual(
                core.normalize_matches(_input),
                expect
            )

    def test_normalize_matches_classe_abbrev_single_no_posfixo(self):

        _input = [
                ['hc', '123', 'STF', None, 2]
        ]

        expect = [
            ('hc', ['123'], 'STF', None, 2),
        ]
        
        self.assertEqual(
                core.normalize_matches(_input),
                expect
            )

    # Testing build response. Function deals with regex matches
    # Converts each part of citations regex matches to a tuple of strings

    def test_build_response_stf_class_plural(self):
        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios res 123, 456 e 789 para sanar a omissao. "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        # Using only first item since its where citation in the above text is contained
        matches = re.finditer(self.pluralized.patterns[0], digest)

        _out = core.build_response(matches, default_court='STJ')

        # build response returns set of citations in the document
        expect = set([('res', ' 123, 456 e 789', 'STJ', None, 252)])

        self.assertEqual(
                _out,
                expect
            )

    def test_build_response_ambiguous_class_default_court(self):
        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios hcs 123, 456 e 789 para sanar a omissao. "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        # Using only first item since its where citation in the above text is contained
        matches = re.finditer(self.pluralized.patterns[0], digest)

        _out = core.build_response(matches, default_court='STF')

        # build response returns set of citations in the document
        expect = set([('hcs', ' 123, 456 e 789', 'STF', None, 252)])
    
        self.assertEqual(
                _out,
                expect
            )

    def test_build_response_ambiguous_class_not_default_court(self):
        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios hcs 123, 456 e 789 do stj para sanar a omissao. "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        # Using only first item since its where citation in the above text is contained
        matches = re.finditer(self.pluralized.patterns[0], digest)

        _out = core.build_response(matches, default_court='STF')

        # build response returns set of citations in the document
        expect = set([('hcs', ' 123, 456 e 789', 'STJ', None, 252)])
    
        self.assertEqual(
                _out,
                expect
            )

if __name__ == '__main__':
    unittest.main()
