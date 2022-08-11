
from unittest import TestCase
from unittest import mock
from fpmmid.fpmmid import Fpmmid


class FpmmidTests(TestCase):
    """
    Test Fpmmid.
    """
    def setUp(self):
        self.app = Fpmmid()

    def test_run(self):
        """
        Test the run code.
        """
        args = []
        if self.app.TYPE == 'ds':
            args.append('/usr/local/src/test_data') # you may want to change this inputdir mock
        args.append('outputdir')  # you may want to change this outputdir mock
        args.append('--inputFileFilter')  # you may want to change this outputdir mock
        args.append("**/*.nii.gz")

        # you may want to add more of your custom defined optional arguments to test
        # your app with
        # eg.
        # args.append('--custom-int')
        # args.append(10)

        options = self.app.parse_args(args)
        self.app.run(options)

        # write your own assertions
        results = self.assertEqual(options.outputdir, 'outputdir')
        print(results)
