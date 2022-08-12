
from unittest import TestCase
from unittest import mock
from fpmmid.fpmmid import Fpmmid
import os


class FpmmidTests(TestCase):
    """
    Test Fpmmid.
    """
    def setUp(self):
        self.app = Fpmmid()
                

        # you may want to add more of your custom defined optional arguments to test
        self.args = []
        if self.app.TYPE == 'ds':
            self.args.append('/usr/local/src/test_data') # you may want to change this inputdir mock
        self.args.append('/usr/local/src/out_data')  # you may want to change this outputdir mock
        self.args.append('--inputFileFilter')  # you may want to change this inputFileFilter mock
        self.args.append("**/*.nii.gz")
        

    def test_run(self):

        options = self.app.parse_args(self.args)              
            
        self.assertEqual(options.inputdir,'/usr/local/src/test_data' )

