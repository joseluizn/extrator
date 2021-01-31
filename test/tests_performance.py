from __future__ import division

import glob
import unittest
from pathlib import Path

import pandas as pd

import core
import helpers

my_path = Path(__file__).parent

data_path = my_path.parent

class SampleTestSTJ(unittest.TestCase):
    """
    Tests results of extracting STJ sample of decisions.
    Compares result with benchmark of the algorithm.
    """
    
    def setUp(self):
        import numpy as np
        # Setting up annotated data
        cit_anot = pd.read_csv(
            (data_path/'data'/'precs_anotacoes.csv').as_posix()
        )

        cit_anot['classe'] = cit_anot.classe.replace(to_replace='sum', value='sum.')

        self.anot_precs = (cit_anot.id_documento + '_' + \
                           cit_anot.classe + '_' + \
                           cit_anot.num_processo.astype(str) + '_' + \
                           cit_anot.corte).values

        # Extracting precs from decisions
        dec_files = glob.glob(
            (data_path/'data'/'anot_empresarial_stj/*').as_posix()
        )
        
        self.extract_precs = list()

        for f in dec_files:
            title = f.split('/')[-1]
            id_ = helpers.parse_title_for_uniqueness(title)
            a = core.submit(open(f, 'r'), id_=id_, default_court='STJ')

            for key, cits in a.items():
                for cit in cits:
                    if cit == "None":
                        continue
                    else:
                        cit = cit.split(' ') #cit is classe, num, soi, tribunal, posfixo
                        
                        self.extract_precs.append('_'.join([title, cit[0], cit[1], cit[3]]))
                    
        self.all_precs = list(set(self.anot_precs) | set(self.extract_precs))
        self.in_anots = np.isin(self.all_precs, self.anot_precs)
        self.in_extract = np.isin(self.all_precs, self.extract_precs)
        self.in_both = self.in_anots & self.in_extract
        
    def test_precision(self):
        """
        Tests algorithm precision against annotations
        """
        precision_benchmark = 385/431
        
        precision = self.in_both.sum()/self.in_extract.sum()
        self.assertGreaterEqual(
            precision,
            precision_benchmark,
            msg="Previous precision was {} tested resulted in {}".format(precision_benchmark, precision)
        )
    
    def test_recall(self):
        """
        Tests algorithm recall against annotations
        """
        recall_benchmark = 385/405
        
        recall = self.in_both.sum()/self.in_anots.sum()
        
        self.assertGreaterEqual(
            recall,
            recall_benchmark,
            msg="Previous recall was {} tested resulted in {}".format(recall_benchmark, recall)
        )    


if __name__ == '__main__':
  unittest.main()
