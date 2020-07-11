# coding: utf-8

import helpers

from copy import deepcopy
from abc import ABCMeta, abstractmethod


class Terms:

    SIGLAS_STF = {'AC', 'ACO', 'ADC', 'ADI', 'ADIn', 'ADO', 'AO', 'AOE', 'AP', 'AR', 'AI', 'ACi',
    'ADPF', 'AImp', 'ARv', 'AS', 'CR', 'Cm', 'CA', 'CC', 'CJ', 'EV', 'EI', 'EL', 'ES',
    'EP', 'Ext', 'HC', 'HD', 'Inq', 'IF', 'MI', 'MS', 'OACO', 'Pet', 'PETA', 'PPE',
    'PA', 'PSV', 'QC', 'Rcl', 'RC', 'RE', 'ARE', 'RMS', 'RHC', 'RHD', 'RMI', 'Rp', 'RvC',
    'SE', 'SEC', 'SL', 'SS', 'STA', 'STP', 'SIRDR'}

    SIGLAS_STJ = {'AC', 'Ag', 'Ag/RE', 'Ag/RHC', 'Ag/RMS', 'AgPres', 'AIA', 'APn', 'AR',
    'AREsp', 'CAt', 'CC', 'Com', 'CR', 'EAg', 'EAREsp', 'EREsp', 'ERMS', 'ExeAR', 'ExeMS',
    'ExImp', 'ExSusp', 'ExVerd', 'HC', 'HD', 'HDE', 'IDC', 'IF', 'IJ', 'Inq', 'MC', 'MI',
    'MISOC', 'MS', 'NC', 'Pet', 'Prc', 'PUIL', 'Rcl', 'REsp', 'RHC', 'RMS', 'RO', 'Rp',
    'RPV', 'RvCr', 'Sd', 'SE', 'SEC', 'SL', 'SLS', 'SS', 'STA', 'TP'}

    CLASSES_PROCESSUAIS_STF = {
    'AÇÃO CAUTELAR',
    'AÇÃO CÍVEL ORIGINÁRIA',
    'AÇÃO DECLARATÓRIA DE CONSTITUCIONALIDADE',
    'AÇÃO DIRETA DE INCONSTITUCIONALIDADE',
    'AÇÃO DIRETA DE INCONSTITUCIONALIDADE POR OMISSÃO',
    'AÇÃO ORIGINÁRIA',
    'AÇÃO ORIGINÁRIA ESPECIAL',
    'AÇÃO PENAL',
    'AÇÃO RESCISÓRIA',
    'AGRAVO DE INSTRUMENTO',
    'APELAÇÃO CÍVEL',
    'ARGÜIÇÃO DE DESCUMPRIMENTO DE PRECEITO FUNDAMENTAL',
    'ARGÜIÇÃO DE IMPEDIMENTO',
    'ARGUIÇÃO DE RELEVÂNCIA',
    'ARGÜIÇÃO DE SUSPEIÇÃO',
    'CARTA ROGATÓRIA',
    'COMUNICAÇÃO',
    'CONFLITO DE ATRIBUIÇÕES',
    'CONFLITO DE COMPETÊNCIA',
    'CONFLITO DE JURISDIÇÃO',
    'EXCEÇÃO DA VERDADE',
    'EXCEÇÃO DE INCOMPETÊNCIA',
    'EXCEÇÃO DE LITISPENDÊNCIA',
    'EXCEÇÃO DE SUSPEIÇÃO',
    'EXECUÇÃO PENAL',
    'EXTRADIÇÃO',
    'HABEAS CORPUS',
    'HABEAS DATA',
    'INQUÉRITO',
    'INTERVENÇÃO FEDERAL',
    'MANDADO DE INJUNÇÃO',
    'MANDADO DE SEGURANÇA',
    'OPOSIÇÃO EM AÇÃO CIVIL ORIGINÁRIA',
    'PETIÇÃO',
    'PETIÇÃO AVULSA',
    'PRISÃO PREVENTIVA PARA EXTRADIÇÃO',
    'PROCESSO ADMINISTRATIVO',
    'PROPOSTA DE SÚMULA VINCULANTE',
    'QUEIXA-CRIME',
    'RECLAMAÇÃO',
    'RECURSO CRIME',
    'RECURSO EXTRAORDINÁRIO',
    'RECURSO EXTRAORDINÁRIO COM AGRAVO',
    'RECURSO ORD. EM MANDADO DE SEGURANÇA',
    'RECURSO ORD. EM HABEAS CORPUS',
    'RECURSO ORD. EM HABEAS DATA',
    'RECURSO ORD. EM MANDADO DE INJUNÇÃO',
    'RECURSO ORDINÁRIO EM MANDADO DE SEGURANÇA',
    'RECURSO ORDINÁRIO EM HABEAS CORPUS',
    'RECURSO ORDINÁRIO EM HABEAS DATA',
    'RECURSO ORDINÁRIO EM MANDADO DE INJUNÇÃO',
    'REPRESENTAÇÃO',
    'REVISÃO CRIMINAL',
    'SENTENÇA ESTRANGEIRA',
    'SENTENÇA ESTRANGEIRA CONTESTADA',
    'SUSPENSÃO DE LIMINAR',
    'SUSPENSÃO DE SEGURANÇA',
    'SUSPENSÃO DE TUTELA ANTECIPADA',
    'SUSPENSÃO DE TUTELA PROVISÓRIA',
    'SUSPENSÃO NACIONAL DO INCIDENTE DE RESOLUÇÃO DE DEMANDAS REPETITIVAS'
    }

    CLASSES_PROCESSUAIS_STJ = {
    'APELAÇÃO CIVEL',
    'AGRAVO',
    'AGRAVO DE INSTRUMENTO',
    'AGRAVO DE INSTRUMENTO PARA STF',
    'AGRAVO DE INSTRUMENTO EM RHC PARA STF',
    'AGRAVO DE INSTRUMENTO EM RMS PARA STF',
    'AGRAVO DE INSTRUMENTO PARA O PRESIDENTE',
    'AÇÃO DE IMPROBIDADE ADMINISTRATIVA',
    'AÇÃO PENAL',
    'AÇÃO RESCISÓRIA',
    'AGRAVO EM RECURSO ESPECIAL',
    'CONFLITO DE ATRIBUIÇÃO',
    'CONFLITO DE COMPETÊNCIA',
    'COMUNICAÇÃO',
    'CARTA ROGATÓRIA',
    'EMBARGOS DE DIVERGÊNCIA EM AGRAVO',
    'EMBARGOS DE DIVERGÊNCIA EM AGRAVO EM RECURSO ESPECIAL',
    'EMBARGOS DE DIVERGÊNCIA EM RESP',
    'EMBARGOS DE DIVERGÊNCIA EM RMS',
    'EXECUÇÃO EM AÇÃO RESCISÓRIA',
    'EXECUÇÃO EM MANDADO DE SEGURANÇA',
    'EXCEÇÃO DE IMPEDIMENTO',
    'EXCEÇÃO DE SUSPEIÇÃO',
    'EXCEÇÃO DA VERDADE',
    'HABEAS CORPUS',
    'HABEAS DATA',
    'HOMOLOGAÇÃO DE DECISÃO ESTRANGEIRA',
    'INCIDENTE DE DESLOCAMENTO DE COMPETÊNCIA',
    'INTERVENÇÃO FEDERAL',
    'INTERPELAÇÃO JUDICIAL',
    'INQUÉRITO',
    'MEDIDA CAUTELAR',
    'MANDADO DE INJUNÇÃO',
    'MEDIDAS INVESTIGATIVAS SOBRE ORGANIZAÇÕES CRIMINOSAS',
    'MANDADO DE SEGURANÇA',
    'NOTÍCIA-CRIME',
    'PETIÇÃO',
    'PRECATÓRIO',
    'PEDIDO DE UNIFORMIZAÇÃO DE INTERPRETAÇÃO DE LEI',
    'RECLAMAÇÃO',
    'RECURSO ESPECIAL',
    'RECURSO EM HABEAS CORPUS',
    'RECURSO EM MANDADO DE SEGURANÇA',
    'RECURSO ORDINÁRIO',
    'RECURSO ORD. EM MANDADO DE SEGURANÇA',
    'RECURSO ORD. EM HABEAS CORPUS',
    'RECURSO ORDINÁRIO EM MANDADO DE SEGURANÇA',
    'RECURSO ORDINÁRIO EM HABEAS CORPUS',
    'REPRESENTAÇÃO',
    'REQUISIÇÃO DE PEQUENO VALOR',
    'REVISÃO CRIMINAL',
    'SINDICÂNCIA',
    'SENTENÇA ESTRANGEIRA',
    'SENTENÇA ESTRANGEIRA CONTESTADA',
    'SUSPENSÃO DE LIMINAR',
    'SUSPENSÃO DE LIMINAR E DE SENTENÇA',
    'SUSPENSÃO DE SEGURANÇA',
    'SUSPENSÃO DE TUTELA ANTECIPADA',
    'PEDIDO DE TUTELA PROVISÓRIA'
    }

    STF_EXTRA = {'SÚMULA', 'SUM.', 'SÚMULA VINCULANTE', 'SUM. VINC.'}
    STJ_EXTRA = {'SÚMULA', 'SUM.'}

    STF = SIGLAS_STF | CLASSES_PROCESSUAIS_STF | STF_EXTRA
    STJ = SIGLAS_STJ | CLASSES_PROCESSUAIS_STJ | STJ_EXTRA
    ALL = STF | STJ

    # PLURALIZAÇÔES

    SIGLAS_STF_PLURALIZED = {'%ss' % t for t in SIGLAS_STF}
    SIGLAS_STJ_PLURALIZED = {'%ss' % t for t in SIGLAS_STJ}

    CLASSES_PROCESSUAIS_STJ_PLURALIZED = {
    'APELAÇÕES CIVEIS',
    'AGRAVOS',
    'AGRAVOS DE INSTRUMENTO',
    'AGRAVOS DE INSTRUMENTO PARA STF',
    'AGRAVOS DE INSTRUMENTO EM RHC PARA STF',
    'AGRAVOS DE INSTRUMENTO EM RMS PARA STF',
    'AGRAVOS DE INSTRUMENTO PARA O PRESIDENTE',
    'AÇÔES DE IMPROBIDADE ADMINISTRATIVA',
    'AÇÕES PENAIS',
    'AÇÕES RESCISÓRIAS',
    'AGRAVOS EM RECURSO ESPECIAL',
    'CONFLITOS DE ATRIBUIÇÃO',
    'CONFLITOS DE COMPETÊNCIA',
    'COMUNICAÇÕES',
    'CARTAS ROGATÓRIAS',
    'EMBARGOS DE DIVERGÊNCIA EM AGRAVO',
    'EMBARGOS DE DIVERGÊNCIA EM AGRAVO EM RECURSO ESPECIAL',
    'EMBARGOS DE DIVERGÊNCIA EM RESP',
    'EMBARGOS DE DIVERGÊNCIA EM RMS',
    'EXECUÇÕES EM AÇÃO RESCISÓRIA',
    'EXECUÇÕES EM MANDADO DE SEGURANÇA',
    'EXCEÇÕES DE IMPEDIMENTO',
    'EXCEÇÕES DE SUSPEIÇÃO',
    'EXCEÇÕES DA VERDADE',
    'HABEAS CORPUS',
    'HABEAS DATA',
    'HOMOLOGAÇÕES DE DECISÃO ESTRANGEIRA',
    'INCIDENTES DE DESLOCAMENTO DE COMPETÊNCIA',
    'INTERVENÇÕES FEDERAIS',
    'INTERPELAÇÕES JUDICIAIS',
    'INQUÉRITOS',
    'MEDIDAS CAUTELARES',
    'MANDADOS DE INJUNÇÃO',
    'MEDIDAS INVESTIGATIVAS SOBRE ORGANIZAÇÕES CRIMINOSAS',
    'MANDADOS DE SEGURANÇA',
    'NOTÍCIAS-CRIME',
    'PETIÇÕES',
    'PRECATÓRIOS',
    'PEDIDOS DE UNIFORMIZAÇÃO DE INTERPRETAÇÃO DE LEI',
    'RECLAMAÇÕES',
    'RECURSOS ESPECIAIS',
    'RECURSOS EM HABEAS CORPUS',
    'RECURSOS EM MANDADO DE SEGURANÇA',
    'RECURSOS ORDINÁRIOS',
    'REPRESENTAÇÕES',
    'REQUISIÇÕES DE PEQUENO VALOR',
    'REVISÕES CRIMINAIS',
    'SINDICÂNCIAS',
    'SENTENÇAS ESTRANGEIRAS',
    'SENTENÇAS ESTRANGEIRAS CONTESTADAS',
    'SUSPENSÕES DE LIMINAR',
    'SUSPENSÕES DE LIMINAR E DE SENTENÇA',
    'SUSPENSÕES DE SEGURANÇA',
    'SUSPENSÕES DE TUTELA ANTECIPADA',
    'PEDIDOS DE TUTELA PROVISÓRIA'
    }

    CLASSES_PROCESSUAIS_STF_PLURALIZED = {
    'AÇÕES CAUTELARES',
    'AÇÕES CÍVEIS ORIGINÁRIAS',
    'AÇÕES DECLARATÓRIAS DE CONSTITUCIONALIDADE',
    'AÇÕES DIRETAS DE INCONSTITUCIONALIDADE',
    'AÇÕES DIRETAS DE INCONSTITUCIONALIDADE POR OMISSÃO',
    'AÇÕES ORIGINÁRIAS',
    'AÇÕES ORIGINÁRIAS ESPECIAIS',
    'AÇÕES PENAIS',
    'AÇÕES RESCISÓRIAS',
    'AGRAVO DE INSTRUMENTO',
    'APELAÇÕES CÍVEIS',
    'ARGÜIÇÕES DE DESCUMPRIMENTO DE PRECEITO FUNDAMENTAL',
    'ARGÜIÇÕES DE IMPEDIMENTO',
    'ARGÜIÇÕES DE RELEVÂNCIA',
    'ARGÜIÇÕES DE SUSPEIÇÃO',
    'CARTAS ROGATÓRIAS',
    'COMUNICAÇÕES',
    'CONFLITOS DE ATRIBUIÇÕES',
    'CONFLITOS DE COMPETÊNCIA',
    'CONFLITOS DE JURISDIÇÃO',
    'EXCEÇÕES DA VERDADE',
    'EXCEÇÕES DE INCOMPETÊNCIA',
    'EXCEÇÕES DE LITISPENDÊNCIA',
    'EXCEÇÕES DE SUSPEIÇÃO',
    'EXECUÇÕES PENAIS',
    'EXTRADIÇÕES',
    'HABEAS CORPUS',
    'HABEAS DATA',
    'INQUÉRITOS',
    'INTERVENÇÕES FEDERAIS',
    'MANDADOS DE INJUNÇÃO',
    'MANDADOS DE SEGURANÇA',
    'OPOSIÇÕES EM AÇÃO CIVIL ORIGINÁRIA',
    'PETIÇÕES',
    'PETIÇÕES AVULSAS',
    'PRISÕES PREVENTIVAS PARA EXTRADIÇÃO',
    'PROCESSOS ADMINISTRATIVOS',
    'PROPOSTAS DE SÚMULA VINCULANTE',
    'QUEIXAS-CRIME',
    'RECLAMAÇÕES',
    'RECURSOS CRIMES',
    'RECURSOS EXTRAORDINÁRIOS',
    'RECURSOS EXTRAORDINÁRIOS COM AGRAVO',
    'RECURSOS ORD. EM MANDADO DE SEGURANÇA',
    'RECURSOS ORDINÁRIOS EM HABEAS CORPUS',
    'RECURSOS ORDINÁRIOS EM HABEAS DATA',
    'RECURSOS ORDINÁRIOS EM MANDADO DE INJUNÇÃO',
    'REPRESENTAÇÕES',
    'REVISÕES CRIMINAIS',
    'SENTENÇAS ESTRANGEIRAS',
    'SENTENÇAS ESTRANGEIRAS CONTESTADAS',
    'SUSPENSÕES DE LIMINAR',
    'SUSPENSÕES DE SEGURANÇA',
    'SUSPENSÕES DE TUTELA ANTECIPADA',
    'SUSPENSÕES DE TUTELA PROVISÓRIA',
    'SUSPENSÕES NACIONAIS DO INCIDENTE DE RESOLUÇÃO DE DEMANDAS REPETITIVAS'
    }

    STF_EXTRA_PLURALIZED = {'SÚMULAS', 'SÚMULAS VINCULANTES', 'AGRAGS'}
    STJ_EXTRA_PLURALIZED = {'SÚMULAS'}

    STF_PLURALIZED = SIGLAS_STF_PLURALIZED | CLASSES_PROCESSUAIS_STF_PLURALIZED | STF_EXTRA_PLURALIZED
    STJ_PLURALIZED = SIGLAS_STJ_PLURALIZED | CLASSES_PROCESSUAIS_STJ_PLURALIZED | STJ_EXTRA_PLURALIZED
    ALL_PLURALIZED = STF_PLURALIZED | STJ_PLURALIZED


