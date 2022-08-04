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

        docker run --rm fnndsc/pl-fpmmid fpmmid                     \\
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
                fnndsc/pl-fpmmid fpmmid                        \
                /incoming /outgoing

    DESCRIPTION

        `fpmmid` ...

    ARGS

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
    TITLE                   = 'A ChRIS plugin app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
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
        self.add_argument(  '--inputFile', '-i',
                            dest        = 'inputFile',
                            type        = str,
                            optional    = True,
                            help        = 'name of the input (raw) file to process',
                            default     = "P0997_t1w.nii.gz")

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
        
        
        input_file_path_list = []
        dir_list = []
        for root,dirs,files in os.walk(options.inputdir):
          for file in files:
            if file == options.inputFile:
                dir_list.append(root)
                input_file_path_list.append(os.path.join(root,file))

        for (input_file_path,out_file_path) in zip(input_file_path_list,dir_list):
            out_file_path = out_file_path.replace(options.inputdir, options.outputdir)
            os.makedirs(out_file_path,exist_ok = True)
            logger.info("Running Inference on {}".format(input_file_path))
            pred.main(input_file_path,out_file_path, out_file_path)
            logger.info("Inference finished and stored in {}".format(out_file_path))


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
        
        
def main():
    chris_app = Fpmmid()
    chris_app.launch()

