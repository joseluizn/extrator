#!/usr/bin/env python
# coding=latin-1

import re
import unittest

from extraction import PatternsFactory
import helpers


class HelpersTests(unittest.TestCase):
    """
    tests for helpers functions
    """
    def setUp(self):
        self.sing = PatternsFactory('STF-STJ').patterns[0]
        self.pluralized = PatternsFactory('STF-STJ', pluralized=True).patterns[0]

    def test_normalize_lower_case(self):
        test_case = helpers.normalize('HC 123')

        self.assertEqual(test_case, 'hc 123')

    def test_normalize_upper_case(self):
        case2 = helpers._normalize_case('um', 'upper')

        self.assertEqual(case2, 'UM')

    def test_normalize_encode(self):
        test_encode = helpers.normalize('pãoº maçarico§ tíó')

        self.assertEqual(test_encode, 'pao macarico tio')

    def test_normalize_numero_processo_three(self):

        s = helpers.normalize_numero_processo('1, 23 e 45')

        self.assertEqual(s, ['1', '23', '45'])

    def test_normalize_numero_processo_three_single_digits(self):

        s = helpers.normalize_numero_processo('5, 6 e 7')

        self.assertEqual(s, ['5', '6', '7'])

    def test_normalize_numero_processo_preceeded_by_n(self):
        s_n = helpers.normalize_numero_processo('n. 12 e n. 45')

        self.assertEqual(s_n, ['12', '45'])

    def test_normalize_posfixo_non_existent(self):
        self.assertEqual(
            helpers.normalize_posfixo('teste'),
            None
            )

    def test_normalize_posfixo(self):
        self.assertEqual(
            helpers.normalize_posfixo('ag.rg'),
            'AgR'
            )

    def test_cleaning_and_removal(self):

        ot = helpers.cleaning_and_removal('   remove  n. 100.546')

        self.assertEqual(
            ot,
            ' remove 100546'
        )

    def test_remove_non_relevant_words(self):
        pass
    
    def test_extract_posfixo_after_abrev(self):
        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme o precedente:  o re 98765 ed")

        self.assertEqual(
            helpers.extract_posfixo_if_any(
                re.search(self.sing, digest)
        ),
        'ed'
        )
        

    def test_extract_posfixo_after_full(self):
        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme o precedente:  o re 98765 questao de ordem")

        self.assertEqual(
            helpers.extract_posfixo_if_any(
                re.search(self.sing, digest)
            ),
            'questao de ordem'
        )
        
    def test_extract_posfixo_before_abrev(self):
        """
        This extraction should not happen, thus test looks for expected behaviour
        """

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme o precedente:  o agr re 98765")

        self.assertNotEqual(
            helpers.extract_posfixo_if_any(
                re.search(self.sing, digest)
            ),
            'agr'
        )
        
    def test_extract_posfixo_before_full(self):
        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme o precedente:  liminar re 98765")

        self.assertEqual(
            helpers.extract_posfixo_if_any(
                re.search(self.sing, digest)
            ),
            'liminar'
        )

    def test_infer_court_being_cited_ambiguous_not_default_court_stf(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
          "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
          "recorrido nem opostos embargos declaratorios hcs 123, 456 e 789 do stj para sanar a omissao. "
          "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        # Using only first item since its where citation in the above text is contained
        match = re.search(self.pluralized, digest)

        self.assertEqual(
            helpers.infer_court_being_cited(match),
            'STJ'
            )

if __name__ == '__main__':
  unittest.main()