class BasePatterns(object):

    __metaclass__ = ABCMeta

    def __init__(self, terms):
        self.raw = deepcopy(terms)
        self.normalized = self._normalize_terms_iter(terms)
        self.patterns = self._generate_patterns()

    def _normalize_terms_iter(self, terms):
        """
        Return the normalized terms by applying the transformation function for each
        individual term.
        """
        return map(lambda t: helpers.normalize(t), terms)

    @abstractmethod
    def _generate_patterns(self):
        """
        Return the list with the patterns created by a(some) generator (in the real sense of the word)
        """
        return


class SingularPatterns(BasePatterns):

    def __init__(self, terms):
        super(SingularPatterns, self).__init__(terms)

    def _generate_patterns(self):
        """
        Return the list with the patterns created by a(some) generator (in the real sense of the word)
        """
        patterns = [r'\b(?P<classe>%s)\.?( n.{0,2})? (?P<numero>[1-9][0-9]{,9})\b' % ('|'.join(self.normalized))]
        
        # These patterns were added to catch different structures used for sumulas. Especially in STJ
        patterns.extend(
            [
                r'(enunciado|verbete)( d.)?(?P<classe>\ssumula( vinculante)?)(\sn.)?(?P<numero>\s[1-9][0-9]{0,3})\b',
                r'(enunciado|verbete)( n.{0,2})?(?P<numero>\s[1-9][0-9]{0,3})\b(\sd.)?(?P<classe>\ssumula( vinculante)?)'
            ]
        )
        return patterns


