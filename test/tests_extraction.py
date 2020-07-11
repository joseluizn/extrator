#!/usr/bin/env python
# coding=latin-1

import re
import unittest

from extraction import PatternsFactory
from helpers import normalize


class PipelineTests(unittest.TestCase):
    pass


class ExtractionTests(unittest.TestCase):

    def setUp(self):
        self.singular = PatternsFactory('STF-STJ')
        self.pluralized = PatternsFactory('STF-STJ', pluralized=True)


    def test_should_match_single_citation_from_decision_digest(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme os precedentes: agrags 259815, 253614, 216735, 214608, "
                  "216871, 211226, 214360, 238557, 208060, 311483, dentre outros. alem disso, o re 98765 suscita materia "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios res 123, 456, e 789 para sanar a omissao (sumulas 282 e 356). "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.search(self.singular.patterns[0], digest)
        self.assertTrue(match)
        match_string = match.string[match.start():match.end()]
        self.assertEqual(match_string, 're 98765')

    def test_should_match_plural_citation_from_decision_digest(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios res 123, 456 e 789 para sanar a omissao (sumula 282). "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.search(self.pluralized.patterns[0], digest)
        self.assertTrue(match)
        match_string = match.string[match.start():match.end()]
        self.assertEqual(match_string, 'res 123, 456 e 789')

    def test_should_match_plural_citation_avoiding_exponential_backtracking_from_decision_digest(self):
        """
        This case tests reproduces the behaviour which triggered a situation where the extraction
        of a citation could hang for hours and hours. This situation was known as catastrophic backtracking.

        More information - although overly complicated - of this behaviour in: http://www.regular-expressions.info/catastrophic.html
        """

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme os precedentes: agrags 259815, 253614, 216735, 214608, "
                  "216871, 211226, 214360, 238557, 208060, 311483, dentre outros. alem disso, o re 98765 suscita materia ")

        match = re.search(self.pluralized.patterns[0], digest)
        self.assertTrue(match)
        match_string = match.string[match.start():match.end()]
        self.assertEqual(match_string, 'agrags 259815, 253614, 216735, 214608, 216871, 211226, 214360, 238557, 208060, 311483,')

    def test_should_match_multiple_single_citations_from_decision_digest(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios re 132491, para sanar a omissao (sumula 282). "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.finditer(self.singular.patterns[0], digest)
        self.assertTrue(match)

        extracted_citations = []
        for m in match:
            extracted = m.string[m.start():m.end()]
            extracted_citations.append(extracted)

        self.assertItemsEqual(extracted_citations, ['re 132491', 'sumula 282'])

    def test_should_match_multiple_pluralized_citations_from_decision_digest(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme os precedentes: agrags 259815, 253614, 216735, 214608, "
                  "216871, 211226, 214360, 238557, 208060, 311483, dentre outros. alem disso, o re 98765 suscita materia "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios res 123, 456 e 789 para sanar a omissao (sumulas 282 e 356). "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.finditer(self.pluralized.patterns[0], digest)
        self.assertTrue(match)

        extracted_citations = []
        for m in match:
            extracted = m.string[m.start():m.end()]
            extracted_citations.append(extracted)

        self.assertItemsEqual(extracted_citations, ['agrags 259815, 253614, 216735, 214608, 216871, 211226, 214360, 238557, 208060, 311483,',
                                                    'res 123, 456 e 789', 'sumulas 282 e 356'])

    def test_should_not_extract_citation_if_sigla_in_singular_and_there_are_multiple_citations(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios re 123, 456, e 789 para sanar a omissao. "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.search(self.pluralized.patterns[0], digest)
        self.assertFalse(match)

    def test_should_not_extract_citations_if_sigla_in_plural_and_there_is_only_one_citation(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios hcs 789111 para sanar a omissao. "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.search(self.singular.patterns[0], digest)
        self.assertFalse(match)

    def test_should_extract_sumulas_spelled_as_enunciados(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme os enunciados de sumulas nº 5, nº 7 e nº 9 dentre outros."
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.search(self.pluralized.patterns[2], digest)
        self.assertTrue(match)
        match_string = match.string[match.start():match.end()]
        self.assertEqual(match_string, 'enunciados de sumulas nº 5, nº 7 e nº 9')

    def test_should_extract_sumulas_spelled_as_enunciados_followed_by_numbers(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme os enunciados nº 5, nº 7 e nº 9 das sumulas dentre outros."
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.search(self.pluralized.patterns[1], digest)
        self.assertTrue(match)
        match_string = match.string[match.start():match.end()]
        self.assertEqual(match_string, 'enunciados nº 5, nº 7 e nº 9 das sumulas')

    def test_should_match_single_citation_with_characters_before_number(self):

        digest = ("decisao: e meramente processual e infraconstitucional questao relativa a cabimento da acao rescisoria. "
                  "disso resulta a inviabilidade do re conforme os precedentes: agrags 259815, 253614, 216735, 214608, "
                  "216871, 211226, 214360, 238557, 208060, 311483, dentre outros. alem disso, o re n.º 98765 suscita materia "
                  "constitucional (art. 5, ii, art. 7, iii e art. 22, vi, todos da cf/88) que nao foi examinada no acordao "
                  "recorrido nem opostos embargos declaratorios res 123, 456, e 789 para sanar a omissao (sumulas 282 e 356). "
                  "nego seguimento ao agravo (cpc, art. 557). publique-se. brasilia, 22 de agosto de 2003. ministro nelson jobim relator")

        match = re.search(self.singular.patterns[0], normalize(digest))
        self.assertTrue(match)
        match_string = match.string[match.start():match.end()]
        self.assertEqual(match_string, normalize('re n.º 98765'))

        
if __name__ == '__main__':
  unittest.main()
