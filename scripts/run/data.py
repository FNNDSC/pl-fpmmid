"""
This module prepares a 3D MRI scan data volume with T1w channel
for multi-class gmentation using FPMMID model
"""

import os
import logging
import numpy as np
from .modules import vol_reader as vlr

class Subject:
    """
    This class provides the data preparations step for MRI scan volumes
    """
    def __init__(self, name):
        self.name = name
        self.num_channels = 1
        self.num_classes = 4

    def prep_data(self, input_path, root_dir, preserve_input_flag):
        """
        This method converts the mri scan to the input shape needed for
        the neural network
        """
        # adding the log file
        logging.basicConfig(filename = os.path.join(root_dir, "pred.log"), \
                            filemode = 'a',level = logging.INFO, \
                            format='%(levelname)s:%(message)s')
        # Find the dimensions of the imported volume
        logging.info("Data Prep - Started...")
        vol = vlr.volume_reader(os.path.join(input_path))
        
        # Logging only
        ip = vol
        logging.info("Shape of input numpy: {} \n \
                      Data type of input numpy: {} \n \
                      Max value of input numpy: {} \n \
                      Unique elements are: {} \n \
                      Count of unique elements: {}" \
                      .format(ip.shape,ip.dtype,np.max(ip), np.unique(ip), len(np.unique(ip))))
        result = vol / np.max(vol)
        # vol /= np.max(vol)
        dims = list(result.shape)

        result = result.reshape(1, dims[0], dims[1], dims[2], self.num_channels)
        sid = self.find_id(input_path, preserve_input_flag)
        logging.info("Data Prep - Finished")
        return dims, self.num_channels, self.num_classes, sid, result

    @staticmethod
    def find_id(input_path,preserve_input_flag):
        """
        This method will assign a subject id to the input scan
        """
        sid = input_path.split("/")[-1]
        
        if preserve_input_flag:
          sid = sid.split(".")[0]
        else:
          sid = sid.split("_")[0]
        return sid