class PluralizedPatterns(BasePatterns):

    def __init__(self, terms):
        super(PluralizedPatterns, self).__init__(terms)

    def _generate_patterns(self):
        """
        Return the list with the patterns created by a(some) generator (in the real sense of the word)
        """
        patterns = [r'\b(?P<classe>%s)\.?(?P<numero>(( n[^\s]{0,3})?\s?[1-9][0-9]{0,9},?){1,}( e( n[^\s]{0,3})? [1-9][0-9]{0,9}){0,1})' % '|'.join(self.normalized)]
        
        # These patterns were added to catch different structures used for sumulas. Especially in STJ
        patterns.extend(
            [
                r'(enunciados|verbetes)(?P<numero>(( n[^\s]{0,3})?\s?[1-9][0-9]{0,9},?){1,}( e( n[^\s]{0,3})? [1-9][0-9]{0,9}){0,1})(\sd.{0,2})(?P<classe>\ssumula(s?)( vinculante(.?))?)',
                r'(enunciado(s)?|verbete(s)?)(\sd.{0,2})? (?P<classe>sumula(s?)(\svinculante(.?))?)(?P<numero>(( n[^\s]{0,3})?\s?[1-9][0-9]{0,9},?){1,}( e( n[^\s]{0,3})? [1-9][0-9]{0,9}){0,1})'
            ]
        )

        # Joining patterns

        return patterns


class PatternsFactory(object):

    def __init__(self, identifier=None, pluralized=False):
        if not identifier:
            raise ValueError('need some identifier to produce an instance')

        if identifier == 'STF':
            if pluralized:
                instance = PluralizedPatterns(Terms.STF_PLURALIZED)
            else:
                instance = SingularPatterns(Terms.STF)
        elif identifier == 'STJ':
            if pluralized:
                instance = PluralizedPatterns(Terms.STJ_PLURALIZED)
            else:
                instance = SingularPatterns(Terms.STJ)
        elif identifier == 'STF-STJ':
            if pluralized:
                instance = PluralizedPatterns(Terms.ALL_PLURALIZED)
            else:
                instance = SingularPatterns(Terms.ALL)

        self.patterns = instance.patterns
        self.normalized = instance.normalized
