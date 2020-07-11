#!/usr/bin/env python
# coding: utf-8

import re
import json
import unicodedata

from pathlib import Path


MULTIPLE_WHITESPACE_PATTERN = r'\s{2,}'
NUMBER_INDICATOR_REMOVAL_PATTERN = r'\sn2\s|\snos\s|\sndeg\s|\sn\.\s|\sn\s(?=\d)'
THOUSANDS_PUNCTUATION_REMOVAL_PATTERN = r'(?<=\d)\.(?=\d)'

#  NON_RELEVANT_WORDS = ['ed', 'agr', 'agrg', 'edv', 'qo']
#  NON_RELEVANT_WORDS_REMOVAL_PATTERN = '|'.join([r'-%s(?=\s|\d|,|\.)' % w for w in NON_RELEVANT_WORDS])

IS_STJ_PATTERN = r'stj|superior tribunal de justica'
IS_STF_PATTERN = r'stf|supremo tribunal federal'

# STF_CLASSE_TO_SIGLA = pickle.load(open('data/lookup/translator/stf.pkl'))
# STJ_CLASSE_TO_SIGLA = pickle.load(open('data/lookup/translator/stj.pkl'))

# PLURALS = pickle.load(open('data/lookup/plurals/all.pkl'))

my_path = Path(__file__).parent

STF_CLASSE_TO_SIGLA = json.load(open(
    str(my_path/'data/lookup/stf_singular.json'))
)

STJ_CLASSE_TO_SIGLA = json.load(open(
    str(my_path/'data/lookup/stj_singular.json'))
)

PLURALS = json.load(open(
    str(my_path/'data/lookup/pluralizado.json'))
)

def parse_title_for_uniqueness(title):
    title = title.split('_')[1:4]
    title = ' '.join(title)

    return title

def normalize(string):
    string = _normalize_encoding(string)
    string = _normalize_case(string)

    return string

def _normalize_case(string, word_case='lower'):
    return string.upper() if word_case == 'upper' else string.lower()

def _normalize_encoding(string):
    if type(string) is not unicode:
        string = string.decode('utf-8')  # hoping it would be utf-8
    string = unicodedata.normalize('NFD', string)
    string = string.encode('ascii', errors='ignore')

    return string

def normalize_numero_processo(numero):
    if re.search(r',|e', numero):
        numero = re.split(r',\s?|\se\s', numero)
    else:
        numero = [numero]

    # removes n. or similar terms, if present
    numero2 = [re.sub(r'\s?(n[^\s]{0,3})\s?', '', n).replace(' ', '') for n in numero]

    return numero2

def normalize_posfixo(posfixo):
    """
    Function which concentrates the rules for normalization of posfixo's as well
    as the respective translation.
    """

    if not posfixo:
        return None

    normalizer_compendium = {
        'embargo declaratorio': 'ED',
        'ed': 'ED',
        'embargo de declaracao': 'ED',
        'embargos de declaracao': 'ED',
        'agravo': 'AgR',  # checar se isso da conflito com classe agravo do STJ, ignorando por enquanto
        'agravo regimental': 'AgR',
        'agravos regimentais': 'AgR',
        'ag.reg.': 'AgR',
        'ag.reg': 'AgR',
        'agreg': 'AgR',
        'agrg': 'AgR',
        'agr': 'AgR',
        'agr.': 'AgR',
        'ag.rg': 'AgR',
        'embargo de divergencia': 'EDv',
        'embargos de divergencia': 'EDv',
        'edv': 'EDv',
        'embargo infringente': 'EI',
        'embargos infrigentes': 'EI',
        'ei': 'EI',
        'medida cautelar': 'MC',
        'mc': 'MC',
        'questao de ordem': 'QO',
        'qo': 'QO',
        'liminar': 'Liminar',
        'lim': 'Liminar'
    }

    return normalizer_compendium.get(posfixo)

def cleaning_and_removal(string):
    """
    applies all cleaning functions to string.
    Removes multiple whitespace
    Removes number indicator
    removes thousand punctuation
    shifts posfixo position
    """
    string = _remove_multiple_whitespaces(string)
    string = _remove_number_indicator(string)
    string = _remove_thousands_punctuation(string)
    string = _remove_non_relevant_words(string)

    return string

def _remove_multiple_whitespaces(string):
    return re.sub(MULTIPLE_WHITESPACE_PATTERN, ' ', string)

def _remove_number_indicator(string):
    return re.sub(NUMBER_INDICATOR_REMOVAL_PATTERN, ' ', string)

def _remove_thousands_punctuation(string):
    return re.sub(THOUSANDS_PUNCTUATION_REMOVAL_PATTERN, r'', string)

def _remove_non_relevant_words(string):
    """
    not removing per se
    but shift posfixo from after class group to after first group of digits
    """
    posfixos = ['agr', 'ed', 'mc', 'ei', 'lim', 'edv', 'qo']

    return re.sub(r'(-(%s)){1,5}( \d{1,7})' % ('|'.join(posfixos)), '\\3\\1', string)


def extract_posfixo_if_any(match, offset=40):
    """
    Should inspect the surrounding, searching for posfixo's on the citation.
    The posfixo's are divided into shortened (siglas) and longer (estendidas) forms.
    Each form has a search window. The return should be the matched posfixo
    """

    POSFIXOS = {
        'ED': 'Embargo declaratório',
        'AgR': 'Agravo',
        'EDv': 'Embargo de divergência',
        'EI': 'Embargo infringente',
        'MC': 'Medida cautelar',
        'QO': 'Questão de ordem',
        'Lim': 'Liminar'
    }

    content = match.string
    start_pos, end_pos = match.span()

    for sigla, estendida in POSFIXOS.items():

        sigla = normalize(sigla)
        estendida = normalize(estendida)

        is_posfixado_sigla = re.search(sigla, content[end_pos:(end_pos + 5)])
        if is_posfixado_sigla:
            return is_posfixado_sigla.group()
        else:

            is_posfixado_estendida_ahead = re.search(estendida, content[end_pos:(end_pos + offset)])
            if is_posfixado_estendida_ahead:
                return is_posfixado_estendida_ahead.group()

            is_posfixado_estendida_behind = re.search(estendida, content[(start_pos - offset):start_pos])
            if is_posfixado_estendida_behind:
                return is_posfixado_estendida_behind.group()

    return None

def infer_court_being_cited(match, offset=40, default_court='STF'):
    """
    Inspect the match object and try to obtain the context where the match ocurred
    so we could infer which court is the one whose the case being cited is being referred.
    """
    start_pos, end_pos = match.span()
    content = match.string

    if default_court == 'STF':
        exterior_court_pattern = IS_STJ_PATTERN
        exterior_court = 'STJ'
    else:
        exterior_court_pattern = IS_STF_PATTERN
        exterior_court = 'STF'

    is_exterior_court = False
    if re.search(exterior_court_pattern, content[(start_pos - offset):start_pos]) or \
            re.search(exterior_court_pattern, content[end_pos:(end_pos + offset)]):
                is_exterior_court = True

    return default_court if not is_exterior_court else exterior_court

def is_self_citing(match, classe_processual, numero):
    """
    Checks whether process has a citation toward itself.
    """
    match_classe_processual, match_numero = match[:2]
    if classe_processual == match_classe_processual and\
            numero in match_numero:
                return True

    return False
