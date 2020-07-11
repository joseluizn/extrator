#!/usr/bin/env python
# coding: utf-8

import os
import re
import json
import time
import argparse
import itertools
import pandas as pd

from copy import deepcopy
from multiprocessing import Pool

import helpers

from log import log
from extraction import PatternsFactory

STF_TERMS = PatternsFactory('STF').normalized
STJ_TERMS = PatternsFactory('STJ').normalized



def run_from(decisions_list, default_court, n_cores=2):
    """
    Execute exctractor on file containing list of elasticserach ids
    """
    pool = Pool(processes=n_cores)
    with open(decisions_list, 'r') as fh:
        decisions = json.load(fh)
        for decision in decisions:
            if os.path.isfile(decision) is False:  # if not dict
                log.error('file %s not found' % decision)
                continue
            pool.apply_async(manage_execution, (decision, default_court), callback=collect)
    pool.close()
    pool.join()

def collect(partial_response):
    """
    Collect function used at callback from apply async.
    Used to collect results while using multiprocess
    """
    D.update(partial_response)


def run(default_court='STF', year=None):
    pool = Pool(processes=6)
    decisions = helpers.query_elasticsearch_for_all_decisions(year)
    for decision in decisions:
        # manage_execution(decision)
        pool.apply_async(manage_execution, (decision, default_court))
    pool.close()
    pool.join()


def build_payload_and_write_to_csv(input_):
    citation_rows  = list()

    for k, v_list in input_.items():
        if v_list == 'None':
            continue
        for cited in v_list:
            if cited == 'None':
                continue
            split = cited.split(' ')
            citation_rows.append(
                (k, split[0], split[1], split[3])
            )
    df_extract = pd.DataFrame(citation_rows, columns=['documento', 'classe', 'num', 'tribunal'])
    df_extract.to_csv('out.csv')

    return True


def manage_execution(decision, default_court='STJ', year=None):
    """
    decision should be file containing decision text
    File name is expected as: YYYYMMDD_CLASSE_NUMERO_ID, where the date refers to decision publishing
    """
    with open(decision, 'r') as d:
        title = os.path.basename(d.name)
        pipeline_id = helpers.parse_title_for_uniqueness(title)
        output = submit(d, id_=pipeline_id, default_court=default_court)
        if output['i_cite']:
            D.update({title: output['i_cite']})
            log.info('precedentes extracted for %s' % title)
    return D


def submit(input_, id_=None, default_court='STJ'):
    """
    Receives the inputed opened file or string containing the term for a unique decision
    and start the pipeline data processing.
    """
    if type(input_) is file:
        raw_text = input_.read()
        input_.close()
    elif type(input_) is str or type(input_) is unicode:
        term = input_
        raw_text = search_decision(term)
    else:
        raw_text = input_['_source']['raw_text']

    normalized_text = normalize(raw_text)
    single_matches = extract_single_citations(normalized_text)
    pluralized_matches = extract_pluralized_citations(normalized_text)
    response = build_response(single_matches, default_court=default_court) | build_response(pluralized_matches, default_court=default_court)

    raw_i_cite = deepcopy(response)  # this information needs to be returned as well
    raw_i_cite = [list(datum) for datum in raw_i_cite]  # set could not be deserialized, so...

    output = normalize_matches(response)
    # trying to make this work
    output = filter_by_valid_citations(output, id_)
    output = reshape(output)

    if not output:
        output = ['None']

    return {'i_cite': output}


def search_decision(term):
    """
    Should return the raw_text of the decision matched by term
    """
    decision = helpers.query_elasticsearch_for_decision(term)
    raw_text = decision['raw_text']

    return raw_text


def normalize(raw_text):
    """
    Should return the normalized text given the raw text
    """
    normalized_text = helpers.normalize(raw_text)
    normalized_text = helpers.cleaning_and_removal(normalized_text)

    return normalized_text


def extract_single_citations(normalized_text):
    """
    Should return a list with regex's match objects from each matched citation
    from the given text
    """
    matches = []
    for extraction_pattern in PatternsFactory('STF-STJ').patterns:
        matches = itertools.chain(
            matches,
            re.finditer(extraction_pattern, normalized_text, flags=re.I|re.U)
            )
        
    return matches


def extract_pluralized_citations(normalized_text):
    """
    Should return a list with regex's match objects from each matched citation
    from the given text
    """
    matches = []
    for extraction_pattern in PatternsFactory('STF-STJ', pluralized=True).patterns:
        matches = itertools.chain(
            matches,
            re.finditer(extraction_pattern, normalized_text, flags=re.I|re.U)
            )
        
    return matches



