#
# fpmmid ds ChRIS plugin app
#
# (c) 2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os
from chrisapp.base import ChrisApp
from scripts.run import pred
from .mapper import PathMapper
from pathlib import Path
import logging
import sys



Gstr_title = r"""
  __                           _     _ 
 / _|                         (_)   | |
| |_ _ __  _ __ ___  _ __ ___  _  __| |
|  _| '_ \| '_ ` _ \| '_ ` _ \| |/ _` |
| | | |_) | | | | | | | | | | | | (_| |
|_| | .__/|_| |_| |_|_| |_| |_|_|\__,_|
    | |                                
    |_|                                
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       fpmmid

    SYNOPSIS

        docker run --rm fnndsc/pl-fpmmid fpmmid                         \\
            [-i/--inputFileFilter <inputFileFilter>]                    \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-fpmmid fpmmid                             \
                /incoming /outgoing

    DESCRIPTION

        `fpmmid` is a chris plugin wrapped around FPMMID

    ARGS
        [-i/--inputFileFilter <inputFileFilter>]
        A glob pattern string, default is "**/*.nii.gz",
        representing the input T1 weighted brain image
        

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
"""


class Fpmmid(ChrisApp):
    """
    An app to ...
    """
    PACKAGE                 = __package__
    TITLE                   = 'A ChRIS plugin app wrapper around FPMMID'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 4000  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument(  '--inputFileFilter','-i',
                            dest         = 'inputFileFilter',
                            type         = str,
                            optional     = True,
                            help         = 'Input file filter',
                            default      = '**/*.nii.gz')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        
         # Output the space of CLI
        d_options = vars(options)
        for k,v in d_options.items():
            print("%20s: %-40s" % (k, v))
        print("")
        
        
        # Set up the logger
        logger = logging.getLogger("eval")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        
        mapper = PathMapper.file_mapper(
                input_dir=Path(options.inputdir),
                output_dir=Path(options.outputdir),
                glob=options.inputFileFilter,
            )

        for input_file_path,out_file_path in mapper:
            os.makedirs(out_file_path.parent, exist_ok=True)
            logger.info("Running Inference on {}".format(input_file_path))
            pred.main(str(input_file_path), str(out_file_path.parent), str( out_file_path.parent))
            logger.info("Inference finished and stored in {}".format(out_file_path.parent))


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
        
        
def main():
    chris_app = Fpmmid()
    chris_app.launch()