def build_response(matches, default_court='STJ'):
    """
    Should return a list of n-tuple's containing citations metadata for each
    and every match for the given matches list.

    The metadata should be something like: ('RE', '1234', 'STJ')
    """
    response = []
    for match in matches:
        classe_processual, numero = match.group('classe', 'numero')
        court = helpers.infer_court_being_cited(match, offset=40, default_court=default_court)
        posfixo = helpers.extract_posfixo_if_any(match)
        start_pos = match.start()
        response.append((classe_processual, numero, court, posfixo, start_pos))

    response = set(response)

    return response


def normalize_matches(response):
    """
    Should return the list containing the response n-tuple where each ocurrence
    is normalized. If classe_processual is pluralized, transform back to singular
    and split the respective numero to a list of numero's.
    """
    output = []
    for match in response:

        # DEALING WITH THE PLURALS IF MUST
        classe_processual, numero, court, posfixo, start_pos = match
        if classe_processual in helpers.PLURALS:
            classe_processual = helpers.PLURALS[classe_processual]

        # NORMALIZE NUMERO BEING A PLURAL OR NOT
        numero = helpers.normalize_numero_processo(numero)

        # NORMALIZE THE POSFIXO IF ANY
        posfixo = helpers.normalize_posfixo(posfixo)

        # SETTING THE RIGHT COURT GIVEN A SIMPLE TEST AND NORMALIZE CLASSES IF NEEDED
        if classe_processual in STF_TERMS and\
                classe_processual not in STJ_TERMS:
                    court = 'STF'
                    if classe_processual in helpers.STF_CLASSE_TO_SIGLA:
                        classe_processual = helpers.STF_CLASSE_TO_SIGLA[classe_processual]

        if classe_processual in STJ_TERMS and\
                classe_processual not in STF_TERMS:
                    court = 'STJ'
                    if classe_processual in helpers.STJ_CLASSE_TO_SIGLA:
                        classe_processual = helpers.STJ_CLASSE_TO_SIGLA[classe_processual]

        if classe_processual in STF_TERMS and\
                classe_processual in STJ_TERMS:
                    # if in both of them, use the default court one
                    LOOKUP_CLASSE_TO_SIGLA = helpers.STF_CLASSE_TO_SIGLA if court == 'STF' \
                        else helpers.STJ_CLASSE_TO_SIGLA
                    if classe_processual in LOOKUP_CLASSE_TO_SIGLA:
                        classe_processual = LOOKUP_CLASSE_TO_SIGLA[classe_processual]
                    # if classe_processual in helpers.STF_CLASSE_TO_SIGLA:
                    #     classe_processual = helpers.STF_CLASSE_TO_SIGLA[classe_processual]

        output.append((classe_processual, numero, court, posfixo, start_pos))
    return output


def filter_by_valid_citations(response, id_=None):

    self_classe_processual, self_numero, _ = id_.split(' ')
    self_classe_processual = self_classe_processual.lower()
    self_numero = self_numero.lower()

    output = []
    for match in response:

        classe_processual, numero, court, posfixo, start_pos = match

        if helpers.is_self_citing(match, self_classe_processual, self_numero):
            numero = filter(lambda n: n != self_numero, numero)
            if numero:  # if there are still potential citations (plurals case)
                match = classe_processual, numero, court, posfixo, start_pos
            else:
                continue  # the match is citing the decision itself. discard!

        # match = helpers.validate_by_api_check(match)

        if match:
            output.append(match)

    return output


def reshape(response):
    """
    Alters citation format from a list to string used on database
    """
    output = []
    for match in response:
        classe_processual, numero, court, posfixo, start_pos = match
        if len(numero) == 1:
            # workaround for the missing validation api check
            numero, soi = numero[0], numero[0]
            soi = str(soi)
            posfixo = posfixo or 'N/A'
            match = ' '.join([classe_processual, numero, soi, court, posfixo])
            output.append(match)
        elif len(numero) > 1:
            for n in numero:
                # workaround for the missing validation api check
                n, soi = n, n
                soi = str(soi)
                posfixo = posfixo or 'N/A'
                match = ' '.join([classe_processual, n, soi, court, posfixo])
                output.append(match)
        else:
            continue  # this shouldn't occur, but if do, just ignore (log at least)

    output = list(output)  # removing duplicates

    return output


if __name__ == '__main__':

    import traceback

    cli = argparse.ArgumentParser()

    cli.add_argument('--ids', help='json file with court ids', required=True)
    cli.add_argument(
        '--default_court', '-c',
        help='defines default court for precedent extraction. Should be Court being extracted.',
        required=True
    )
    cli.add_argument('--n_cores', help='number of cores to use', required=False)
    args = cli.parse_args()

    D = {}

    try:
        log.info('Running...')
        
        run_from(args.ids, args.default_court, args.n_cores)

        build_payload_and_write_to_csv(D)
    except Exception as e:
        log.error(e.message)
        log.info('Trying again in a few seconds...')
        time.sleep(3)
        traceback.print_exc()
